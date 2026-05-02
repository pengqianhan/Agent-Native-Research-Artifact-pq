# Algorithm

## Mathematical Formulation

Let `E` be an environment with observation space `O` and action space `A`. At step `t`
the agent observes `o_t ∈ O`, selects `a_t ∈ A`, and receives reward `r_t` and next
observation `o_{t+1}`. A trajectory is
$\tau = (o_0, a_0, r_0, \ldots, o_T, a_T, r_T)$.
Tasks are specified by a natural-language description `d`. The LLM-based agent
parameterised by `θ` implements a policy `π_θ(a_t | o_{≤t}, d, c)` where `c` represents
additional context (e.g., skills, demonstrations). Subject to context length
`|c| ≤ L_max`, the goal is

$$\max_\theta \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_{t=0}^{T} \gamma^t r_t\right].$$

### Stage 1 — Experience-based skill distillation

Roll out `π_base` to collect `T = T⁺ ∪ T⁻` with
`T⁺ = {τ_i : r(τ_i) = 1}` and `T⁻ = {τ_i : r(τ_i) = 0}`. Apply differential processing:

$$s^+ = \mathcal{M}_T(\tau^+, d) \quad (\text{Eq. 2})$$
$$s^- = \mathcal{M}_T(\tau^-, d) \quad (\text{Eq. 3})$$

`s⁺` extracts strategic patterns; `s⁻` is the four-component counterfactual described in
§3.1.

### Stage 2 — Hierarchical SkillBank

$\mathcal{S} = \mathcal{S}_g \cup \bigcup_{k=1}^{K} \mathcal{S}_k$. At inference, given
task description `d`,

$$\mathcal{S}_{\mathrm{ret}} = \mathrm{TopK}\!\left(\{ s \in \mathcal{S}_k : \mathrm{sim}(e_d, e_s) > \delta \}, K \right) \quad (\text{Eq. 4})$$

The policy conditions on retrieved skills:

$$a_t \sim \pi_\theta\!\left(a_t \mid o_{\leq t}, d, \mathcal{S}_g, \mathcal{S}_{\mathrm{ret}}\right) \quad (\text{Eq. 5}).$$

### Stage 3 — Cold-start SFT

$$\theta_{\mathrm{sft}} = \arg\min_\theta \mathcal{L}_{CE}(\mathcal{D}_{SFT}; \theta) \quad (\text{Eq. 6})$$
with `D_SFT = {(d_i, S_i, τ_i*)}_{i=1}^N`. The resulting `π_θ_sft` is also `π_ref` for RL.

### Stage 4 — Skill-augmented GRPO

Per query `x`, sample `G` responses `{y^(1), …, y^(G)}` and rewards `{R_1, …, R_G}`.
Standard GRPO (Eq. 1):

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{x,\{y_i\}}\!\left[\frac{1}{G}\sum_{i=1}^{G} \min\!\left( r_i A_i, \mathrm{clip}(r_i, 1-\epsilon, 1+\epsilon) A_i \right) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right]$$

with $r_i = \pi_\theta(y_i|x)/\pi_{\mathrm{old}}(y_i|x)$ and
$A_i = (R_i - \mathrm{mean}\{R_j\}) / \mathrm{std}\{R_j\}$ (Eq. 8 for the agent setting).

In SkillRL, the importance ratio is computed over the *skill-augmented* context
(Eq. 9):

$$\rho_i = \frac{\pi_\theta(\tau^{(i)} \mid d, \mathcal{S}_g, \mathcal{S}_{\mathrm{ret}})}{\pi_{\mathrm{old}}(\tau^{(i)} \mid d, \mathcal{S}_g, \mathcal{S}_{\mathrm{ret}})}$$
$$\mathcal{J}(\theta) = \mathbb{E}_{d,\{\tau^{(i)}\}}\!\left[\frac{1}{G}\sum_{i=1}^{G} \min\!\left( \rho_i A_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) A_i \right) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right] \quad (\text{Eq. 9})$$

### Stage 5 — Recursive skill evolution

At each validation epoch, for each task category `C`:
- If `Acc(C) < δ`, collect `T_val` failed trajectories using diversity-aware stratified
  sampling (group by category, prioritize negative-reward severity, round-robin select
  to preserve categorical entropy).
