from __future__ import annotations
from typing import Dict
import re

# Try TextBlob; fall back gracefully if not installed
try:
    from textblob import TextBlob
    _HAS_TEXTBLOB = True
except Exception:
    _HAS_TEXTBLOB = False

# Lightweight keyword lexicon
NEG_CUES = {
    "not good", "not studying", "not studing", "bad", "poor",
    "dirty", "smell", "smelly", "issue", "problem", "broken",
    "delay", "late", "bully", "harass", "unsafe", "hygine", "hygiene",
    "no water", "water issue", "no wifi", "wifi issue",
}
POS_CUES = {"excellent", "very good", "good", "great", "thanks", "thank you", "helpful"}

def _rule_polarity(text: str) -> float:
    """Very small rule scorer for very short or typo'd texts."""
    t = " " + re.sub(r"\s+", " ", text.lower()).strip() + " "
    score = 0.0
    for k in POS_CUES:
        if k in t:
            score += 0.6
    for k in NEG_CUES:
        if k in t:
            score -= 0.8
    # Flip if negation patterns present
    if " not " in t and any(p in t for p in [" good", " fine", " ok", " studying", " working"]):
        score -= 0.5
    return max(-1.0, min(1.0, score))

def score_sentiment(text: str) -> Dict[str, float | str]:
    """
    Returns: {label, score, confidence}
    """
    text = (text or "").strip()
    score = 0.0
    conf = 0.35  # base

    # Rule score first
    r = _rule_polarity(text)
    score += r
    conf = max(conf, 0.55 if abs(r) >= 0.4 else 0.35)

    # Blend with TextBlob if available
    if _HAS_TEXTBLOB and text:
        try:
            tb = TextBlob(text)
            tb_score = float(tb.sentiment.polarity or 0.0)
            # weighted blend
            w_tb = 0.6 if len(text) >= 25 else 0.4
            score = (1 - w_tb) * score + w_tb * tb_score
            conf = max(conf, 0.6 if abs(tb_score) > 0.25 else conf)
        except Exception:
            pass

    label = "neutral"
    if score > 0.1:
        label = "positive"
    elif score < -0.1:
        label = "negative"

    return {"label": label, "score": round(score, 3), "confidence": round(conf, 3)}