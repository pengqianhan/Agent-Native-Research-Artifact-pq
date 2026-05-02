"""Recursive skill evolution — Eq. (7) and Algorithm 1 lines 24-28.

At each validation epoch and for each task category C:
  * if Acc(C) < δ, gather failed validation trajectories using diversity-aware
    stratified sampling (paper §3.3),
  * prompt the teacher model M_T to (a) identify failure patterns not addressed
    by current skills, (b) propose new skills, (c) suggest refinements,
  * append the result (capped at ``max_new_skills_per_update``) to the
    SkillBank under ``general_skills`` with auto-assigned ``dyn_NNN`` IDs.

Mirrors ``agent_system/memory/skill_updater.py`` in the released code.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Callable


Trajectory = list[dict]
Skill = dict[str, str]


@dataclass
class FailedValidationTraj:
    task: str
    task_type: str
    trajectory: Trajectory


@dataclass
class EvolutionConfig:
    threshold_delta: float = 0.4              # δ in §3.3 / Table 4
    max_new_skills_per_update: int = 3        # Table 4
    max_failures_low_sr: int = 10             # SR < 0.4
    max_failures_high_sr: int = 5             # SR > 0.4


@dataclass
class EvolutionLogEntry:
    epoch: int
    category: str
    num_failures_analyzed: int
    new_skill_ids: list[str] = field(default_factory=list)


def should_trigger_evolution(
    per_category_acc: dict[str, float], threshold_delta: float
) -> list[str]:
    """Return the list of categories whose validation success is below δ."""
    return [c for c, acc in per_category_acc.items() if acc < threshold_delta]


def stratified_failure_sample(
    failures: list[FailedValidationTraj],
    *,
    overall_sr: float,
    cfg: EvolutionConfig,
    severity: Callable[[FailedValidationTraj], float] | None = None,
) -> list[FailedValidationTraj]:
    """Diversity-aware stratified sampling (§3.3).

    Trajectories are grouped by category, prioritised by negative-reward
    severity, and selected via round-robin to maintain categorical entropy.
    """
    cap = cfg.max_failures_low_sr if overall_sr < cfg.threshold_delta else cfg.max_failures_high_sr
    by_cat: dict[str, list[FailedValidationTraj]] = {}
    for f in failures:
        by_cat.setdefault(f.task_type, []).append(f)

    if severity is not None:
        for cat in by_cat:
            by_cat[cat].sort(key=severity, reverse=True)

    selected: list[FailedValidationTraj] = []
    while len(selected) < cap and any(by_cat.values()):
        for cat in list(by_cat.keys()):
            if not by_cat[cat]:
                continue
            selected.append(by_cat[cat].pop(0))
            if len(selected) >= cap:
                break
    return selected


def next_dyn_index(skillbank: dict) -> int:
    """Return the next unused integer for a `dyn_NNN` skill_id."""
    pattern = re.compile(r"^dyn_(\d+)$")
    max_idx = 0
    for s in skillbank.get("general_skills", []):
        m = pattern.match(s.get("skill_id", ""))
        if m:
            max_idx = max(max_idx, int(m.group(1)))
    for skills in skillbank.get("task_specific_skills", {}).values():
        for s in skills:
            m = pattern.match(s.get("skill_id", ""))
            if m:
                max_idx = max(max_idx, int(m.group(1)))
    return max_idx + 1


def reassign_dyn_ids(skills: list[Skill], start_idx: int) -> list[Skill]:
    """Replace whatever IDs the teacher returned with `dyn_NNN` starting at start_idx."""
    return [
        {**s, "skill_id": f"dyn_{start_idx + i:03d}"}
        for i, s in enumerate(skills)
    ]


def evolve_skillbank(
    skillbank: dict,
    failures: list[FailedValidationTraj],
    *,
    overall_sr: float,
    cfg: EvolutionConfig,
    teacher_call: Callable[[str], str],
    epoch: int,
) -> tuple[dict, EvolutionLogEntry]:
    """One iteration of Algorithm 1 lines 24-28.

    Returns the updated SkillBank and a log entry summarising the round.
    """
    sampled = stratified_failure_sample(failures, overall_sr=overall_sr, cfg=cfg)
    if not sampled:
        return skillbank, EvolutionLogEntry(epoch=epoch, category="*", num_failures_analyzed=0)

    start_idx = next_dyn_index(skillbank)
    prompt = _build_evolution_prompt(sampled, skillbank, start_idx, cfg.max_new_skills_per_update)
    raw = teacher_call(prompt)
    proposed = _parse_skill_array(raw)

    capped = reassign_dyn_ids(proposed, start_idx)[: cfg.max_new_skills_per_update]
    if not capped:
        return skillbank, EvolutionLogEntry(
            epoch=epoch, category="*", num_failures_analyzed=len(sampled)
        )

    new_bank = {**skillbank, "general_skills": list(skillbank.get("general_skills", []))}
    existing_ids = _collect_skill_ids(new_bank)
    for s in capped:
        if s["skill_id"] in existing_ids:
            continue
        new_bank["general_skills"].append(s)
        existing_ids.add(s["skill_id"])

    return new_bank, EvolutionLogEntry(
        epoch=epoch,
        category=",".join(sorted({f.task_type for f in sampled})),
        num_failures_analyzed=len(sampled),
        new_skill_ids=[s["skill_id"] for s in capped],
    )


def _collect_skill_ids(bank: dict) -> set[str]:
    ids: set[str] = set()
    for s in bank.get("general_skills", []):
        sid = s.get("skill_id")
        if sid:
            ids.add(sid)
    for skills in bank.get("task_specific_skills", {}).values():
        for s in skills:
            sid = s.get("skill_id")
            if sid:
                ids.add(sid)
    return ids


def _build_evolution_prompt(
    failures: list[FailedValidationTraj],
    skillbank: dict,
    start_idx: int,
    max_new: int,
) -> str:
    """Realise the prompt template from Appendix Prompt B.1."""
    ...


def _parse_skill_array(raw: str) -> list[Skill]:
    """Parse the JSON-array response. Released code at
    ``skill_updater._parse_skills_response`` extracts ``[ ... ]`` substring and
    validates required fields (``skill_id``, ``title``, ``principle``)."""
    ...
