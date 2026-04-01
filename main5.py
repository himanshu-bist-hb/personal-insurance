import streamlit as st

st.set_page_config(layout="wide")

# ─────────────────────────────────────────────
# CSS (FINAL PERFECT FIX)
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* REMOVE TOP WHITE SPACE */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

header, .stAppHeader {
    display: none !important;
}

html, body {
    margin: 0 !important;
    padding: 0 !important;
}

/* ───────── HEADER (FLUID - BEST APPROACH) ───────── */
.nw-header {
    position: sticky;
    top: 0;
    width: 100%;
    height: 64px;
    background: #1A5DAB;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    z-index: 999;
}

/* GOLD LINE */
.gold-line {
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg,#C8A951,#EDD97A,transparent);
    margin-bottom: 20px;
}

/* CONTENT */
.block-container {
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #0D3F7A;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Nationwide Insurance")
    st.write("BA Analytics Platform")
    st.radio("Line of Business", [
        "Business Auto",
        "General Liability",
        "Farm Auto",
        "Property"
    ])

# ─────────────────────────────────────────────
# HEADER (NOW PERFECTLY ALIGNED)
# ─────────────────────────────────────────────
st.markdown("""
<div class="nw-header">
    <div>🦅 Nationwide Insurance</div>
    <div>BA · Analytics · Internal Tool</div>
</div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────────
col1, col2 = st.columns([3,1])

with col1:
    st.markdown("## Build Business Auto Rate Pages")
    st.write("Upload proposed ratebooks · Configure options · Generate output")

with col2:
    st.markdown("### Required Files")
    st.markdown("## 0/8")

st.divider()

left, right = st.columns([2,1])

with left:
    st.subheader("Upload Ratebooks")
    st.file_uploader("Upload Excel", type=["xlsx", "xlsm"])

with right:
    st.subheader("Configuration")
    st.text_input("Save Path")
    st.number_input("Schedule Mod", 0, 100, 0)

st.button("Create Rate Pages")