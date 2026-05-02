# Appendix Skill Catalog and Prompt Templates

This file routes the appendix material from the paper (Appendix A — Prompts; Appendix C
— Illustration of Skill Library; Appendix D — Additional Cases) into the ARA. Numerical
content is preserved verbatim. Per-entry skill records are kept rather than reduced to
counts so the granularity matches the source.

## A. Prompt Templates

### Prompt A.1 — ALFWorld Agent Execution with Skills (Appendix A.1, page 12)
**System Prompt**:
> You are an expert agent operating in the ALFRED Embodied Environment. Your task is to: {task_description}
>
> ## Retrieved Relevant Experience
> {retrieved_memories}
>
> ## Current Progress
> Prior to this step you have already taken {step_count} step(s). Below are the most recent {history_length} observations and the corresponding actions you took: {action_history}
> You are now at step {current_step} and your current observation is: {current_observation}
> Your admissible actions of the current situation are: [{admissible_actions}].
>
> Now it's your turn to take an action. You should first reason step-by-step about the current situation. This reasoning process MUST be enclosed within <think> </think> tags. Once you've finished your reasoning, you should choose an admissible action for current step and present it within <action> </action> tags.

### Prompt A.2 — WebShop Agent Execution with Skills (Appendix A.1, page 12)
> You are an expert autonomous agent operating in the WebShop e-commerce environment. Your task is to: {task_description}.
>
> ## Retrieved Relevant Experience
> {retrieved_memories}
>
> ## Current Progress
> Prior to this step you have already taken {step_count} step(s). … (analogous structure with `available_actions` instead of `admissible_actions`).

### Prompt B.1 — Dynamic Skill Discovery from Failures (Appendix A.2, page 13)
> Analyze these failed {env_description} agent trajectories and suggest NEW skills to add.
>
> FAILED TRAJECTORIES: {failure_examples}
> EXISTING SKILL TITLES: {existing_titles}
>
> Generate 1-3 NEW actionable skills that would help avoid these failures. Each skill must have: skill_id, title (3-5 words), principle (1-2 sentences), when_to_apply. The skill_id should be unique and follow the pattern: "dyn_001", "dyn_002", etc.
>
> Return ONLY a JSON array of skills, no other text.

### Prompt B.2 — Initial Skill Distillation (ALFWorld) (Appendix A.2)
> You are an expert at distilling agent behavior patterns into concise, actionable skills. Analyze these successful and failed trajectories from an embodied AI agent operating in household environments (ALFWorld).
>
> SUCCESSFUL TRAJECTORIES: {success_patterns}
> FAILED TRAJECTORIES: {failure_patterns}
>
> Generate 8-12 GENERAL SKILLS that apply across ALL task types. These should be: 1. Concise; 2. Actionable; 3. Transferable; 4. Failure-aware. Focus on: Navigation, object manipulation, state tracking, error recovery, and container interaction rules.

### Prompt B.3 — Initial Skill Distillation (WebShop) (Appendix A.2)
> Analyze these successful and failed trajectories from an AI agent operating in an online shopping environment (WebShop). Generate 10-15 GENERAL SKILLS. Focus on: Search query formulation, product selection heuristics, option configuration (size, color, etc.), constraint verification, navigation patterns, and price handling.

### Prompt C.1 — Synthetic Trajectory Generation (ALFWorld) (Appendix A.3, page 13)
> You are an expert agent in the ALFRED embodied environment. You will be given a task and relevant skills to apply. Your goal is to generate a successful trajectory that demonstrates proper use of these skills.
>
> You should generate a step-by-step trajectory that: 1. Uses the provided skills appropriately; 2. Takes realistic actions in the environment; 3. Completes the task successfully; 4. Demonstrates good planning and systematic exploration.

### Prompt C.2 — Synthetic Trajectory Generation (WebShop) (Appendix A.3, page 14)
> Analogous prompt for WebShop with action vocabulary `search[query], click[element], buy now`.

## C. Skill Library — Verbatim Examples

### Table 5: Example distilled skills from SkillBank for ALFWorld (page 15)

**General Exploration & Acquisition Skills**

| ID | Skill Title | Principle (Actionable Pattern) | When to Apply |
|----|-------------|-------------------------------|---------------|
| gen_001 | Systematic Exploration | Search every plausible surface or container exactly once before revisiting; prioritize unseen locations. | Anytime the goal count is not met and unexplored areas remain. |
| gen_002 | Immediate Acquisition | As soon as a required object becomes visible and reachable, take it immediately. | Upon first visual confirmation of a goal-relevant object. |
| gen_003 | Destination First Policy | After picking up a goal object, navigate directly to the known target receptacle and place it. | Holding any goal object while target location is identified. |

**State-Changing & Spatial Relation Skills**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_005 | Use State-Changing Tools Early | Acquire the object, then immediately use the nearest suitable appliance (heat/cool/clean) before placement. | After picking up an object requiring temperature or cleanliness change. |
| gen_006 | Establish Spatial Relations | First locate the reference object, adjust its state if needed, then search or place in the specified region. | Tasks containing prepositions like "under", "inside", or "on". |

**Reliability & Error Recovery**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_014 | Loop Escape Trigger | If the last 3-5 actions do not change the state, switch to an untried search branch or action type. | After several consecutive no-progress observations. |
| gen_015 | Pre-Action Sanity Check | Confirm prerequisites (hand free, capacity, power) before executing manipulative commands. | Right before issuing any command that could legally fail. |

### Table 6: Common Agent Failures and Mitigation Strategies for ALFWorld (page 15)

