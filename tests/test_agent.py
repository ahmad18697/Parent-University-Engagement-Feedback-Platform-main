from app.services.sentiment import score_sentiment
from app.services.categorizer import categorize, priority_from
from app.services.routing_agent import run_agent

def test_sentiment_posneg():
    assert score_sentiment("This is great and helpful")["label"] == "positive"
    assert score_sentiment("This is terrible and dirty")["label"] == "negative"

def test_categorize():
    c = categorize("The hostel hygiene is poor and water is leaking")
    assert c["category"] == "Hostel"
    assert c["hits"] >= 1

def test_agent():
    out = run_agent({"message": "Exam schedule is delayed and confusing"})
    assert out["category"] in {"Academics", "General"}
    assert out["sentiment"] in {"negative","neutral","positive"}
    assert out["priority"] in {"low","medium","high"}
