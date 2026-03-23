# ba_rate_page_ui.py  –  Streamlit port of BARatePageUserInterface
# Run with:  streamlit run ba_rate_page_ui.py

import streamlit as st
import os
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BA Rate Page Builder",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Nationwide palette & custom CSS ──────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

  /* ── CSS Variables ── */
  :root {
    --nw-navy:      #003087;
    --nw-navy-dark: #001f5b;
    --nw-gold:      #D4A017;
    --nw-gold-lt:   #f0c84a;
    --nw-white:     #FFFFFF;
    --nw-off:       #F4F6FB;
    --nw-muted:     #8892A4;
    --nw-border:    #DDE3EF;
    --nw-success:   #1E7D45;
    --nw-danger:    #C0392B;
    --card-radius:  14px;
    --shadow:       0 4px 24px rgba(0,48,135,0.10);
  }

  /* ── Reset Streamlit chrome ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: var(--nw-off) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1a2340 !important;
  }

  /* Hide hamburger / footer */
  #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

  /* ── Top banner ── */
  .nw-banner {
    background: linear-gradient(135deg, var(--nw-navy-dark) 0%, var(--nw-navy) 60%, #1a4aad 100%);
    border-radius: var(--card-radius);
    padding: 38px 44px 32px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
  }
  .nw-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(212,160,23,0.18) 0%, transparent 70%);
    border-radius: 50%;
  }
  .nw-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
  }
  .nw-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 11px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--nw-gold);
    margin-bottom: 10px;
  }
  .nw-title {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 8px;
    line-height: 1.15;
  }
  .nw-subtitle {
    font-size: 14px;
    font-weight: 300;
    color: rgba(255,255,255,0.72);
    margin: 0;
  }
  .nw-logo-mark {
    position: absolute;
    top: 28px; right: 40px;
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    color: var(--nw-gold);
    letter-spacing: 1px;
    opacity: 0.9;
  }

  /* ── Cards ── */
  .nw-card {
    background: var(--nw-white);
    border-radius: var(--card-radius);
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
    border: 1px solid var(--nw-border);
  }
  .nw-card-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--nw-navy);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .nw-card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--nw-border);
  }

  /* ── File pill grid ── */
  .pill-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 4px;
  }
  .pill-item {
    background: var(--nw-off);
    border: 1.5px dashed var(--nw-border);
    border-radius: 10px;
    padding: 12px 14px;
    cursor: pointer;
    transition: all 0.18s ease;
    text-align: left;
  }
  .pill-item:hover {
    border-color: var(--nw-navy);
    background: #EEF2FF;
  }
  .pill-item.loaded {
    background: #EAF4EE;
    border-color: var(--nw-success);
    border-style: solid;
  }
  .pill-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--nw-muted);
    margin-bottom: 4px;
  }
  .pill-value {
    font-size: 12px;
    font-weight: 400;
    color: #1a2340;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .pill-value.empty { color: var(--nw-muted); }

  /* ── Misc inputs ── */
  .nw-input-row {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  /* ── Status badge ── */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
  }
  .status-ready    { background: #EEF2FF; color: var(--nw-navy); }
  .status-running  { background: #FFF8E1; color: #7B5800; }
  .status-success  { background: #EAF4EE; color: var(--nw-success); }
  .status-error    { background: #FDECEA; color: var(--nw-danger); }

  /* ── Primary button override ── */
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--nw-navy) 0%, #1a4aad 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 12px 36px !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 16px rgba(0,48,135,0.25) !important;
    transition: all 0.2s !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--nw-navy-dark) 0%, var(--nw-navy) 100%) !important;
    box-shadow: 0 6px 22px rgba(0,48,135,0.35) !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--nw-navy) !important;
    border: 1.5px solid var(--nw-navy) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
  }

  /* ── Streamlit number_input / text_input ── */
  [data-testid="stNumberInput"] input,
  [data-testid="stTextInput"]   input {
    border: 1.5px solid var(--nw-border) !important;
    border-radius: 8px !important;
    background: var(--nw-off) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
  }
  [data-testid="stNumberInput"] input:focus,
  [data-testid="stTextInput"]   input:focus {
    border-color: var(--nw-navy) !important;
    box-shadow: 0 0 0 3px rgba(0,48,135,0.12) !important;
  }

  /* ── Expander (file upload panel) ── */
  [data-testid="stExpander"] {
    border: 1.5px solid var(--nw-border) !important;
    border-radius: var(--card-radius) !important;
    background: var(--nw-white) !important;
    box-shadow: var(--shadow) !important;
    margin-bottom: 20px !important;
  }
  [data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--nw-navy) !important;
    padding: 18px 24px !important;
  }

  /* ── File uploader ── */
  [data-testid="stFileUploader"] {
    background: var(--nw-off) !important;
    border: 1.5px dashed var(--nw-border) !important;
    border-radius: 10px !important;
  }

  /* ── Divider ── */
  hr { border-color: var(--nw-border) !important; margin: 24px 0 !important; }

  /* ── Progress bar ── */
  [data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--nw-navy), #1a4aad) !important;
    border-radius: 4px !important;
  }

  /* ── Alert ── */
  [data-testid="stAlert"] { border-radius: 10px !important; }

  /* ── Small helper text ── */
  .helper-text {
    font-size: 11px;
    color: var(--nw-muted);
    margin-top: 4px;
  }

  /* ── Gold accent line ── */
  .gold-line {
    height: 3px;
    background: linear-gradient(90deg, var(--nw-gold), transparent);
    border-radius: 2px;
    margin: -4px 0 22px;
  }
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
RATEBOOK_KEYS = ["NGIC", "MM", "NACO", "NAFF", "NICOF", "HICNJ", "CCMIC", "NWAG"]
OPTIONAL_KEYS = ["CW"]
ALL_KEYS = RATEBOOK_KEYS + OPTIONAL_KEYS

