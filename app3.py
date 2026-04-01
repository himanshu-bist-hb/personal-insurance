"""
BA Rate Pages - Streamlit Web Application
Nationwide Insurance - BA Analytics Division
Converts ratebook Excel files into formatted rate pages (Excel/PDF)
"""

import streamlit as st
import os
import tempfile
import threading
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Page Config (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BA Rate Pages | Nationwide",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Try importing the actual backend; gracefully degrade if missing
# ─────────────────────────────────────────────────────────────────────────────
# try:
#     from BARatePages import run as run_rate_pages  # type: ignore
#     _IMPORT_ERROR = None
# except Exception as e:
#     run_rate_pages = None
#     _IMPORT_ERROR = str(e)

# ─────────────────────────────────────────────────────────────────────────────
# Design Tokens  (Nationwide Brand / DESIGN.md palette)
# ─────────────────────────────────────────────────────────────────────────────
PRIMARY        = "#003e83"
PRIMARY_CONT   = "#1d56a4"
PRIMARY_FIXED  = "#d7e2ff"
SURFACE        = "#f7f9fc"
SURF_LOW       = "#f2f4f7"
SURF_HIGH      = "#e0e3e6"
SURF_WHITE     = "#ffffff"
ON_SURFACE     = "#191c1e"
ON_SURF_VAR    = "#424751"
OUTLINE_VAR    = "#c3c6d3"
TERTIARY       = "#693000"
ERROR          = "#ba1a1a"

# ─────────────────────────────────────────────────────────────────────────────
# Global CSS injection
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {ON_SURFACE};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {SURF_LOW} !important;
    border-right: 1px solid {OUTLINE_VAR} !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.5rem;
}}

/* ── Main area background ── */
[data-testid="stAppViewContainer"] > .main {{
    background: {SURFACE};
}}
[data-testid="block-container"] {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}}

/* ── Headings ── */
h1, h2, h3 {{
    font-family: 'Manrope', sans-serif !important;
    color: {ON_SURFACE} !important;
}}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header {{visibility: hidden;}}
[data-testid="stToolbar"] {{display: none;}}

/* ── Upload zone cards ── */
.upload-card {{
    background: {SURF_LOW};
    border-radius: 12px;
    border: 1.5px dashed {OUTLINE_VAR};
    padding: 18px 12px;
    text-align: center;
    transition: all .18s ease;
    cursor: pointer;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
}}
.upload-card:hover {{
    border-color: {PRIMARY};
    background: {PRIMARY_FIXED};
}}
.upload-card.uploaded {{
    border-color: {PRIMARY};
    background: {PRIMARY_FIXED};
    border-style: solid;
}}
.upload-card-label {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: {ON_SURF_VAR};
    margin: 0;
}}
.upload-card-sub {{
    font-size: 9px;
    color: #8a8fa0;
    margin: 0;
}}
.upload-icon {{
    font-size: 22px;
    color: #9aa0ae;
}}
.upload-card.uploaded .upload-icon {{ color: {PRIMARY}; }}
.upload-card.uploaded .upload-card-label {{ color: {PRIMARY}; }}

/* ── Section headers ── */
.section-header {{
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #8a8fa0;
    margin-bottom: 12px;
}}

/* ── Pill badge ── */
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 100px;
    background: {PRIMARY_FIXED};
    color: {PRIMARY_CONT};
}}

/* ── Parameters card ── */
.param-card {{
    background: {SURF_LOW};
    border-radius: 12px;
    padding: 20px;
}}

/* ── Status card ── */
.status-card {{
    background: {SURF_WHITE};
    border-left: 4px solid {PRIMARY};
    border-radius: 0 12px 12px 0;
    padding: 20px;
    box-shadow: 0 2px 16px 0 rgba(0,62,131,.06);
}}