- Prompt `M_T` to identify failure patterns, propose new skills, suggest refinements:

$$\mathcal{S}_{\mathrm{new}} = \mathcal{M}_T(\mathcal{T}_{\mathrm{val}}, \mathrm{SKILLBANK}) \quad (\text{Eq. 7})$$

- Update SkillBank: `SKILLBANK ← SKILLBANK ∪ S_new`.

## Pseudocode (Algorithm 1, paper §3.3, page 4)

```
Algorithm 1: SkillRL — Recursive Skill-Augmented RL
Require: Base model π_base, teacher M_T, environment E
Ensure : Trained policy π_θ*, evolved skill library SKILLBANK*

# ▷ Experience-based Skill Distillation
1:  T+, T- ← Rollout(π_base, E)
2:  for all τ+ ∈ T+ do
3:      s+ ← M_T(τ+)              # Eq. (2)
4:  end for
5:  for all τ- ∈ T- do
6:      s- ← M_T(τ-)              # Eq. (3)
7:  end for

# ▷ Hierarchical Skill Library Construction
8:  S_g ← general skills from distilled experiences
9:  for all task type k do
10:     S_k ← task-specific skills for category k
11: end for
12: SKILLBANK ← S_g ∪ ⋃_k S_k

# ▷ Recursive Skill Evolution
13: # Cold-start initialization
14: D_SFT ← M_T(E, SKILLBANK)
15: θ ← SFT(π_base, D_SFT);   π_ref ← π_θ
16:
17: # RL with recursive evolution
18: for epoch = 1 to N do
19:     for all task d do
20:         S_ret ← Retrieve(d, SKILLBANK)            # Eq. (4)
21:         Sample {τ^(i)}_{i=1..G} ~ π_θ(·|d, S_g, S_ret)   # Eq. (5)
22:         Compute {R_i}_{i=1..G} and update θ via GRPO     # Eqs. (8), (9)
23:     end for
24:     if validation epoch then
25:         T_val ← failed validation trajectories
26:         S_new ← M_T(T_val, SKILLBANK)             # Eq. (7)
27:         SKILLBANK ← SKILLBANK ∪ S_new
28:     end if
29: end for
30: return π_θ, SKILLBANK
```

## Step-by-step explanation

1. **Lines 1–7** offline distillation: a single rollout pass under `π_base` populates
   the success and failure pools; the teacher then converts each trajectory into a
   compact skill record.
2. **Lines 8–12** library construction: skills are organized into general (universal)
   and per-category (task-specific) sets.
3. **Lines 13–15** cold-start SFT: the teacher generates skill-augmented reasoning
   traces; the base model is fine-tuned on them. The fine-tuned model is the RL
   warm-start *and* the KL reference for line 22.
4. **Lines 18–29** main RL loop: for each task, retrieve relevant skills, sample `G`
   trajectories under the current policy conditioned on the skill-augmented context,
   compute group-normalized advantages, and apply the GRPO objective with the KL anchor
   to the reference policy. At validation epochs, the teacher analyses the latest
   failures and proposes additions to the bank.

## Complexity analysis

The paper does not state a formal complexity expression. From the released
implementation, per RL step the cost decomposes as:

- **Rollout cost** O(G · L) — `G = 8` parallel trajectories of length up to `L = 50`
  steps for ALFWorld and `L = 15` for WebShop; LLM forward passes dominate.
- **Retrieval cost** O(|S_k| · d) for embedding mode (cosine similarity over cached
  skill embeddings of dimension `d`); O(1) for template mode after a single keyword
  scan over `d`.
- **Skill evolution cost** O(|T_val| · cost(M_T)) at validation epochs only. With
  `max_failures_analyzed = 10` (when SR < 0.4) or 5 (when SR > 0.4) per fire and one
  teacher call per fire, the amortized RL-step cost is small (Appendix B.2 lists 0.5 h
  total for skill distillation vs 24 h RL training).

Token-budget cost. Skill distillation produces 10–20× compression of trajectory tokens
(§3.1), and the agent's average prompt length is reduced from ~1,450 to <1,300 tokens
versus the raw-memory baseline (~10.3% reduction, §4.3) — in absolute terms a savings
of ~150 tokens per inference call.
