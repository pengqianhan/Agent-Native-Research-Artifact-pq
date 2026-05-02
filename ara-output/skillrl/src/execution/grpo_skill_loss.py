"""Skill-augmented GRPO objective — Eqs. (8) and (9).

Per query (task description) `d`, the trainer samples G trajectories
`{τ^(i)}` under the current policy with the policy conditioned on the
*skill-augmented* context `(d, S_g, S_ret)`. Group-normalized advantages
and a KL anchor to the cold-start SFT model `π_ref = π_θ_sft` are used.

This stub assumes the verl trainer machinery handles batching, distributed
training, and rollout generation; what follows is the loss computation that
plugs into a verl-style actor update.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

import torch
import torch.nn.functional as F


@dataclass
class GRPOConfig:
    epsilon: float = 0.2     # PPO clip half-width (paper notation in Eq. 9)
    beta: float = 0.01       # KL coefficient β (Table 4: kl_loss_coef = 0.01)
    eps_adv_std: float = 1e-8


def grouped_advantages(rewards: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
    """Eq. (8): group-normalised advantage.

    Args:
        rewards: shape (G,) of binary task rewards r(τ^(i)) ∈ {0, 1}.

    Returns:
        Advantages of shape (G,).
    """
    mean = rewards.mean()
    std = rewards.std(unbiased=False).clamp_min(eps)
    return (rewards - mean) / std


def low_variance_kl(
    log_pi: torch.Tensor, log_pi_ref: torch.Tensor
) -> torch.Tensor:
    """Low-variance KL estimator used by verl when ``kl_loss_type=low_var_kl``.

    Args:
        log_pi:     log π_θ(τ^(i) | d, S_g, S_ret), shape (G, T).
        log_pi_ref: log π_ref(τ^(i) | d, S_g, S_ret), shape (G, T).

    Returns:
        Per-sequence KL, shape (G,).
    """
    delta = log_pi_ref - log_pi
    # k3 estimator: exp(δ) − 1 − δ ≥ 0, lower variance than (log π − log π_ref).
    return ((delta.exp() - 1.0) - delta).sum(dim=-1)


def skill_augmented_grpo_loss(
    *,
    log_pi: torch.Tensor,
    log_pi_old: torch.Tensor,
    log_pi_ref: torch.Tensor,
    rewards: torch.Tensor,
    response_mask: torch.Tensor,
    cfg: GRPOConfig = GRPOConfig(),
) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    """Eq. (9): skill-augmented GRPO objective with PPO clip and KL anchor.

    All per-token tensors are computed over the response tokens only; the
    skill-augmented prompt context (`d, S_g, S_ret`) is part of the model
    input and is masked out via `response_mask`.

    Args:
        log_pi:        log π_θ(a_t | …, d, S_g, S_ret) over response tokens, (G, T).
        log_pi_old:    log π_old over the same trajectories, (G, T).
        log_pi_ref:    log π_ref = log π_{θ_sft} over the same trajectories, (G, T).
        rewards:       binary task reward per trajectory, (G,).
        response_mask: 1 over response tokens, 0 over prompt/padding, (G, T).
        cfg:           GRPO hyperparameters.

    Returns:
        ``(loss, metrics)`` where loss is a scalar and metrics is a dict of
        diagnostic scalars (mean policy-loss, mean KL, advantage stats).
    """
    # Per-token importance ratio ρ_t = exp(log π_θ - log π_old).
    log_ratio = log_pi - log_pi_old
    ratio = log_ratio.exp()

    # Group-normalised advantage broadcast to the response token dimension.
    advantages = grouped_advantages(rewards, eps=cfg.eps_adv_std)  # (G,)
    adv_per_token = advantages.unsqueeze(-1).expand_as(ratio)      # (G, T)

    # PPO-clipped policy loss.
    surr1 = ratio * adv_per_token
    surr2 = torch.clamp(ratio, 1.0 - cfg.epsilon, 1.0 + cfg.epsilon) * adv_per_token
    clipped = torch.min(surr1, surr2)
    policy_loss = -((clipped * response_mask).sum() / response_mask.sum().clamp_min(1.0))

    # KL anchor to the cold-start SFT reference (low-variance estimator,
    # token-aggregated).
    delta = log_pi_ref - log_pi
    kl_per_token = (delta.exp() - 1.0) - delta
    kl_loss = (kl_per_token * response_mask).sum() / response_mask.sum().clamp_min(1.0)

    loss = policy_loss + cfg.beta * kl_loss

    return loss, {
        "policy_loss": policy_loss.detach(),
        "kl_loss": kl_loss.detach(),
        "advantage_mean": advantages.mean().detach(),
        "advantage_std": advantages.std(unbiased=False).detach(),
        "ratio_mean": ratio.detach().mean(),
    }


def invalid_action_penalty(
    actions_valid: torch.Tensor,
    rewards: torch.Tensor,
    coef: float = 0.1,
) -> torch.Tensor:
    """Subtract a per-trajectory penalty for steps that emitted an invalid action.

    Mirrors the released option ``actor_rollout_ref.actor.use_invalid_action_penalty=True``
    with ``invalid_action_penalty_coef=0.1``. ``actions_valid`` is a binary
    mask of shape (G, T_actions) where 0 marks an invalid (rejected) action.
    """
    invalid_count = (1.0 - actions_valid).sum(dim=-1)  # (G,)
    return rewards - coef * invalid_count
