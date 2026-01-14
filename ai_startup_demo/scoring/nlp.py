import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

BMO_KEYWORDS = [
    "bank", "fintech", "ai", "risk",
    "compliance", "payments", "fraud",
    "lending", "wealth", "capital markets"
]
def strategic_language_score(text):
    vectorizer = TfidfVectorizer(vocabulary=BMO_KEYWORDS)
    tfidf = vectorizer.fit_transform([text]).toarray()[0]
    return np.mean(tfidf)


def infer_startup_values_from_text(text):
    text = text.lower()

    # Default values
    market = 500  # Market size in million USD
    revenue = 3  # Revenue model strength 1-5
    tech = 3  # Technology readiness 1-5
    team = 3  # Team experience 1-5
    risk = 3  # Regulatory risk 1-5 (lower is better)
    fit = 3  # Strategic alignment 1-5

    # Adjust values based on keywords
    if "large market" in text or "millions" in text:
        market = 3000
    elif "small market" in text:
        market = 100

    if "ai" in text or "machine learning" in text or "fintech" in text:
        tech = 5
    elif "prototype" in text:
        tech = 2

    if "experienced team" in text or "founder with track record" in text:
        team = 5
    elif "new team" in text:
        team = 2

    if "compliance" in text or "regulation" in text:
        risk = 2
    elif "uncertain market" in text or "risky" in text:
        risk = 5

    if "bank" in text or "bmo" in text or "aligns with bank" in text:
        fit = 5

    if "subscription" in text or "recurring revenue" in text:
        revenue = 5
    elif "ad-supported" in text:
        revenue = 3

    return {
        "market_size_musd": market,
        "revenue_model_strength": revenue,
        "technology_readiness": tech,
        "team_experience": team,
        "regulatory_risk_level": risk,
        "bmo_strategic_alignment": fit
    }