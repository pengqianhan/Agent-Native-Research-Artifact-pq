# Table 5: Example distilled skills from SkillBank for ALFWorld

- **Source**: Table 5, Appendix C (page 15)
- **Caption**: "Example distilled skills from SKILLBANK for ALFWorld (Shridhar et al.). This table summarizes general patterns and application logic derived from raw trajectories."
- **Extraction type**: raw_table

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
