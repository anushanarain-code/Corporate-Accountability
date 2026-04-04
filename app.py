import streamlit as st
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Corporate Accountability Tool", layout="wide")

# -----------------------------
# TITLE + CREDIT
# -----------------------------
st.title("🧾 Corporate Accountability Tool")
st.caption("Developed by Anusha Narain | Ahimsa Fellowship (2025–26)")

st.info("This tool helps identify which companies need advocacy pressure and what kind of campaign is most effective.")

# -----------------------------
# CASE STUDIES
# -----------------------------
case_studies = {
    "None": {},
    "Sodexo": {
        "commitment_strength": 3, "language_strength": 2, "timeline_clarity": 3, "geographic_scope": 2,
        "reported_progress": 2, "progress_vs_timeline": 2, "supply_chain_evidence": 1, "consistency_across_reports": 2,
        "reporting_frequency": 2, "data_granularity": 1, "third_party_verification": 1, "accessibility": 2
    },
    "Marriott": {
        "commitment_strength": 2, "language_strength": 1, "timeline_clarity": 1, "geographic_scope": 2,
        "reported_progress": 1, "progress_vs_timeline": 1, "supply_chain_evidence": 1, "consistency_across_reports": 1,
        "reporting_frequency": 1, "data_granularity": 1, "third_party_verification": 0, "accessibility": 1
    },
    "Nestlé": {
        "commitment_strength": 3, "language_strength": 3, "timeline_clarity": 3, "geographic_scope": 3,
        "reported_progress": 2, "progress_vs_timeline": 2, "supply_chain_evidence": 2, "consistency_across_reports": 2,
        "reporting_frequency": 3, "data_granularity": 2, "third_party_verification": 2, "accessibility": 3
    }
}

# -----------------------------
# SIDEBAR INPUT
# -----------------------------
st.sidebar.header("Company Input")

company_name = st.sidebar.text_input("Company Name")

geography = st.sidebar.selectbox(
    "Geography",
    ["Global", "Europe", "North America", "Asia", "India", "Multiple regions", "Unknown"]
)

selected_case = st.sidebar.selectbox("Load Case Study", list(case_studies.keys()))
default = case_studies[selected_case]

def val(key):
    return default.get(key, 1)

# -----------------------------
# INPUTS
# -----------------------------
with st.sidebar.expander("Commitment"):
    commitment_strength = st.slider("Commitment Strength", 0, 3, val("commitment_strength"))
    language_strength = st.slider("Language Strength", 0, 3, val("language_strength"))
    timeline_clarity = st.slider("Timeline Clarity", 0, 3, val("timeline_clarity"))
    geographic_scope = st.slider("Geographic Scope", 0, 3, val("geographic_scope"))

with st.sidebar.expander("Implementation"):
    reported_progress = st.slider("Reported Progress", 0, 3, val("reported_progress"))
    progress_vs_timeline = st.slider("Progress vs Timeline", 0, 3, val("progress_vs_timeline"))
    supply_chain_evidence = st.slider("Supply Chain Evidence", 0, 3, val("supply_chain_evidence"))
    consistency_across_reports = st.slider("Consistency Across Reports", 0, 3, val("consistency_across_reports"))

with st.sidebar.expander("Transparency"):
    reporting_frequency = st.slider("Reporting Frequency", 0, 3, val("reporting_frequency"))
    data_granularity = st.slider("Data Granularity", 0, 3, val("data_granularity"))
    third_party_verification = st.slider("Third-Party Verification", 0, 3, val("third_party_verification"))
    accessibility = st.slider("Accessibility", 0, 3, val("accessibility"))

# -----------------------------
# CALCULATIONS
# -----------------------------
commitment_score = (commitment_strength + language_strength + timeline_clarity + geographic_scope)/12*10
implementation_score = (reported_progress + progress_vs_timeline + supply_chain_evidence + consistency_across_reports)/12*10
transparency_score = (reporting_frequency + data_granularity + third_party_verification + accessibility)/12*10

# Geo modifier
geo_modifier = 0
if geography in ["India", "Asia"]:
    geo_modifier = -0.5
elif geography == "Global":
    geo_modifier = 0.5
elif geography == "Europe":
    geo_modifier = 1

implementation_score = max(0, min(10, implementation_score + geo_modifier))

final_score = commitment_score*0.3 + implementation_score*0.4 + transparency_score*0.3

credibility_gap = commitment_score - implementation_score
transparency_deficit = 10 - transparency_score

# -----------------------------
# RISK LOGIC
# -----------------------------
if commitment_score >= 7 and implementation_score <= 4:
    risk = "High Greenwashing Risk"
elif final_score < 4:
    risk = "High Risk"
elif final_score < 7:
    risk = "Moderate Risk"
else:
    risk = "Low Risk"

# Strategy
if transparency_score < 4:
    priority = "Increase transparency and disclosure pressure"
elif implementation_score < 5:
    priority = "Investigate supply chain implementation"
else:
    priority = "Monitor and maintain engagement"

# -----------------------------
# UI RESULTS
# -----------------------------
st.subheader(f"Results for: {company_name or selected_case}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Commitment", f"{commitment_score:.1f}")
col2.metric("Implementation", f"{implementation_score:.1f}")
col3.metric("Transparency", f"{transparency_score:.1f}")
col4.metric("Final Score", f"{final_score:.1f}")

# -----------------------------
# INSIGHTS (NEW)
# -----------------------------
st.markdown("### 🔍 Key Insights")

st.write(f"""
**Risk Level:** {risk}  

**Credibility Gap:** {credibility_gap:.1f}  
→ Difference between commitment and actual implementation  

**Transparency Deficit:** {transparency_deficit:.1f}  
→ Indicates how much information is missing or unclear  
""")

# -----------------------------
# STRATEGIC INTERPRETATION (NEW)
# -----------------------------
st.markdown("### 🧠 Strategic Interpretation")

if credibility_gap > 2:
    insight = "Significant gap between commitments and execution. High potential for accountability-focused campaigns."
elif transparency_deficit > 3:
    insight = "Limited disclosure creates an opportunity for transparency-driven pressure."
else:
    insight = "Company appears relatively aligned, focus should be on monitoring and incremental pressure."

st.write(insight)

# -----------------------------
# ADVOCACY RECOMMENDATION (NEW)
# -----------------------------
st.markdown("### 📣 Advocacy Recommendation")

st.write(f"""
**Primary Action:** {priority}  

This company should be targeted through:
- Strategic engagement where possible  
- Escalation if progress remains unclear  
""")

# -----------------------------
# REPORT
# -----------------------------
report = f"""
CORPORATE ACCOUNTABILITY REPORT

Developed by: Anusha Narain | Ahimsa Fellowship (2025–26)

Company: {company_name or "Sample"}
Geography: {geography}

Final Score: {final_score:.1f}
Risk: {risk}

Credibility Gap: {credibility_gap:.1f}
Transparency Deficit: {transparency_deficit:.1f}

Priority Action: {priority}
"""

st.download_button("📥 Download Report", report, file_name="report.txt")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("© Anusha Narain | Ahimsa Fellowship (2025–26)")
