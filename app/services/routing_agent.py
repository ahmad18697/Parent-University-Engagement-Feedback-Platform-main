from __future__ import annotations
from typing import Dict, Any
from langchain_core.runnables import RunnableLambda, RunnableParallel

from .sentiment import score_sentiment
from .categorizer import categorize, priority_from

# Nodes
_sentiment_node = RunnableLambda(lambda x: {"sent": score_sentiment(x["message"])})
_category_node  = RunnableLambda(lambda x: {"cat": categorize(x["message"])})

# Run in parallel
_parallel = RunnableParallel(**{"sent": _sentiment_node, "cat": _category_node})

def _combine(outputs: Dict[str, Any]) -> Dict[str, Any]:
    sent: Dict[str, Any] = outputs["sent"]["sent"]
    cat: Dict[str, Any]  = outputs["cat"]["cat"]

    sentiment_label = sent.get("label", "neutral")
    category = cat.get("category", "General")
    hits = int(cat.get("hits", 0))

    prio = priority_from(sentiment_label, hits, outputs.get("message", ""), category)

    return {
        "sentiment": sentiment_label,
        "sentiment_score": sent.get("score", 0.0),
        "sentiment_confidence": sent.get("confidence", 0.5),
        "category": category,
        "department": cat.get("department", "Student Affairs"),
        "priority": prio,
    }

_combine_node = RunnableLambda(_combine)

# Full chain
def _inject_message(x: Dict[str, Any]) -> Dict[str, Any]:
    out = _parallel.invoke(x)
    out["message"] = x.get("message", "")
    return out

_chain = RunnableLambda(_inject_message) | _combine_node

def run_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the heuristic agent on a payload dict
    """
    if "message" not in payload or not str(payload["message"]).strip():
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.0,
            "sentiment_confidence": 0.35,
            "category": "General",
            "department": "Student Affairs",
            "priority": "low",
        }
    return _chain.invoke(payload)