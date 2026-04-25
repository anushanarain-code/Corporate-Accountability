import streamlit as st
import re
import numpy as np
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Corporate Accountability Intelligence System", layout="wide")

# =========================
# HEADER
# =========================
st.title("🧾 Corporate Accountability Intelligence System")
st.caption("Evidence-based | Transparent | Advocacy-Oriented")

st.info("Evidence → Perception → Interpretation → Credibility → Decision → Advocacy")
st.warning("⚠️ Decision-support tool. Requires expert validation.")

# =========================
# CONTEXT
# =========================
st.sidebar.header("📍 Context")

company_name = st.sidebar.text_input("Company Name")

geography = st.sidebar.selectbox(
    "Geography",
    ["Global", "Europe", "North America", "Asia", "India", "Multiple regions", "Unknown"]
)

# =========================
# CASE STUDY MODE
# =========================
st.markdown("## 🧪 Case Study Demo Mode")

case = st.selectbox("Load Case Study", ["None", "Marriott International", "Nestlé"])

case_studies = {
    "Marriott International": """
Marriott International is committed to sourcing 100% cage-free eggs globally by 2025.

As of 2023, approximately 35% of our egg supply is cage-free globally. Progress varies by region due to supply constraints.

We engage with third-party auditors where feasible, but verification systems vary across markets.

We report annually through our Serve 360 sustainability platform.
""",

    "Nestlé": """
Nestlé is committed to improving animal welfare standards across its supply chain aligned with international guidelines.

Over 80% of key supply chains are compliant with our requirements as of 2023.

We conduct regular audits and publish annual sustainability reports with regional breakdowns.

Our goal is full compliance across sourcing regions by 2025.
"""
}

# =========================
# EVIDENCE LAYER
# =========================
st.markdown("## 📄 Evidence Layer")

if case != "None":
    report_text = case_studies[case]
    st.text_area("Loaded Case Study", report_text, height=200)
else:
    report_text = st.text_area("Paste sustainability report / policy excerpt", height=200)

external_text = st.text_area("Paste NGO / media input (optional)", height=150)

text = report_text.lower() if report_text else ""

# =========================
# SMART EXTRACTION
# =========================
st.markdown("## 🔍 Perception Layer (Smart Extraction)")

signals = {
    "commitment_strength": 1,
    "language_strength": 1,
    "timeline_clarity": 1,
    "geographic_scope": 1,
    "reported_progress": 1,
    "progress_vs_timeline": 1,
    "supply_chain_evidence": 1,
    "consistency_across_reports": 2,
    "reporting_frequency": 1,
    "data_granularity": 1,
    "third_party_verification": 0,
    "accessibility": 1
}

if report_text:

    if "100%" in text or "commit" in text:
        signals["commitment_strength"] = 3
        st.write("✔ Commitment detected: '100%' or 'commit'")

    years = re.findall(r'20\d{2}', text)
    if years:
        signals["timeline_clarity"] = 3

    percentages = re.findall(r'\d+%', text)
    if percentages:
        vals = [int(p.replace("%","")) for p in percentages]
        max_p = max(vals)

        if max_p >= 70:
            signals["reported_progress"] = 3
        elif max_p >= 40:
            signals["reported_progress"] = 2

    weak = ["aim", "aspire", "continue", "where feasible"]
    strong = ["achieved", "completed", "compliant"]

    if any(w in text for w in weak):
        signals["language_strength"] = 1

    if any(s in text for s in strong):
        signals["language_strength"] = 3

    if "audit" in text or "third-party" in text:
        signals["third_party_verification"] = 3

    if "region-specific" in text:
        signals["data_granularity"] = 3

    if "annually" in text:
        signals["reporting_frequency"] = 3

    if "however" in text or "constraints" in text:
        signals["consistency_across_reports"] = 1

# =========================
# SIGNAL OVERRIDE
# =========================
st.markdown("## ⚙️ Signal Override")

cols = st.columns(3)
for i, key in enumerate(signals.keys()):
    with cols[i % 3]:
        signals[key] = st.slider(key, 0, 3, signals[key])

# =========================
# SCORING ENGINE
# =========================
def compute_scores(data, geography):

    intent = sum([
        data["commitment_strength"],
        data["language_strength"],
        data["timeline_clarity"],
        data["geographic_scope"]
    ]) / 12 * 10

    execution = sum([
        data["reported_progress"],
        data["progress_vs_timeline"],
        data["supply_chain_evidence"],
        data["consistency_across_reports"]
    ]) / 12 * 10

    transparency = sum([
        data["reporting_frequency"],
        data["data_granularity"],
        data["third_party_verification"],
        data["accessibility"]
    ]) / 12 * 10

    # -------------------------
    # GEOGRAPHY MODIFIER
    # -------------------------
    geo_penalty = 0

    if geography in ["India", "Asia"]:
        geo_penalty = -0.5   # uncertainty penalty

    elif geography == "Global":
        geo_penalty = 0      # neutral

    elif geography == "Europe":
        geo_penalty = +0.5   # stronger regulatory context

    # apply ONLY to execution (not intent)
    execution = max(0, min(10, execution + geo_penalty))

    final = intent*0.3 + execution*0.4 + transparency*0.3

    return round(intent,1), round(execution,1), round(transparency,1), round(final,1)