for k in ALL_KEYS:
    if f"file_{k}" not in st.session_state:
        st.session_state[f"file_{k}"] = None
if "save_dir" not in st.session_state:
    st.session_state.save_dir = ""
if "status" not in st.session_state:
    st.session_state.status = "ready"
if "status_msg" not in st.session_state:
    st.session_state.status_msg = "Ready to build."


# ── Helper ───────────────────────────────────────────────────────────────────
def count_loaded():
    return sum(1 for k in ALL_KEYS if st.session_state[f"file_{k}"] is not None)

def short_name(f):
    return Path(f.name).name if f else None


# ── Banner ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nw-banner">
  <div class="nw-logo-mark">NATIONWIDE ✦</div>
  <div class="nw-eyebrow">Insurance · Analytics</div>
  <div class="nw-title">BA Rate Page Builder</div>
  <p class="nw-subtitle">Select proposed ratebooks, configure options, and generate rate pages in one click.</p>
</div>
""", unsafe_allow_html=True)


# ── File Upload Panel (collapsible) ──────────────────────────────────────────
loaded = count_loaded()
expand_label = f"📂  Ratebook Files  ·  {loaded} of {len(ALL_KEYS)} loaded"

with st.expander(expand_label, expanded=(loaded == 0)):
    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    # Required ratebooks – 2 columns
    st.markdown("**Required Ratebooks**")
    cols_a = st.columns(2)
    for i, key in enumerate(RATEBOOK_KEYS):
        with cols_a[i % 2]:
            uploaded = st.file_uploader(
                key,
                type=["xlsx", "xlsm", "xls"],
                key=f"uploader_{key}",
                label_visibility="visible",
            )
            if uploaded:
                st.session_state[f"file_{key}"] = uploaded
            if st.session_state[f"file_{key}"]:
                fname = short_name(st.session_state[f"file_{key}"])
                st.markdown(f'<p class="helper-text">✅ {fname}</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Optional CW
    st.markdown("**Optional Ratebook**")
    cw_upload = st.file_uploader(
        "CW – Commercial Workers (optional)",
        type=["xlsx", "xlsm", "xls"],
        key="uploader_CW",
        label_visibility="visible",
    )
    if cw_upload:
        st.session_state["file_CW"] = cw_upload
    if st.session_state["file_CW"]:
        st.markdown(f'<p class="helper-text">✅ {short_name(st.session_state["file_CW"])}</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Quick-clear
    if loaded > 0:
        if st.button("Clear all files", type="secondary"):
            for k in ALL_KEYS:
                st.session_state[f"file_{k}"] = None
            st.rerun()


# ── Configuration Card ────────────────────────────────────────────────────────
st.markdown('<div class="nw-card">', unsafe_allow_html=True)
st.markdown('<div class="nw-card-title">⚙ Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    sched_mod = st.number_input(
        "Schedule Rating Mod  (0 – 100)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Rule 417 · State's Schedule Rating Maximum Modification Threshold (%)",
    )

with col2:
    save_dir = st.text_input(
        "Save Location",
        value=st.session_state.save_dir,
        placeholder="e.g.  C:\\Users\\you\\Documents\\RatePages",
        help="Folder where generated rate pages will be saved.",
    )
    if save_dir:
        st.session_state.save_dir = save_dir

st.markdown('</div>', unsafe_allow_html=True)


# ── Status & Action Row ───────────────────────────────────────────────────────
st.markdown("")
status_col, btn_col = st.columns([3, 1])

with status_col:
    badge_map = {
        "ready":   ("status-ready",   "○", st.session_state.status_msg),
        "running": ("status-running", "◉", "Running… this may take a few minutes."),
        "success": ("status-success", "✓", "Rate pages created successfully."),
        "error":   ("status-error",   "✕", st.session_state.status_msg),
    }
    cls, icon, msg = badge_map.get(st.session_state.status, badge_map["ready"])
    st.markdown(f'<span class="status-badge {cls}">{icon} {msg}</span>', unsafe_allow_html=True)

with btn_col:
    run = st.button("Create Rate Pages ›", type="primary", use_container_width=True)


# ── Run Logic ─────────────────────────────────────────────────────────────────
if run:
    # Validation
    errors = []
    if not st.session_state.save_dir:
        errors.append("Please set a **Save Location** before running.")
    if loaded == 0:
        errors.append("Please upload at least one ratebook file.")

    if errors:
        for e in errors:
            st.warning(e)
    else:
        # Confirm dialog via a flag (Streamlit has no native modal, use warning)
        st.session_state.status = "running"
        st.info("⚠️ Make sure all Excel files are **saved and closed** before continuing.")

        # Build args dict (mirrors BARatePages.run signature)
        args = {k: st.session_state[f"file_{k}"] for k in ALL_KEYS}
        args["save_dir"] = st.session_state.save_dir
        args["sched_rating_mod"] = int(sched_mod) if sched_mod else None

        # ── Plug your run() call here ──────────────────────────────────────
        # from BARatePages import run as run_rate_pages
        # try:
        #     run_rate_pages(
        #         args["NGIC"], args["MM"], args["NACO"], args["NICOF"],
        #         args["NAFF"], args["HICNJ"], args["CCMIC"], args["NWAG"],
        #         args["save_dir"], args["sched_rating_mod"], args["CW"]
        #     )
        #     st.session_state.status = "success"
        # except Exception as e:
        #     st.session_state.status = "error"
        #     st.session_state.status_msg = str(e)
        # ──────────────────────────────────────────────────────────────────

        # Placeholder success (remove when wiring real run())
        st.session_state.status = "success"
        st.session_state.status_msg = "Rate pages created successfully."
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<p style="text-align:center; font-size:11px; color:#8892A4; letter-spacing:1px;">
  NATIONWIDE INSURANCE &nbsp;·&nbsp; BA RATE PAGE BUILDER &nbsp;·&nbsp; INTERNAL TOOL
</p>
""", unsafe_allow_html=True)