"""Hierarchical skill retrieval — Eq. (4) and Eq. (5).

Two retrieval modes mirror the released ``SkillsOnlyMemory.retrieve``:
  * ``"template"`` — keyword task-type detection then return all skills under
    the matched category. No GPU model is loaded.
  * ``"embedding"`` — encode (task description, every skill) with
    Qwen3-Embedding-0.6B and rank by cosine similarity; cross-category top-K.

General skills `S_g` are always included (they are universal strategic
principles per paper §3.2). Dynamic skills (id starting with ``dyn_``) are
included unconditionally so evolution-derived guidance is not dropped by a
naive ``[:top_k]`` slice — see heuristic H07.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Literal


Skill = dict[str, str]
RetrievalMode = Literal["template", "embedding"]


@dataclass
class RetrievalResult:
    general_skills: list[Skill]
    task_specific_skills: list[Skill]
    mistakes_to_avoid: list[Skill]
    task_type: str
    retrieval_mode: RetrievalMode


def retrieve(
    task_description: str,
    skillbank: dict,
    *,
    top_k: int = 6,
    task_specific_top_k: int | None = None,
    mode: RetrievalMode = "template",
    similarity_threshold: float = 0.4,
    classify_task: Callable[[str], str] | None = None,
    encode: Callable[[str], "Vector"] | None = None,
    cached_skill_embeddings: "tuple[list[tuple[str, str | None, Skill]], Any] | None" = None,
) -> RetrievalResult:
    """Compose the in-context skill set for the current task description.

    Args:
        task_description:        Free-form goal string `d`.
        skillbank:               Dict with keys ``general_skills``,
                                  ``task_specific_skills``, ``common_mistakes``.
        top_k:                    Budget for general skills (Eq. 4 budget K).
        task_specific_top_k:      Budget for task-specific skills. ``None``
                                  means "all in matched category" (template
                                  mode) or "same as top_k" (embedding mode).
        mode:                     ``"template"`` or ``"embedding"``.
        similarity_threshold:     δ in Eq. (4) — only matters for embedding mode.
        classify_task:            Callable returning the task category for `d`
                                  (template mode only).
        encode:                   Callable that returns a normalized embedding
                                  for a string (embedding mode only).
        cached_skill_embeddings:  Pre-computed (items, matrix) for embedding mode.

    Returns:
        ``RetrievalResult`` to be formatted into the agent prompt block.
    """
    common_mistakes = skillbank.get("common_mistakes", [])[:5]

    if mode == "embedding":
        ts_top_k = task_specific_top_k if task_specific_top_k is not None else top_k
        general, task_specific = _embedding_retrieve(
            task_description=task_description,
            cached=cached_skill_embeddings,
            encode=encode,  # type: ignore[arg-type]
            top_k_general=top_k,
            top_k_task_specific=ts_top_k,
            similarity_threshold=similarity_threshold,
        )
        task_type = classify_task(task_description) if classify_task else "unknown"
        return RetrievalResult(
            general_skills=general,
            task_specific_skills=task_specific,
            mistakes_to_avoid=common_mistakes,
            task_type=task_type,
            retrieval_mode="embedding",
        )

    # Template mode.
    if classify_task is None:
        raise ValueError("template mode requires classify_task")
    task_type = classify_task(task_description)

    # H07: always include all dyn_ skills first, then fill the budget with
    # static skills. Without this, a naive [:top_k] slice silently drops
    # newly-evolved skills once the bank exceeds top_k.
    all_general = skillbank.get("general_skills", [])
    dynamic = [s for s in all_general if s.get("skill_id", "").startswith("dyn_")]
    static = [s for s in all_general if not s.get("skill_id", "").startswith("dyn_")]
    n_static = max(0, top_k - len(dynamic))
    general_skills = dynamic + static[:n_static]

    all_task_skills = skillbank.get("task_specific_skills", {}).get(task_type, [])
    if task_specific_top_k is not None:
        task_skills = all_task_skills[:task_specific_top_k]
    else:
        task_skills = all_task_skills  # original behaviour: return all in category

    return RetrievalResult(
        general_skills=general_skills,
        task_specific_skills=task_skills,
        mistakes_to_avoid=common_mistakes,
        task_type=task_type,
        retrieval_mode="template",
    )


def _embedding_retrieve(
    task_description: str,
    cached: Any,
    encode: Callable[[str], "Vector"],
    top_k_general: int,
    top_k_task_specific: int,
    similarity_threshold: float,
) -> tuple[list[Skill], list[Skill]]:
    """Eq. (4) realisation: cosine similarity ranking with threshold δ.

    `cached` is an opaque structure of (items, embedding_matrix) where
    `items[i] = (kind, task_type, skill_dict)` and the first `n_general`
    rows correspond to general skills.
    """
    import numpy as np  # local import keeps the stub light

    items, embeddings, n_general = cached  # type: ignore[misc]
    query_emb = encode(task_description)
    sims = embeddings @ query_emb  # cosine similarity (embeddings pre-normalized)

    general_sims = sims[:n_general]
    task_sims = sims[n_general:]

    g_idx = np.argsort(general_sims)[::-1][:top_k_general]
    general = [items[int(i)][2] for i in g_idx]

    # Threshold filter then top-K (Eq. 4).
    valid = np.where(task_sims > similarity_threshold)[0]
    if valid.size > 0:
        order = valid[np.argsort(task_sims[valid])[::-1]][:top_k_task_specific]
        task_specific = [items[n_general + int(i)][2] for i in order]
    else:
        task_specific = []

    return general, task_specific


def format_for_prompt(result: RetrievalResult) -> str:
    """Render the retrieved skills as the multi-section block injected under
    `## Retrieved Relevant Experience` (Appendix Prompt A.1)."""
    sections: list[str] = []
    if result.general_skills:
        lines = ["### General Principles"]
        for s in result.general_skills:
            lines.append(f"- **{s.get('title', '')}**: {s.get('principle', '')}")
        sections.append("\n".join(lines))

    if result.task_specific_skills:
        if result.retrieval_mode == "embedding":
            header = "### Task-Relevant Skills"
        else:
            header = f"### {result.task_type.replace('_', ' ').title()} Skills"
        lines = [header]
        for s in result.task_specific_skills:
            lines.append(f"- **{s.get('title', '')}**: {s.get('principle', '')}")
            when = s.get("when_to_apply", "")
            if when:
                lines.append(f"  _Apply when: {when}_")
        sections.append("\n".join(lines))

    if result.mistakes_to_avoid:
        lines = ["### Mistakes to Avoid"]
        for m in result.mistakes_to_avoid:
            desc = m.get("description", "")
            fix = m.get("how_to_avoid", "")
            if desc:
                lines.append(f"- **Don't**: {desc}")
                if fix:
                    lines.append(f"  **Instead**: {fix}")
        sections.append("\n".join(lines))

    return "\n\n".join(sections) if sections else "No relevant skills found for this task."


# Lightweight type alias used only for documentation purposes.
class Vector:  # pragma: no cover
    pass