intent, execution, transparency, final_score = compute_scores(signals, geography)

# =========================
# CREDIBILITY ENGINE
# =========================
def credibility_engine(signals):
    penalties = 0
    if signals["language_strength"] == 1:
        penalties += 1
    if signals["third_party_verification"] == 0:
        penalties += 1
    if signals["consistency_across_reports"] == 1:
        penalties += 1
    return max(0, 3 - penalties)

credibility = credibility_engine(signals)

# =========================
# EVIDENCE CONFIDENCE
# =========================
def evidence_confidence(text):
    if not text:
        return 0
    score = 0
    if len(text.split()) > 100:
        score += 1
    if "%" in text:
        score += 1
    if "audit" in text:
        score += 1
    return score

conf_score = evidence_confidence(report_text)

# =========================
# CONTRADICTION ENGINE
# =========================
def contradiction_engine(ext):
    if not ext:
        return 0
    ext = ext.lower()
    if any(w in ext for w in ["violation", "abuse", "failure", "investigation"]):
        return 2
    return 0

contradiction_score = contradiction_engine(external_text)

# =========================
# OVERCLAIMING RISK
# =========================
# =========================
# BAAMT ENGINE
# =========================
def baamt(intent, execution, transparency, credibility, overclaim_level):

    gap = intent - execution

    if overclaim_level == "High":
        return {
            "frame": "Credibility Breakdown",
            "narrative": "Public commitments significantly outpace credible execution.",
            "strategy": "High-pressure accountability campaign",
            "actions": [
                "Media exposure",
                "Reputation pressure",
                "Investor escalation",
                "Demand verified disclosures"
            ]
        }

    elif gap > 2:
        return {
            "frame": "Accountability Gap",
            "narrative": "Intent exists but execution is inconsistent.",
            "strategy": "Targeted engagement",
            "actions": [
                "Investor engagement",
                "Benchmark pressure",
                "Push time-bound targets",
                "Supply chain transparency"
            ]
        }

    elif credibility <= 1:
        return {
            "frame": "Verification Deficit",
            "narrative": "Claims lack strong verification or consistency.",
            "strategy": "Evidence-focused scrutiny",
            "actions": [
                "Push third-party audits",
                "Demand consistent reporting",
                "Highlight verification gaps"
            ]
        }

    else:
        return {
            "frame": "Reinforcement",
            "narrative": "Claims and execution are relatively aligned.",
            "strategy": "Support leadership",
            "actions": [
                "Highlight best practices",
                "Encourage scaling",
                "Policy alignment"
            ]
        }
overclaim_score = (
    (intent > execution + 2) +
    (credibility <= 1) +
    (conf_score <= 1) +
    contradiction_score
)

if overclaim_score >= 3:
    overclaim_level = "High"
elif overclaim_score == 2:
    overclaim_level = "Moderate"
else:
    overclaim_level = "Low"

# =========================
# BAAMT ENGINE
# =========================
def baamt(intent, execution, transparency, credibility, overclaim_level):

    gap = intent - execution

    # -------------------------
    # HIGH OVERCLAIM
    # -------------------------
    if overclaim_level == "High":

        narrative = "Public commitments significantly outpace credible execution, indicating reputational positioning without sufficient delivery."

        actions = [
            "Expose claim–reality gap through media",
            "Target brand reputation and consumer perception",
            "Leverage investor risk framing (ESG inconsistency)",
            "Push for verifiable disclosures"
        ]

        return {
            "frame": "Credibility Breakdown",
            "narrative": narrative,
            "strategy": "High-pressure accountability campaign",
            "actions": actions
        }

    # -------------------------
    # MODERATE GAP
    # -------------------------
    elif gap > 2:

        narrative = "Company demonstrates intent but lacks consistent execution, suggesting implementation bottlenecks."

        actions = [
            "Engage investors on execution risk",
            "Benchmark against industry leaders",
            "Demand time-bound milestones",
            "Push supply chain transparency"
        ]

        return {
            "frame": "Accountability Gap",
            "narrative": narrative,
            "strategy": "Targeted pressure + engagement",
            "actions": actions
        }

    # -------------------------
    # LOW GAP BUT LOW CREDIBILITY
    # -------------------------
    elif credibility <= 1:

        narrative = "Claims are not sufficiently backed by credible verification or consistent reporting."

        actions = [
            "Push for third-party audits",
            "Demand consistent reporting standards",
            "Highlight verification gaps publicly"
        ]

        return {
            "frame": "Verification Deficit",
            "narrative": narrative,
            "strategy": "Evidence-focused scrutiny",
            "actions": actions
        }

    # -------------------------
    # STRONG PERFORMANCE
    # -------------------------
    else:

        narrative = "Company demonstrates relatively aligned commitments and execution with credible disclosures."

        actions = [
            "Highlight as emerging best practice",
            "Encourage policy alignment",
            "Promote sector-wide adoption"
        ]

        return {
            "frame": "Reinforcement",
            "narrative": narrative,
            "strategy": "Support and scale leadership",
            "actions": actions
        }

