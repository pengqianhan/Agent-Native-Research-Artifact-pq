"""Skill distillation — convert raw trajectories into structured skill records.

Implements Eqs. (2) and (3) of SkillRL: a teacher model M_T converts
successful trajectories into strategic-pattern skills (s+) and failed ones into
four-component failure lessons (s-). Used once at SkillBank construction.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, Literal


TrajectoryStep = dict
Trajectory = list[TrajectoryStep]
Outcome = Literal["success", "failure"]


@dataclass
class Skill:
    skill_id: str
    title: str
    principle: str
    when_to_apply: str


@dataclass
class FailureLesson:
    skill_id: str
    title: str
    failure_point: str
    flawed_reasoning_or_action: str
    what_should_have_been_done: str
    generalizable_principle: str


def split_by_outcome(
    trajectories: list[tuple[str, Trajectory, int]],
) -> tuple[list[tuple[str, Trajectory]], list[tuple[str, Trajectory]]]:
    """Partition (task_description, trajectory, reward) tuples into (T+, T-).

    The reward `r ∈ {0, 1}` is the binary task-success indicator (paper §2).
    """
    success: list[tuple[str, Trajectory]] = []
    failure: list[tuple[str, Trajectory]] = []
    for task_desc, traj, reward in trajectories:
        if reward == 1:
            success.append((task_desc, traj))
        else:
            failure.append((task_desc, traj))
    return success, failure


def distill_success(
    teacher_call: Callable[[str], str],
    task_description: str,
    trajectory: Trajectory,
) -> Skill:
    """Eq. (2): s+ = M_T(τ+, d).

    The teacher identifies critical decision points, the reasoning behind correct
    actions, and patterns that transfer beyond the specific task instance.
    """
    prompt = _build_success_prompt(task_description, trajectory)
    raw = teacher_call(prompt)
    return _parse_skill_json(raw)


def distill_failure(
    teacher_call: Callable[[str], str],
    task_description: str,
    trajectory: Trajectory,
) -> FailureLesson:
    """Eq. (3): s- = M_T(τ-, d).

    The teacher synthesises four components: (1) point of failure, (2) flawed
    reasoning or action, (3) what should have been done, (4) generalizable
    principle to prevent similar failures (paper §3.1).
    """
    prompt = _build_failure_prompt(task_description, trajectory)
    raw = teacher_call(prompt)
    return _parse_failure_json(raw)


def build_initial_skillbank(
    teacher_call: Callable[[str], str],
    trajectories: list[tuple[str, Trajectory, int]],
    task_categories: Iterable[str],
    classify_task: Callable[[str], str],
) -> dict:
    """Build the initial hierarchical SkillBank (Algorithm 1 lines 1-12).

    Returns a JSON-serializable dict matching the released
    ``claude_style_skills.json`` schema with keys
    ``general_skills``, ``task_specific_skills``, ``common_mistakes``.
    """
    success, failure = split_by_outcome(trajectories)

    # Extract general skills from a mix of all successes/failures.
    general: list[Skill] = []
    general_prompt = _build_general_prompt(success, failure)
    for s in _parse_skill_array(teacher_call(general_prompt)):
        general.append(s)

    # Per-category task-specific skills.
    task_specific: dict[str, list[Skill]] = {k: [] for k in task_categories}
    for category in task_categories:
        cat_success = [(d, t) for d, t in success if classify_task(d) == category]
        cat_failure = [(d, t) for d, t in failure if classify_task(d) == category]
        if not cat_success and not cat_failure:
            continue
        prompt = _build_task_specific_prompt(category, cat_success, cat_failure)
        task_specific[category] = list(_parse_skill_array(teacher_call(prompt)))

    # Common mistakes derived from failure trajectories.
    common_mistakes = list(
        _parse_failure_array(teacher_call(_build_mistakes_prompt(failure)))
    )

    return {
        "general_skills": [skill.__dict__ for skill in general],
        "task_specific_skills": {k: [s.__dict__ for s in v] for k, v in task_specific.items()},
        "common_mistakes": [m.__dict__ for m in common_mistakes],
    }


# --- Prompt builders + JSON parsers ----------------------------------------
# These are intentionally minimal stubs; the released
# ``skill_generation/alfworld.py`` (and ``webshop.py``, ``search.py``)
# files contain the full prompt templates from Appendix A.2 (Prompts B.2-B.3).

def _build_general_prompt(success, failure) -> str: ...
def _build_task_specific_prompt(category, success, failure) -> str: ...
def _build_mistakes_prompt(failure) -> str: ...
def _build_success_prompt(task_description, trajectory) -> str: ...
def _build_failure_prompt(task_description, trajectory) -> str: ...
def _parse_skill_json(raw: str) -> Skill: ...
def _parse_failure_json(raw: str) -> FailureLesson: ...
def _parse_skill_array(raw: str) -> Iterable[Skill]: ...
def _parse_failure_array(raw: str) -> Iterable[FailureLesson]: ...
