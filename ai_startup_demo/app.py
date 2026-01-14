import streamlit as st
import pandas as pd
from scoring.scorer import score_startup
from scoring.nlp import infer_startup_values_from_text, strategic_language_score

# -------------------- Session State for Dashboard --------------------
if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = []

# -------------------- App Header --------------------
st.title("BMO AI Startup Intake & Prioritization System")
st.subheader("Startup Submission")

# -------------------- Mode Selection --------------------
mode = st.radio("Select Mode", ["Manual Input", "AI Auto-Score"])

# -------------------- Manual Input Mode --------------------
if mode == "Manual Input":
    market_size = st.slider("Market Size (USD Millions)", 50, 5000, 500)
    revenue = st.slider("Revenue Model Strength", 1, 5, 3)
    tech = st.slider("Technology Readiness", 1, 5, 3)
    team = st.slider("Team Execution Capability", 1, 5, 3)
    risk = st.slider("Regulatory Risk (Lower is Better)", 1, 5, 2)
    fit = st.slider("Strategic Alignment with BMO", 1, 5, 4)

    description = st.text_area("Startup Description / Pitch")

    if st.button("Evaluate Startup"):
        startup = {
            "market_size_musd": market_size,
            "revenue_model_strength": revenue,
            "technology_readiness": tech,
            "team_experience": team,
            "regulatory_risk_level": risk,
            "bmo_strategic_alignment": fit
        }

        score, breakdown = score_startup(startup)

        if description.strip() != "":
            breakdown["bmo_strategic_alignment"] = (
                breakdown.get("bmo_strategic_alignment", 0) * 0.7 +
                strategic_language_score(description) * 0.3
            )

        st.metric("Overall Priority Score", score)
        st.subheader("Decision Breakdown")
        st.json(breakdown)

        # Fast-Track / Review / Reject label
        if score > 80:
            st.success("Fast-Track ✅")
        elif score > 60:
            st.warning("Review ⚠️")
        else:
            st.error("Reject ❌")

        # Append to Manager Dashboard
        st.session_state.dashboard_data.append({
            "Idea": description if description.strip() else "Manual Input Idea",
            "Score": score,
            "Market": breakdown.get("market_size_musd", 0),
            "Tech": breakdown.get("technology_readiness", 0),
            "Team": breakdown.get("team_experience", 0),
            "Risk": breakdown.get("regulatory_risk_level", 0),
            "Fit": breakdown.get("bmo_strategic_alignment", 0),
            "Revenue": breakdown.get("revenue_model_strength", 0)
        })

# -------------------- AI Auto-Score Mode --------------------
if mode == "AI Auto-Score":
    idea_text = st.text_area("Enter Startup Idea / Pitch")

    if st.button("Evaluate Automatically"):
        if idea_text.strip() != "":
            # 1️⃣ Infer numeric category values from AI
            startup_categories = infer_startup_values_from_text(idea_text)

            # DEBUG: check what AI returned
            st.write("DEBUG: AI inferred category values:", startup_categories)

            # Ensure all keys exist
            defaults = {
                "market_size_musd": 0,
                "technology_readiness": 0,
                "team_experience": 0,
                "regulatory_risk_level": 0,
                "bmo_strategic_alignment": 0,
                "revenue_model_strength": 0
            }
            for key in defaults:
                if key not in startup_categories or startup_categories[key] is None:
                    startup_categories[key] = defaults[key]

            # 2️⃣ Calculate total score
            score, breakdown = score_startup(startup_categories)

            # 3️⃣ Optional: adjust strategic fit using NLP
            fit_score = startup_categories.get("bmo_strategic_alignment", 0)
            breakdown["bmo_strategic_alignment"] = fit_score * 0.7 + strategic_language_score(idea_text) * 0.3

            # 4️⃣ Display overall score and breakdown
            st.metric("Overall Priority Score", score)
            st.subheader("Decision Breakdown")
            st.json(breakdown)

            # 5️⃣ Fast-Track / Review / Reject
            if score > 80:
                st.success("Fast-Track ✅")
            elif score > 60:
                st.warning("Review ⚠️")
            else:
                st.error("Reject ❌")

            # 6️⃣ Append to Manager Dashboard
            st.session_state.dashboard_data.append({
                "Idea": idea_text,
                "Score": score,
                "Market": breakdown.get("market_size_musd", 0),
                "Tech": breakdown.get("technology_readiness", 0),
                "Team": breakdown.get("team_experience", 0),
                "Risk": breakdown.get("regulatory_risk_level", 0),
                "Fit": breakdown.get("bmo_strategic_alignment", 0),
                "Revenue": breakdown.get("revenue_model_strength", 0)
            })

        else:
            st.warning("Please enter a startup idea")

# -------------------- Manager Dashboard --------------------
st.markdown("---")
st.header("Manager Dashboard (Summary of Evaluations)")

# Build the dashboard table dynamically from session state
df = pd.DataFrame(st.session_state.dashboard_data, columns=[
    "Idea", "Score", "Market", "Tech", "Team", "Risk", "Fit", "Revenue"
])

st.subheader("Top Startups Ranked by Priority Score")

# Highlight Fast-Track / Review / Reject with colors
def color_score(val):
    if val > 80:
        return 'background-color: #d4edda'  # green
    elif val > 60:
        return 'background-color: #1f4e79; color: white'  # blue for Review
    else:
        return 'background-color: #f8d7da'  # red

if not df.empty:
    # Apply coloring only to Score column
    styled_df = df.style.applymap(color_score, subset=["Score"])
    st.dataframe(styled_df)
else:
    st.dataframe(df)