/* ── Progress bar override ── */
[data-testid="stProgressBar"] > div > div {{
    background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_CONT}) !important;
    border-radius: 4px !important;
}}
[data-testid="stProgressBar"] > div {{
    background: {SURF_HIGH} !important;
    border-radius: 4px !important;
    height: 6px !important;
}}

/* ── Buttons ── */
[data-testid="baseButton-primary"] {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_CONT} 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 32px !important;
    color: white !important;
    box-shadow: 0 2px 16px rgba(0,62,131,.25) !important;
    transition: all .18s ease !important;
    width: 100% !important;
}}
[data-testid="baseButton-primary"]:hover {{
    box-shadow: 0 4px 24px rgba(0,62,131,.35) !important;
    transform: translateY(-1px) !important;
}}
[data-testid="baseButton-secondary"] {{
    background: {SURF_WHITE} !important;
    border: 1.5px solid {OUTLINE_VAR} !important;
    border-radius: 8px !important;
    color: {ON_SURF_VAR} !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
}}

/* ── Text inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {{
    border-radius: 6px !important;
    border-color: {OUTLINE_VAR} !important;
    font-size: 13px !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {{
    border-color: {PRIMARY} !important;
    box-shadow: 0 0 0 2px {PRIMARY_FIXED} !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {{
    color: {PRIMARY} !important;
}}

/* ── Sidebar nav item ── */
.nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 20px;
    border-radius: 0;
    font-size: 13px;
    font-weight: 500;
    color: {ON_SURF_VAR};
    cursor: pointer;
    transition: background .15s;
    border-right: 3px solid transparent;
    text-decoration: none;
}}
.nav-item:hover {{
    background: {SURF_HIGH};
    color: {ON_SURFACE};
}}
.nav-item.active {{
    background: {SURF_WHITE};
    color: {PRIMARY};
    border-right-color: {PRIMARY};
    font-weight: 700;
}}
.nav-icon {{ font-size: 18px; }}

/* ── LOB title ── */
.lob-heading {{
    font-family: 'Manrope', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: {ON_SURFACE};
    margin: 0 0 4px 0;
    line-height: 1.1;
}}
.lob-subheading {{
    font-size: 13px;
    color: {ON_SURF_VAR};
    margin: 0 0 24px 0;
}}

/* ── File name pill ── */
.file-pill {{
    display: inline-block;
    background: {PRIMARY_FIXED};
    color: {PRIMARY};
    font-size: 9px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 100px;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: middle;
}}

/* ── Alert / info boxes ── */
.info-box {{
    background: {PRIMARY_FIXED};
    border: 1px solid {PRIMARY_CONT}44;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: {PRIMARY_CONT};
    display: flex;
    gap: 8px;
    align-items: flex-start;
}}
.error-box {{
    background: #ffdad6;
    border: 1px solid {ERROR}44;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: {ERROR};
    display: flex;
    gap: 8px;
    align-items: flex-start;
}}
.success-box {{
    background: #d4edda;
    border: 1px solid #28a74544;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #155724;
    display: flex;
    gap: 8px;
    align-items: flex-start;
}}