baamt_output = baamt(intent, execution, transparency, credibility, overclaim_level)

# =========================
# RESULTS
# =========================
st.markdown("## 📊 Results")

st.metric("Intent", intent)
st.metric("Execution", execution)
st.metric("Transparency", transparency)
st.metric("Final Score", final_score)

st.write("Credibility:", credibility)
st.write("Evidence Confidence:", conf_score)
st.write("Overclaim Risk:", overclaim_level)

st.caption("Note: Execution score is adjusted for regional enforcement and reporting variability.")

st.markdown("## 🔎 Score Breakdown")
st.caption("Each category is scored out of 12 and scaled to a 10-point system.")

st.write("### Intent Calculation")
st.write({
    "commitment_strength": signals["commitment_strength"],
    "language_strength": signals["language_strength"],
    "timeline_clarity": signals["timeline_clarity"],
    "geographic_scope": signals["geographic_scope"]
})
st.write("→ Weighted to 10-point scale")

st.write("### Execution Calculation")
st.write({
    "reported_progress": signals["reported_progress"],
    "progress_vs_timeline": signals["progress_vs_timeline"],
    "supply_chain_evidence": signals["supply_chain_evidence"],
    "consistency_across_reports": signals["consistency_across_reports"]
})
st.write(f"→ Geography-adjusted: {execution}")

st.write("### Transparency Calculation")
st.write({
    "reporting_frequency": signals["reporting_frequency"],
    "data_granularity": signals["data_granularity"],
    "third_party_verification": signals["third_party_verification"],
    "accessibility": signals["accessibility"]
})

st.markdown("## ⚠️ Credibility Explanation")

if signals["language_strength"] == 1:
    st.write("- Weak/aspirational language reduces credibility")

if signals["third_party_verification"] == 0:
    st.write("- Lack of third-party verification")

if signals["consistency_across_reports"] == 1:
    st.write("- Inconsistency detected (e.g., constraints/limitations)")

st.markdown("## 🚨 Overclaim Risk Logic")

st.write("Intent vs Execution Gap:", round(intent - execution,2))
st.write("Credibility Score:", credibility)
st.write("Evidence Strength:", conf_score)
st.write("External Contradictions:", contradiction_score)

st.write("→ Overclaim risk increases when:")
st.write("- Intent significantly exceeds execution")
st.write("- Credibility is low")
st.write("- Evidence is weak")
st.write("- External contradictions exist")

# =========================
# BAAMT OUTPUT
# =========================
st.markdown("## 🧠 BAAMT Advocacy Layer")

st.write("**Frame:**", baamt_output["frame"])
st.write("**Narrative:**", baamt_output["narrative"])
st.write("**Strategy:**", baamt_output["strategy"])

st.write("**Recommended Actions:**")
for a in baamt_output["actions"]:
    st.write("-", a)

# =========================
# EXPLANATION LAYER
# =========================
if case != "None":
    st.markdown("## 🧠 Why this result?")

    st.write("- Signals extracted from disclosure text")
    st.write("- Weighted scoring across intent, execution, transparency")
    st.write("- Credibility penalties for weak verification or inconsistency")
    st.write("- Overclaiming detected via gaps + external contradictions")

# =========================
# VISUAL DASHBOARD
# =========================
st.markdown("## 📊 Visual Dashboard")

fig1 = go.Figure([
    go.Bar(x=["Intent","Execution","Transparency"], y=[intent,execution,transparency])
])
st.plotly_chart(fig1, use_container_width=True)

gap = intent - execution

fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=gap,
    title={'text': "Claim vs Execution Gap"},
    gauge={'axis': {'range': [0,10]}}
))
st.plotly_chart(fig2, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("© Anusha Narain | Ahimsa Fellowship (2025–26)")
