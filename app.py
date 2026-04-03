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
# SCORING FUNCTION (NEW FIX)
# -----------------------------
def compute_scores(data, geography):
    c = (data["commitment_strength"] + data["language_strength"] +
         data["timeline_clarity"] + data["geographic_scope"]) / 12 * 10

    i = (data["reported_progress"] + data["progress_vs_timeline"] +
         data["supply_chain_evidence"] + data["consistency_across_reports"]) / 12 * 10

    t = (data["reporting_frequency"] + data["data_granularity"] +
         data["third_party_verification"] + data["accessibility"]) / 12 * 10

    geo_modifier = 0
    if geography in ["India", "Asia"]:
        geo_modifier = -0.5
    elif geography == "Global":
        geo_modifier = 0.5
    elif geography == "Europe":
        geo_modifier = 1

    i = max(0, min(10, i + geo_modifier))

    final = c*0.3 + i*0.4 + t*0.3

    return round(c,1), round(i,1), round(t,1), round(final,1)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Company Input")

company_name = st.sidebar.text_input("Company Name")

geography = st.sidebar.selectbox(
    "Geography",
    ["Global", "Europe", "North America", "Asia", "India", "Multiple regions", "Unknown"]
)

selected_case = st.sidebar.selectbox("Load Case Study", list(case_studies.keys()))
compare_case = st.sidebar.selectbox("Compare With", list(case_studies.keys()))

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
# CURRENT COMPANY SCORE
# -----------------------------
current_data = {
    "commitment_strength": commitment_strength,
    "language_strength": language_strength,
    "timeline_clarity": timeline_clarity,
    "geographic_scope": geographic_scope,
    "reported_progress": reported_progress,
    "progress_vs_timeline": progress_vs_timeline,
    "supply_chain_evidence": supply_chain_evidence,
    "consistency_across_reports": consistency_across_reports,
    "reporting_frequency": reporting_frequency,
    "data_granularity": data_granularity,
    "third_party_verification": third_party_verification,
    "accessibility": accessibility
}

c_score, i_score, t_score, final_score = compute_scores(current_data, geography)

# -----------------------------
# UI
# -----------------------------
st.subheader(f"Results for: {company_name or selected_case}")

col1, col2, col3 = st.columns(3)
col1.metric("Commitment", c_score)
col2.metric("Implementation", i_score)
col3.metric("Transparency", t_score)

st.metric("Final Score", final_score)

# -----------------------------
# COMPARISON (FIXED)
# -----------------------------
if compare_case != "None":
    st.header("🔄 Comparison Analysis")

    comp_data = case_studies[compare_case]
    c2, i2, t2, f2 = compute_scores(comp_data, geography)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Current")
        st.write(f"Final Score: {final_score}")

    with col2:
        st.subheader(compare_case)
        st.write(f"Final Score: {f2}")

    st.subheader("📊 Difference")

    st.write(f"Commitment Gap: {round(c_score - c2,1)}")
    st.write(f"Implementation Gap: {round(i_score - i2,1)}")
    st.write(f"Transparency Gap: {round(t_score - t2,1)}")

    if final_score > f2:
        st.success("Current company performs better overall.")
    else:
        st.warning(f"{compare_case} performs better overall.")

# -----------------------------
# REPORT
# -----------------------------
report = f"""
CORPORATE ACCOUNTABILITY REPORT

Developed by: Anusha Narain | Ahimsa Fellowship (2025–26)

Company: {company_name or "Sample"}
Geography: {geography}

Final Score: {final_score}
"""

st.download_button("📥 Download Report", report, file_name="report.txt")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("© Anusha Narain | Ahimsa Fellowship (2025–26)")