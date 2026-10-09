"""Small, dependency-free helpers for the Streamlit NLP application."""

from dataclasses import dataclass
import json
import re
from typing import Any, Dict, Iterable, Optional, Tuple


TOPIC_L2_BY_L1 = {
    "Politics": ("India", "UK", "USA"),
    "Sports": ("Cricket", "Football", "Tennis", "Olympics"),
    "Technology": ("AI", "Space", "Gadgets"),
    "Entertainment": ("Bollywood", "Hollywood"),
    "Health": ("Nutrition", "Mental Health", "Fitness"),
    "History": ("India", "World Wars"),
    "Geography": ("Countries", "Cities"),
    "General": ("General",),
}

INTERRUPT_PATTERNS = (
    r"^\s*(brb|brt|back|ok|okay|k|thanks|thank you|got it|noted|alright|sure|"
    r"wait|wait a sec|hold on|one sec|give me a (min|sec|moment)|be right back|"
    r"i.?m back|coming back|just a min|afk)[.!?]?\s*$",
)


@dataclass(frozen=True)
class ExpansionDecision:
    expanded_query: str
    needs_clarification: bool = False
    clarification_question: str = ""
    answer: str = ""


def is_interruption(text: str) -> bool:
    """Return True only for known acknowledgements/fillers, not arbitrary short queries."""
    normalized = text.strip()
    return any(re.match(pattern, normalized, re.IGNORECASE) for pattern in INTERRUPT_PATTERNS)


def parse_expansion_decision(content: str, original_message: str) -> ExpansionDecision:
    """Parse the LLM JSON response, including common wrapper and key variations."""
    candidate = content.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.IGNORECASE)
        candidate = re.sub(r"\s*```\s*$", "", candidate)
    try:
        object_start = candidate.find("{")
        if object_start < 0:
            raise json.JSONDecodeError("No JSON object", candidate, 0)
        payload, _ = json.JSONDecoder().raw_decode(candidate[object_start:])
    except (json.JSONDecodeError, TypeError, ValueError):
        return ExpansionDecision(
            expanded_query=original_message,
            needs_clarification=True,
            clarification_question="I couldn’t safely resolve that message. Could you rephrase or add a little more context?",
        )

    if not isinstance(payload, dict):
        payload = {}
    status = str(payload.get("status", "")).strip().lower()
    question = str(payload.get("clarification_question") or "").strip()
    answer = str(payload.get("answer") or payload.get("reply") or "").strip()

    if status in {"needs_clarification", "clarify", "ambiguous"}:
        return ExpansionDecision(
            expanded_query=original_message,
            needs_clarification=True,
            clarification_question=question or "Could you clarify what you mean?",
        )

    intent_preserved = payload.get("intent_preserved", True)
    unsupported_details = payload.get("unsupported_details", False)
    intent_failed = intent_preserved is False or str(intent_preserved).strip().lower() == "false"
    details_unsupported = unsupported_details is True or str(unsupported_details).strip().lower() == "true"
    if intent_failed or details_unsupported:
        return ExpansionDecision(
            expanded_query=original_message,
            needs_clarification=True,
            clarification_question=question or "I couldn’t verify that a rewrite preserves your meaning. Could you clarify or rephrase it?",
        )

    expanded = payload.get("expanded_query") or payload.get("query")
    if status and status not in {"ready", "complete", "success"}:
        expanded = None
    if not isinstance(expanded, str) or not expanded.strip():
        return ExpansionDecision(
            expanded_query=original_message,
            needs_clarification=True,
            clarification_question="I couldn’t safely resolve that message. Could you rephrase or add a little more context?",
        )

    return ExpansionDecision(expanded_query=expanded.strip(), answer=answer)


def canonical_l1(label: str) -> Optional[str]:
    normalized = re.sub(r"[_\-\s]+", " ", str(label)).strip().casefold()
    return next((topic for topic in TOPIC_L2_BY_L1 if topic.casefold() == normalized), None)


def select_consistent_l2(
    l1_label: str, candidates: Iterable[Dict[str, Any]]
) -> Tuple[str, float]:
    """Choose the highest-scoring L2 candidate allowed by the chosen L1."""
    parent = canonical_l1(l1_label) or "General"
    allowed = {topic.casefold(): topic for topic in TOPIC_L2_BY_L1[parent]}
    valid = []
    for candidate in candidates:
        label = str(candidate.get("label", ""))
        normalized = re.sub(r"[_\-\s]+", " ", label).strip().casefold()
        if normalized in allowed:
            try:
                score = float(candidate.get("score", 0.0))
            except (TypeError, ValueError):
                score = 0.0
            valid.append((allowed[normalized], score))
    if valid:
        return max(valid, key=lambda item: item[1])

    # Keep the output hierarchy valid when a model returns unexpected labels.
    return TOPIC_L2_BY_L1[parent][0], 0.0
