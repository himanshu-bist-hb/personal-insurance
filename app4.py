import streamlit as st
from pathlib import Path
import tempfile, os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* GLOBAL */
body {
    background-color: #f7f9fc;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #eef2f7;
    border-right: 1px solid #e0e3e6;
}

/* TITLE */
.main-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 5px;
}
.sub-title {
    color: #6b7280;
    font-size: 14px;
}

/* CARD */
.card {
    background: #f2f4f7;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border: 1px solid #e0e3e6;
}
.card:hover {
    background: #e8f0ff;
    border: 1px solid #003e83;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg,#003e83,#1d56a4);
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 50px;
    font-size: 16px;
}

/* RIGHT PANEL */
.panel {
    background: #f2f4f7;
    padding: 20px;
    border-radius: 12px;
}

/* PROGRESS */
.progress-bar {
    height: 6px;
    background: #e0e3e6;
    border-radius: 10px;
}
.progress-fill {
    height: 6px;
    background: #003e83;
    width: 45%;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
st.sidebar.markdown("### Insurance Categories")

lob = st.sidebar.radio(
    "",
    ["Business Auto", "General Liability", "Farm Auto", "Property"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Support")
st.sidebar.caption("Documentation")


# ---------------- HEADER ----------------
st.markdown('<div class="main-title">Business Auto Ratebooks</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Transforming uploaded ratebook data into standardized customer-facing rate pages.</div>', unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
left, right = st.columns([3,1])

# ================= LEFT =================
with left:
    st.markdown("##### MANDATORY RATEBOOK UPLOADS")

    cols = st.columns(3)

    def upload_card(title, key):
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="font-size:14px;font-weight:600;">{title}</div>
            </div>
            """, unsafe_allow_html=True)
            return st.file_uploader("", key=key)

    with cols[0]:
        ngic = upload_card("Master Ratebook", "NGIC")
        class_factors = upload_card("Class Factors", "NICOF")

    with cols[1]:
        mm = upload_card("State Exceptions", "MM")
        liability = upload_card("Liability Rates", "HICNJ")

    with cols[2]:
        naco = upload_card("Territory Codes", "NACO")
        damage = upload_card("Physical Damage", "CCMIC")

    # OPTIONAL
    st.markdown("##### OPTIONAL SUPPLEMENTS")

    col1, col2 = st.columns(2)
    with col1:
        uw = st.file_uploader("Underwriting Guide")
    with col2:
        cw = st.file_uploader("Historical Delta")

    # BUTTON
    st.markdown("###")
    run = st.button("🚀 Create Rate Pages", use_container_width=True)


# ================= RIGHT =================
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### ⚙️ Ratebook Parameters")

    sched = st.number_input("Schedule Rating %", 0, 100, 0)
    st.slider("", 0, 100, sched)

    save_dir = st.text_input("Save Location", "/outputs/rate-pages/")

    st.markdown("---")

    st.markdown("### PROCESS STATUS")

    st.markdown("**Data Transformation** 45%")
    st.markdown('<div class="progress-bar"><div class="progress-fill"></div></div>', unsafe_allow_html=True)

    st.markdown("""
    **Step 2: Mapping Rows**  
    *Normalizing OHIO_AUTO_V2...*
    """)

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- BACKEND ----------------
if run:
    st.success("Running... (connect your backend here)")