/* ── Step indicator ── */
.step-dot {{
    display: inline-flex;
    width: 20px; height: 20px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
    font-size: 8px;
    font-weight: 800;
    border: 2px solid white;
}}
.step-dot.done {{ background: {SURF_HIGH}; color: {ON_SURF_VAR}; }}
.step-dot.active {{ background: {PRIMARY}; color: white; }}
.step-dot.pending {{ background: {SURF_LOW}; color: #bbb; }}

/* ── Footer ── */
.app-footer {{
    font-size: 10px;
    color: #aaa;
    padding: 12px 0 4px 0;
    border-top: 1px solid {OUTLINE_VAR};
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

/* ── Streamlit file uploader compact ── */
[data-testid="stFileUploaderDropzone"] {{
    border-radius: 8px !important;
    background: {SURF_LOW} !important;
    border-color: {OUTLINE_VAR} !important;
    padding: 8px !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{
    border-color: {PRIMARY} !important;
    background: {PRIMARY_FIXED} !important;
}}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab"] {{
    font-family: 'Manrope', sans-serif;
    font-weight: 600;
    font-size: 13px;
    color: {ON_SURF_VAR};
    border-bottom: 3px solid transparent;
    padding-bottom: 6px;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: {PRIMARY} !important;
    border-bottom-color: {PRIMARY} !important;
    background: transparent !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background-color: {PRIMARY} !important;
    height: 3px !important;
    border-radius: 3px !important;
}}

/* ── Dividers ── */
hr {{ border-color: {OUTLINE_VAR} !important; margin: 12px 0 !important; opacity: .5; }}

/* ── Coming soon placeholder ── */
.coming-soon {{
    background: {SURF_LOW};
    border-radius: 16px;
    padding: 64px 32px;
    text-align: center;
    margin-top: 32px;
}}
.coming-soon h3 {{
    font-family: 'Manrope', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: {ON_SURF_VAR} !important;
    margin-bottom: 8px;
}}
.coming-soon p {{
    font-size: 13px;
    color: #9aa0ae;
}}
.coming-soon .big-icon {{
    font-size: 48px;
    margin-bottom: 12px;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "lob": "Business Auto",
        "files": {},          # key → UploadedFile
        "save_dir": "",
        "sched_rating": 0,
        "status": "Ready.",
        "status_type": "info",   # info | error | success
        "running": False,
        "progress": 0,
        "log_lines": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─────────────────────────────────────────────────────────────────────────────
# LOB definitions  (extend this dict to add more LOBs)
# ─────────────────────────────────────────────────────────────────────────────
LOB_CONFIG = {
    "Business Auto": {
        "icon": "🚗",
        "description": "Transforming uploaded ratebook data into standardized customer-facing rate pages.",
        "mandatory_files": [
            ("NGIC",  "NGIC Ratebook",        "Excel/CSV"),
            ("MM",    "MM Ratebook",           "Excel/CSV"),
            ("NACO",  "NACO Ratebook",         "Excel/CSV"),
            ("NAFF",  "NAFF Ratebook",         "Excel/CSV"),
            ("NICOF", "NICOF Ratebook",        "Excel/CSV"),
            ("HICNJ", "HICNJ Ratebook",       "Excel/CSV"),
            ("CCMIC", "CCMIC Ratebook",        "Excel/CSV"),
            ("NWAG",  "NWAG Ratebook",         "Excel/CSV"),
        ],
        "optional_files": [
            ("CW",    "CW Ratebook (Optional)", "Excel/CSV"),
        ],
        # "backend_fn": run_rate_pages,
        "arg_order": ["NGIC","MM","NACO","NICOF","NAFF","HICNJ","CCMIC","NWAG","save_dir","sched_rating","CW"],
    },
    "General Liability": {
        "icon": "⚖️",
        "description": "General Liability ratebook processing — configure your GL rate pages.",
        "mandatory_files": [],
        "optional_files":  [],
        "backend_fn": None,
        "arg_order": [],
    },
    "Farm Auto": {
        "icon": "🚜",
        "description": "Farm Auto ratebook processing — configure your Farm rate pages.",
        "mandatory_files": [],
        "optional_files":  [],
        "backend_fn": None,
        "arg_order": [],
    },
    "Property": {
        "icon": "🏠",
        "description": "Property ratebook processing — configure your Property rate pages.",
        "mandatory_files": [],
        "optional_files":  [],
        "backend_fn": None,
        "arg_order": [],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="padding: 0 16px 20px 16px;">
      <div style="font-family:'Manrope',sans-serif; font-size:18px; font-weight:800;
                  color:#003e83; letter-spacing:-.5px; line-height:1;">
        Nationwide
      </div>
      <div style="font-size:9px; font-weight:700; letter-spacing:.12em;
                  text-transform:uppercase; color:#9aa0ae; margin-top:2px;">
        BA Analytics Platform
      </div>
    </div>
    <div style="font-size:9px; font-weight:700; letter-spacing:.12em;
                text-transform:uppercase; color:#9aa0ae;
                padding: 0 16px 8px 16px; border-bottom:1px solid #c3c6d344;">
      Insurance Categories
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'/>", unsafe_allow_html=True)

    for lob_name, cfg in LOB_CONFIG.items():
        is_active = st.session_state.lob == lob_name
        active_cls = "active" if is_active else ""
        # Use a button styled as nav item
        btn_style = f"""
        <style>
        div[data-testid="stButton"] button[kind="secondary"]#nav_{lob_name.replace(' ','_')} {{
            background: {'#ffffff' if is_active else 'transparent'} !important;
            color: {'#003e83' if is_active else '#424751'} !important;
            border: none !important;
            border-right: 3px solid {'#003e83' if is_active else 'transparent'} !important;
            border-radius: 0 !important;
            font-weight: {'700' if is_active else '500'} !important;
            text-align: left !important;
            width: 100% !important;
            padding: 9px 20px !important;
            font-size: 13px !important;
            justify-content: flex-start !important;
        }}
        </style>
        """
        if st.button(f"{cfg['icon']}  {lob_name}", key=f"nav_{lob_name}", use_container_width=True):
            st.session_state.lob = lob_name
            # Reset file state when switching LOB
            st.session_state.files = {}
            st.session_state.status = "Ready."
            st.session_state.status_type = "info"
            st.session_state.running = False
            st.session_state.progress = 0
            st.rerun()

    st.markdown("<div style='flex:1'/>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding: 0 12px;'>
      <div style='font-size:10px; color:#9aa0ae; display:flex; gap:6px; align-items:center; margin-bottom:6px;'>
        <span>❓</span><span>Support</span>
      </div>
      <div style='font-size:10px; color:#9aa0ae; display:flex; gap:6px; align-items:center;'>
        <span>📄</span><span>Documentation</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Header tabs  (Dashboard / Settings)
# ─────────────────────────────────────────────────────────────────────────────
tab_dashboard, tab_settings = st.tabs(["Dashboard", "Settings"])

# ─────────────────────────────────────────────────────────────────────────────
# ──  SETTINGS TAB  ───────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
with tab_settings:
    st.markdown("""
    <div class='coming-soon'>
      <div class='big-icon'>⚙️</div>
      <h3>Application Settings</h3>
      <p>Global preferences, theme options, and advanced configuration will appear here.</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ──  DASHBOARD TAB  ──────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
with tab_dashboard:

    lob      = st.session_state.lob
    cfg      = LOB_CONFIG[lob]
    man_keys = [f[0] for f in cfg["mandatory_files"]]
    opt_keys = [f[0] for f in cfg["optional_files"]]

    # ── LOB heading ──
    st.markdown(f"""
    <p class='lob-heading'>{cfg['icon']}  {lob} Ratebooks</p>
    <p class='lob-subheading'>{cfg['description']}</p>
    """, unsafe_allow_html=True)

    # Show backend import warning at top
    # if _IMPORT_ERROR:
    #     st.markdown(f"""
    #     <div class='error-box'>
    #       ⚠️&nbsp; <span><b>Backend not found:</b> BARatePages.run could not be imported.
    #       The UI is fully functional; rate page generation requires the backend module.
    #       <br/><code style='font-size:10px'>{_IMPORT_ERROR}</code></span>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     st.markdown("<div style='height:12px'/>", unsafe_allow_html=True)

    # ── Only Business Auto has the real form; others show placeholder ──
    if not cfg["mandatory_files"] and not cfg["optional_files"]:
        st.markdown(f"""
        <div class='coming-soon'>
          <div class='big-icon'>{cfg['icon']}</div>
          <h3>{lob} — Coming Soon</h3>
          <p>The {lob} ratebook workflow is under development.<br/>
             Switch to <b>Business Auto</b> to use the current tool.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Two-column layout: left (files) | right (params + status) ──
        col_files, col_right = st.columns([8, 4], gap="large")

        # ── LEFT: File uploads ─────────────────────────────────────────
        with col_files:

            # Mandatory uploads count
            uploaded_count = sum(
                1 for k in man_keys if k in st.session_state.files and st.session_state.files[k]
            )
            total_req = len(man_keys)

            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
              <span class='section-header' style='margin-bottom:0'>Mandatory Ratebook Uploads</span>
              <span class='badge'>{'✅' if uploaded_count==total_req else '📂'} {uploaded_count} of {total_req} Required</span>
            </div>
            """, unsafe_allow_html=True)

            # Grid of file uploaders
            n_cols = 3
            mand_chunks = [cfg["mandatory_files"][i:i+n_cols] for i in range(0, len(cfg["mandatory_files"]), n_cols)]

            for row_items in mand_chunks:
                cols = st.columns(n_cols)
                for col, (key, label, fmt) in zip(cols, row_items):
                    with col:
                        already = st.session_state.files.get(key)
                        is_up   = already is not None
                        icon    = "✅" if is_up else "☁️"
                        border  = f"border: 1.5px solid {PRIMARY}; border-style: solid;" if is_up else ""
                        bg      = PRIMARY_FIXED if is_up else SURF_LOW
                        st.markdown(f"""
                        <div class='upload-card {"uploaded" if is_up else ""}' style='background:{bg}; {border}'>
                          <span class='upload-icon'>{icon}</span>
                          <p class='upload-card-label'>{label}</p>
                          <p class='upload-card-sub'>{fmt}</p>
                          {"<span class='file-pill'>" + already.name + "</span>" if is_up else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        uf = st.file_uploader(
                            f"Upload {key}",
                            type=["xlsx","xlsm","xls","csv"],
                            key=f"fu_{lob}_{key}",
                            label_visibility="collapsed",
                        )
                        if uf:
                            st.session_state.files[key] = uf

            # ── Optional supplements ──
            if cfg["optional_files"]:
                st.markdown("<div style='height:16px'/>", unsafe_allow_html=True)
                st.markdown("<span class='section-header'>Optional Supplements</span>", unsafe_allow_html=True)
                opt_cols = st.columns(len(cfg["optional_files"]))
                for col, (key, label, fmt) in zip(opt_cols, cfg["optional_files"]):
                    with col:
                        already = st.session_state.files.get(key)
                        is_up   = already is not None
                        st.markdown(f"""
                        <div class='upload-card {"uploaded" if is_up else ""}' style='background:{"#ffffff" if not is_up else PRIMARY_FIXED}'>
                          <span class='upload-icon'>{"📄" if not is_up else "✅"}</span>
                          <p class='upload-card-label'>{label}</p>
                          <p class='upload-card-sub'>{fmt}</p>
                          {"<span class='file-pill'>" + already.name + "</span>" if is_up else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        uf = st.file_uploader(
                            f"Upload {key}",
                            type=["xlsx","xlsm","xls","csv"],
                            key=f"fu_{lob}_{key}",
                            label_visibility="collapsed",
                        )
                        if uf:
                            st.session_state.files[key] = uf

            # ── Create Rate Pages button ──
            st.markdown("<div style='height:20px'/>", unsafe_allow_html=True)

            all_required = all(
                k in st.session_state.files and st.session_state.files[k]
                for k in man_keys
            )
            has_save_dir = bool(st.session_state.save_dir.strip())

            btn_disabled = st.session_state.running or not all_required or not has_save_dir

            if st.button(
                "🚀  Create Rate Pages",
                type="primary",
                disabled=btn_disabled,
                use_container_width=True,
                key="btn_run",
            ):
                # ── Validation ──
                sched = st.session_state.get("sched_rating_input", 0)
                if not (0 <= sched <= 100):
                    st.session_state.status = "❌ Schedule Rating must be between 0 and 100."
                    st.session_state.status_type = "error"
                    st.rerun()
                else:
                    st.session_state.sched_rating = sched
                    st.session_state.running = True
                    st.session_state.progress = 0
                    st.session_state.status = "Running… This may take a few minutes."
                    st.session_state.status_type = "info"
                    st.session_state.log_lines = []
                    st.rerun()

            if not all_required:
                st.markdown(f"""
                <p style='text-align:center; font-size:10px; color:#9aa0ae;
                           font-style:italic; margin-top:6px;'>
                  All required files must be uploaded before processing can begin.
                </p>
                """, unsafe_allow_html=True)
            elif not has_save_dir:
                st.markdown(f"""
                <p style='text-align:center; font-size:10px; color:#c17f24;
                           font-style:italic; margin-top:6px;'>
                  Please set a save location before running.
                </p>
                """, unsafe_allow_html=True)

        # ── RIGHT: Parameters + Status ─────────────────────────────────
        with col_right:

            # ── Ratebook Parameters ──
            st.markdown(f"""
            <div class='param-card'>
              <div style='display:flex; align-items:center; gap:8px; margin-bottom:16px;'>
                <span style='font-size:18px;'>⚙️</span>
                <span style='font-family:Manrope,sans-serif; font-size:15px;
                             font-weight:800; color:{ON_SURFACE};'>Ratebook Parameters</span>
              </div>
            """, unsafe_allow_html=True)

            st.markdown("<span class='section-header'>Schedule Rating %</span>", unsafe_allow_html=True)
            sched_val = st.number_input(
                "Schedule Rating",
                min_value=0,
                max_value=100,
                value=st.session_state.sched_rating,
                step=1,
                key="sched_rating_input",
                label_visibility="collapsed",
            )
            st.slider(
                "Rating Slider",
                0, 100,
                value=sched_val,
                key="sched_slider",
                label_visibility="collapsed",
            )
            # Sync slider ↔ number input
            if st.session_state.get("sched_slider") != sched_val:
                st.session_state.sched_rating = st.session_state.sched_slider
            st.markdown("""
            <p style='font-size:9px; color:#9aa0ae; margin-top:-8px; margin-bottom:12px;'>
              Adjust base rating factor for commercial risk. (0–100)
            </p>
            """, unsafe_allow_html=True)

            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown("<span class='section-header'>Save Location</span>", unsafe_allow_html=True)
            save_input = st.text_input(
                "Save Location",
                value=st.session_state.save_dir,
                placeholder="/outputs/rate-pages/",
                key="save_dir_input",
                label_visibility="collapsed",
            )
            st.session_state.save_dir = save_input

            st.markdown("""
            <p style='font-size:9px; color:#9aa0ae; margin-top:-8px;'>
              📁 Enter the full path to your local output directory.
            </p>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)  # close param-card

            # ── Process Status ──
            st.markdown("<div style='height:16px'/>", unsafe_allow_html=True)

            if st.session_state.running:
                status_icon = "🔄"
                pill_color  = PRIMARY
                pill_label  = "RUNNING"
                anim_attr   = "animation: pulse 1s infinite;"
            elif st.session_state.status_type == "success":
                status_icon = "✅"
                pill_color  = "#155724"
                pill_label  = "DONE"
                anim_attr   = ""
            elif st.session_state.status_type == "error":
                status_icon = "❌"
                pill_color  = ERROR
                pill_label  = "ERROR"
                anim_attr   = ""
            else:
                status_icon = "⏳"
                pill_color  = "#8a8fa0"
                pill_label  = "IDLE"
                anim_attr   = ""

            st.markdown(f"""
            <div class='status-card'>
              <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
                <span class='section-header' style='margin-bottom:0'>Process Status</span>
                <span style='display:inline-flex; align-items:center; gap:4px;
                             font-size:9px; font-weight:700; letter-spacing:.1em;
                             text-transform:uppercase; color:{pill_color};'>
                  <span style='width:7px; height:7px; border-radius:50%;
                               background:{pill_color}; display:inline-block; {anim_attr}'></span>
                  {pill_label}
                </span>
              </div>
            """, unsafe_allow_html=True)

            if st.session_state.running:
                st.progress(st.session_state.progress / 100)
                st.markdown(f"""
                <div style='background:{PRIMARY_FIXED}; border:1px solid {PRIMARY_CONT}44;
                            border-radius:8px; padding:10px 14px; margin-top:10px;
                            display:flex; gap:8px; align-items:flex-start;'>
                  <span style='font-size:16px;'>🔄</span>
                  <div>
                    <p style='font-size:10px; font-weight:700; color:{ON_SURFACE}; margin:0 0 2px 0;'>
                      Processing…
                    </p>
                    <p style='font-size:9px; color:{ON_SURF_VAR}; margin:0; font-style:italic;'>
                      {st.session_state.status}
                    </p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Status message
                box_cls = {
                    "error": "error-box",
                    "success": "success-box",
                }.get(st.session_state.status_type, "info-box")
                st.markdown(f"""
                <div class='{box_cls}'>
                  {status_icon}&nbsp;<span>{st.session_state.status}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)  # close status-card

        # ── Run logic ─────────────────────────────────────────────────────
        # Execute in main thread (Streamlit doesn't support background threads well for UI updates)
        if st.session_state.running and run_rate_pages is not None:
            try:
                # Save uploaded files to temp directory
                tmp_dir = tempfile.mkdtemp()
                file_paths = {}
                all_keys = man_keys + opt_keys
                for key in all_keys:
                    uf = st.session_state.files.get(key)
                    if uf:
                        tmp_path = os.path.join(tmp_dir, uf.name)
                        with open(tmp_path, "wb") as f:
                            f.write(uf.getbuffer())
                        file_paths[key] = tmp_path
                    else:
                        file_paths[key] = None

                # Build args in correct order
                save_dir  = st.session_state.save_dir or tmp_dir
                sched_mod = st.session_state.sched_rating or None
                args = tuple(
                    file_paths.get(k) if k not in ("save_dir", "sched_rating") else
                    (save_dir if k == "save_dir" else sched_mod)
                    for k in cfg["arg_order"]
                )
                run_rate_pages(*args)
                st.session_state.status = f"✅ Rate Pages created successfully in: {save_dir}"
                st.session_state.status_type = "success"
            except Exception as e:
                st.session_state.status = f"Error: {e}"
                st.session_state.status_type = "error"
            finally:
                st.session_state.running = False
                st.session_state.progress = 100
                st.rerun()

        elif st.session_state.running and run_rate_pages is None:
            # Backend not available — simulate completion
            st.session_state.status = "⚠️ Backend module not available. Cannot generate rate pages."
            st.session_state.status_type = "error"
            st.session_state.running = False
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='app-footer'>
  <span>© 2024 Nationwide Mutual Insurance Company. Internal Utility.</span>
  <div style='display:flex; gap:16px; align-items:center;'>
    <span style='display:flex; align-items:center; gap:4px;'>
      <span style='width:6px;height:6px;border-radius:50%;background:#28a745;display:inline-block;'></span>
      Connected: Localhost
    </span>
    <span style='border-left:1px solid #c3c6d3; padding-left:12px;
                 font-size:9px; font-weight:800; letter-spacing:.12em;
                 text-transform:uppercase; color:#9aa0ae;'>V1.2.0-BETA</span>
  </div>
</div>
""", unsafe_allow_html=True)