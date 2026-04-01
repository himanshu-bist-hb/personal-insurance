import streamlit as st

st.set_page_config(layout="wide")

# ─────────────────────────────────────────────
# CSS FIX (TOP SPACE + HEADER + LAYOUT)
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* 🔥 REMOVE ALL TOP WHITE SPACE */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Remove Streamlit header completely */
header, .stAppHeader {
    display: none !important;
}

/* Remove default body spacing */
html, body {
    margin: 0 !important;
    padding: 0 !important;
}

/* ───────── HEADER ───────── */
.nw-header {
    position: fixed;
    top: 0;
    left: 220px;   /* adjust if sidebar width changes */
    right: 0;
    height: 64px;
    background: #1A5DAB;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 30px;
    z-index: 9999;
}

/* Gold line */
.gold-line {
    position: fixed;
    top: 64px;
    left: 220px;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg,#C8A951,#EDD97A,transparent);
    z-index: 9999;
}

/* Push content below header */
.block-container {
    margin-top: 80px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* ───────── SIDEBAR ───────── */
[data-testid="stSidebar"] {
    background: #0D3F7A;
    width: 220px !important;
}

/* Sidebar text */
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
    st.radio("LOB", ["Business Auto", "General Liability", "Farm Auto"])

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="nw-header">
    <div>🦅 Nationwide Insurance</div>
    <div>BA · Analytics · Internal Tool</div>
</div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
col1, col2 = st.columns([3,1])

with col1:
    st.markdown("## Build Business Auto Rate Pages")
    st.write("Upload proposed ratebooks · Configure options · Generate output")

with col2:
    st.markdown("### Required Files")
    st.markdown("## 0/8")

st.divider()

# Example UI
left, right = st.columns([2,1])

with left:
    st.subheader("Upload Ratebooks")
    st.file_uploader("Upload Excel", type=["xlsx","xlsm"])

with right:
    st.subheader("Configuration")
    st.text_input("Save Path")
    st.number_input("Schedule Mod", 0, 100, 0)

st.button("Create Rate Pages")