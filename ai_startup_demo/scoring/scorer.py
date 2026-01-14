from .weights import WEIGHTS

def normalize(value, min_val, max_val):
    return max(0, min(1, (value - min_val) / (max_val - min_val)))

def score_startup(startup):
    scores = {}

    scores["market_opportunity"] = normalize(
        startup["market_size_musd"], 50, 5000
    )

    scores["business_viability"] = normalize(
        startup["revenue_model_strength"], 1, 5
    )

    scores["technology_maturity"] = normalize(
        startup["technology_readiness"], 1, 5
    )

    scores["team_execution"] = normalize(
        startup["team_experience"], 1, 5
    )

    scores["strategic_fit"] = normalize(
        startup["bmo_strategic_alignment"], 1, 5
    )

    scores["regulatory_risk"] = 1 - normalize(
        startup["regulatory_risk_level"], 1, 5
    )

    final_score = sum(
        scores[key] * WEIGHTS[key] for key in WEIGHTS
    )

    return round(final_score * 100, 2), scores