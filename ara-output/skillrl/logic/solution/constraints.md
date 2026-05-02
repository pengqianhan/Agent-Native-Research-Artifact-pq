# Constraints

## Boundary conditions

### B1: Binary reward signal
The pipeline relies on `r(τ) ∈ {0,1}` to split rollouts into `T⁺/T⁻` (Eqs. 2, 3) and to
compute group-normalized advantages (Eq. 8). Environments with continuous or sparse
non-binary rewards would require a thresholding step before applying the same machinery.

### B2: Teacher-model dependence
Both initial skill distillation and recursive evolution depend on a high-capability
teacher `M_T`. The released code targets Azure OpenAI o3 (`skill_updater.py` and
`skill_generation/{alfworld,webshop,search}.py`). Skill quality is bounded by the
teacher's instruction-following ability; the agent cannot bootstrap stronger skills than
the teacher can articulate.

### B3: Context-length budget `|c| ≤ L_max`
The agent must operate within a finite context window (Eq. 1 of §2 explicitly states
`|c| ≤ L_max`). The released ALFWorld script sets `data.max_prompt_length=4096` and
`data.max_response_length=512`; the WebShop script uses 6000 and 768 respectively. Skill
abstraction is the mechanism keeping the augmented prompt within these limits.

### B4: Validation-epoch trigger condition
Recursive evolution only fires when `Acc(C) < δ` (default δ = 0.4) for some category at
a validation epoch. If validation success is already high for every category, evolution
is skipped — the library is stable when the policy succeeds.

### B5: Bounded library growth per epoch
At most `max_new_skills_per_update = 3` skills are added per fire (Table 4; also
enforced in `SkillUpdater.analyze_failures`). Library growth is therefore at most
3 × (number of validation epochs that fired).

### B6: Pre-existing task category taxonomy (template mode)
Template-mode retrieval relies on a hand-coded keyword-to-task-type rule
(`SkillsOnlyMemory._detect_task_type` in the released code). For ALFWorld it uses keys
{pick_and_place, look_at_obj_in_light, clean, heat, cool, examine}; for WebShop it uses
{apparel, footwear, electronics, accessories, home_decor, beauty_health, other}. New
environments require either a new keyword rule or switching to embedding mode.

### B7: Environment instrumentation
The paper assumes the environment exposes (i) a per-step observation, (ii) a list of
admissible actions for prompt formatting (Appendix Prompt A.1), and (iii) a binary task
success indicator at termination. ALFWorld and WebShop satisfy all three; arbitrary new
environments may need adapters.

## Known limitations

### L1: Reliance on offline trajectory pool
The initial SkillBank is constructed from a one-shot rollout of `π_base` (Algorithm 1
line 1). If the base model cannot reach any success state in `E`, `T⁺` is empty and only
`s⁻` records will be available; skill quality degrades. The paper does not discuss
remediation, but the released `skill_generation` scripts pre-compute memory data offline,
so this is a deployment-time consideration.

### L2: Teacher API cost
Every validation failure-cycle calls the teacher; over 150 RL training steps with
test_freq=5, this is up to 30 teacher calls per run, in addition to the upfront
distillation pass. Researchers without access to a strong frontier teacher (the released
code targets o3 specifically) cannot reproduce identical skills.

### L3: Skill-quality variance not quantified
The paper does not report variance (multiple seeds) for the main results in Tables 1, 2
or 3. Reproductions should expect run-to-run variance not reflected in the reported
single numbers.

### L4: No comparison with same-model SFT baselines
The closest "skill-aware SFT only" comparison (Cold-Start SFT without the RL stage) is
not separately tabulated; only the inverse — RL without cold-start SFT — is reported in
the ablation. Therefore the standalone contribution of cold-start SFT relative to
classic instruction tuning is not isolated.

### L5: Search task does not use task-specific skills
The released search skill JSON contains only general skills (10) and common mistakes
(11) and zero task-specific skills (verified directly:
`memory_data/search/claude_style_skills_search.json` has `task_specific_skills = {}`).
The hierarchical-structure ablation result on search-augmented QA is therefore not
applicable in the exact form reported for ALFWorld/WebShop.

### L6: Inference still requires the embedding model in embedding mode
Embedding-mode retrieval requires loading Qwen3-Embedding-0.6B at inference time,
adding ~600M parameters of GPU memory beyond the 7B agent. Template mode avoids this
cost but is restricted to the keyword-rule taxonomy (B6).

### L7: All RL experiments with Qwen2.5-7B
All claimed numerical results (Tables 1–3) are with Qwen2.5-7B-Instruct as the base.
The paper does not test smaller (e.g., 1.5B) or larger (e.g., 70B) base models, so the
size-dependence of the SkillRL effect is not characterized — even though one of the
released training scripts is named for a 1.5B SFT checkpoint, no numbers for that
model size are reported.

### L8: ALFWorld and WebShop use the same script template
The released `run_alfworld_skills.sh` sets `tensor_model_parallel_size=4` and
`n_gpus_per_node=4`, while `run_webshop_skills.sh` sets `n_gpus_per_node=8`. Hardware
budget is not identical between environments, although both fit in the 8 × H100
configuration described in Appendix B.2.