| ID | Failure Description | Root Cause | Mitigation |
|----|---------------------|------------|-------------|
| err_001 | Redundant Revisit | Lacks explicit memory of explored areas; strategy degenerates into local loops. | Maintain an exploration map; prioritize unvisited candidates. |
| err_006 | Skipping State Changes | Conflates object presence with goal satisfaction; omits cleanliness/temp checks. | Integrate state precondition checks into the planner before placement. |

### Table 7: Example distilled skills for WebShop Navigation (page 16)

**Search & Query Engineering**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_001 | Prioritize Core Keywords | Include product type, 1-2 functional attributes, and hard constraints; omit secondary descriptors. | Before issuing the first search or refining over-specific queries. |
| gen_002 | Iterative Refinement | Adjust keywords or apply site filters instead of repeating the same failed query. | When results are irrelevant or repeat despite multiple searches. |

**Product Evaluation & Verification**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_003 | Scan Before You Click | Read titles, thumbnails, and prices in results to ensure plausibility before opening a link. | On search-results pages when choosing the next product to inspect. |
| gen_004 | Verify Early, Abort Fast | Immediately check category, attributes, and price on the product page; leave if any constraint is violated. | Within the first observation on every product detail page. |
| gen_006 | Confirm Hidden Attributes | Open Description/Features sections to ensure non-visible specs (e.g., material) meet constraints. | When constraints are not evident from the title or variant list. |

**Configuration & Transaction**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_005 | Set Mandatory Variants | Always select required options (size, color, etc.) before evaluating price or purchasing. | After confirming product match but before any purchase action. |
| gen_007 | Check Variant Pricing | For price ranges, select the exact variant combination to verify the specific price is within budget. | Whenever price changes with variant selection or shows as a range. |
| gen_013 | Purchase Decisively | Execute "Buy Now" immediately once all constraints and prices are confirmed on a variant. | After validating every constraint on the current product variant. |

### Table 8: Common Failures in Web-based Shopping Tasks (page 16)

| ID | Failure Description | Root Cause | Mitigation Strategy |
|----|---------------------|------------|---------------------|
| err_001 | Missing Constraints in Query | Omits size or price caps, leading to overwhelming or irrelevant result sets. | Assemble full requirement list first; ensure every hard constraint is in the query string. |
| err_004 | Price Shift Oversight | Fails to notice price changes after selecting a specific size or color variant. | Re-read the price element after every option change before proceeding to checkout. |
| err_005 | Premature Purchase | Clicks "Buy Now" without setting mandatory variants, leading to errors or wrong items. | Validate that every required dropdown/radio option is explicitly selected before buying. |
| err_009 | Ignoring Stock Status | Attempts to purchase out-of-stock items by ignoring disabled buttons or 'Out of Stock' messages. | Verify that the 'Add to Cart' button is enabled and no 'Out of Stock' message is present post-selection. |
| err_011 | Sponsored Link Distraction | Clicks loosely matched ads, diverting the workflow from organic, suitable products. | Implement ad-label detection; prioritize organic listings for higher constraint reliability. |

## D. Additional Case Studies (page 17–18)

The paper includes worked-trajectory case studies illustrating skill-guided reasoning.
We summarize the structure (skills referenced, mistakes avoided, and outcome). Full
step-by-step transcripts appear on pages 17–18.

| Case | Environment | Task | Skills Applied | Mistakes Avoided | Result |
|------|-------------|------|----------------|------------------|--------|
| 1 (page 17) | WebShop | Men's black slip-resistant work shoes, size 10, rubber sole, < $50 | foo_002 (Verify features in description), foo_004 (Confirm price after variant selection) | err_001 (Omitting price cap), err_003 (Wrong product category) | SUCCESS — Purchased at $38.99 |
| 2 (page 17) | WebShop | Portable bluetooth speaker, waterproof, black, < $30 | ele_001 (Constraint-rich search), ele_004 (Bail on mismatch fast), gen_002 (Iterative refinement) | err_002 (Overly specific variant names), ele_006 (Click loops) | SUCCESS — Used early-abort to switch candidates |
| 1 (page 18) | ALFWorld | Clean some lettuce and put it in countertop | cle_001 (Phase-ordered Locate→Clean→Place), cle_006 (Use location priors: Fridge for food) | err_002 (Skipping closed containers), err_003 (Ignoring visible target objects) | SUCCESS (7 steps) |
| 2 (page 18) | ALFWorld | Heat some egg and put it in countertop | hea_001 (Secure exact target first), hea_003 (Open-Place-Heat sequence), hea_004 (No appliance before object) | n/a | SUCCESS (8 steps) |
| 3 (page 18) | ALFWorld | Look at pencil under the desklamp | loo_001 (Seek lamp surfaces — Desk/Sidetable), loo_002 (Switch lamp on), exa_001 (Pair objects early), exa_002 (Pick target before tool) | err_003 (Ignoring reachable targets), loo_005 (Toggle only once) | SUCCESS (Optimal 3 steps) |

## Released SkillBank counts (verified directly from `memory_data/`)

| Environment | General | Task-specific | Common mistakes | Total |
|-------------|---------|---------------|-----------------|-------|
| ALFWorld    | 12      | 32 (across 6 task types) | 11 | 55 |
| WebShop     | 15      | 39 (across 7 task types) | 12 | 66 |
| Search      | 10      | 0  (no task-specific subset)         | 11 | 21 |

Source: `memory_data/{alfworld,webshop,search}/claude_style_skills*.json` in the
released repo.
