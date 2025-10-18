from __future__ import annotations
from typing import Dict, List, Tuple
import re
from difflib import get_close_matches

DEFAULT_DEPARTMENT = "Student Affairs"

# Canonical keyword dictionary
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Hostel": [
        "hostel", "dorm", "room", "warden", "mess", "canteen", "mess food",
        "hygiene", "hygine", "clean", "unclean", "dirty", "water", "electricity",
        "wifi", "wifi issue", "noise"
    ],
    "Academics": [
        "exam", "lecture", "professor", "syllabus", "grade", "assignment",
        "class", "course", "curriculum", "study", "studying", "studing",
        "attendance", "lab", "project"
    ],
    "Finance": ["fee", "fees", "scholarship", "refund", "payment", "invoice", "finance", "bank"],
    "Transport": ["bus", "transport", "parking", "shuttle"],
    "Health": ["hospital", "clinic", "medical", "health", "doctor", "vaccination", "insurance"],
    "Counselling": ["counsel", "counselling", "mental", "stress", "bully", "harass"],
    "IT Support": ["portal", "login", "password", "server", "email", "it", "software", "network"],
}

# Words indicating urgency or severity
URGENCY_WORDS = {"urgent", "immediately", "asap", "unsafe", "emergency", "harass", "bully", "no water", "power cut"}

def _tokens(text: str) -> List[str]:
    t = re.sub(r"[^a-zA-Z0-9\s]", " ", (text or "").lower())
    return [w for w in t.split() if w]

def _approx_hit(word: str, vocab: List[str]) -> bool:
    """Return True if word is in vocab or close enough (typos)."""
    if word in vocab:
        return True
    close = get_close_matches(word, vocab, n=1, cutoff=0.83)
    return bool(close)

def categorize(text: str) -> Dict[str, str | int]:
    """
    Returns: {"category","department","hits"}
    """
    words = _tokens(text)
    joined = " ".join(words)

    best_cat: str | None = None
    best_hits = 0

    for cat, vocab in CATEGORY_KEYWORDS.items():
        hits = 0

        # phrase hits
        for phrase in [v for v in vocab if " " in v]:
            if phrase in joined:
                hits += 2

        # token hits (with fuzzy)
        for w in words:
            if _approx_hit(w, [v for v in vocab if " " not in v]):
                hits += 1

        if hits > best_hits:
            best_hits, best_cat = hits, cat

    if not best_cat:
        best_cat = "General"

    department = best_cat if best_cat in CATEGORY_KEYWORDS else DEFAULT_DEPARTMENT

    return {"category": best_cat, "department": department, "hits": int(best_hits)}

def priority_from(sentiment_label: str, hits: int, text: str, category: str) -> str:
    """
    Heuristic priority:
    """
    t = " " + (text or "").lower() + " "
    has_urgency = any(k in t for k in URGENCY_WORDS)

    if has_urgency:
        return "high"

    if sentiment_label == "negative":
        if category in {"Health", "Counselling"}:
            return "high"
        if hits >= 2:
            return "high"
        return "medium"

    if category != "General" and hits >= 1:
        return "medium"

    return "low"