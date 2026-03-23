"""
BA Rate Page Builder — Streamlit UI
Mirrors all capabilities of BARatePageUserInterface.py (tkinter version)
with a professional, modern design and room for future feature additions.

Run with:
    streamlit run ba_rate_page_ui.py
"""

import streamlit as st
from pathlib import Path
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BA Rate Page Builder",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&display=swap');

/* ── CSS Variables ── */
:root {
    --bg:           #0d1117;
    --surface:      #161b22;
    --surface-2:    #21262d;
    --surface-3:    #2d333b;
    --border:       #30363d;
    --border-hover: #484f58;
    --primary:      #2f81f7;
    --primary-dim:  #1f6feb;
    --primary-glow: rgba(47, 129, 247, 0.15);
    --success:      #3fb950;
    --warning:      #d29922;
    --danger:       #f85149;
    --text:         #e6edf3;
    --text-2:       #8b949e;
    --text-3:       #6e7681;
    --accent:       #58a6ff;
    --radius:       8px;
    --radius-lg:    12px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(47,129,247,0.08), transparent),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(63,185,80,0.04), transparent);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1200px;
}

/* ── Top brand bar ── */
.brand-bar {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.5rem;
}
.brand-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--primary), #1a56db);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 20px rgba(47,129,247,0.3);
}
.brand-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    margin: 0; line-height: 1;
}
.brand-sub {
    font-size: 0.78rem;
    color: var(--text-3);
    font-weight: 400;
    margin: 0;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
    margin: 1.2rem 0 1.8rem;
}

/* ── Section headers ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 0.75rem;
}

/* ── Card panel ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--border-hover); }

/* ── File row ── */
.file-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.55rem 0.75rem;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 0.45rem;
    transition: border-color 0.2s, background 0.2s;
}
.file-row:hover { border-color: var(--border-hover); background: var(--surface-3); }
.file-row-code {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--accent);
    background: rgba(88,166,255,0.1);
    border-radius: 5px;
    padding: 2px 8px;
    min-width: 62px;
    text-align: center;
}
.file-row-name {
    font-size: 0.82rem;
    color: var(--text-2);
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.file-row-name.selected { color: var(--success); }
.file-row-badge-ok {
    font-size: 0.7rem;
    background: rgba(63,185,80,0.12);
    color: var(--success);
    border-radius: 20px;
    padding: 1px 8px;
    font-weight: 500;
}
.file-row-badge-opt {
    font-size: 0.7rem;
    background: rgba(139,148,158,0.12);
    color: var(--text-3);
    border-radius: 20px;
    padding: 1px 8px;
    font-weight: 500;
}

/* ── Stat chips ── */
.stats-row {
    display: flex;
    gap: 12px;
    margin: 1rem 0 1.5rem;
    flex-wrap: wrap;
}
.stat-chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: var(--text-2);
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.stat-chip .val { color: var(--text); font-weight: 600; }

/* ── Override Streamlit widgets ── */
/* Buttons */
.stButton > button {
    background: var(--surface-2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.35rem 1rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--surface-3) !important;
    border-color: var(--border-hover) !important;
}

/* Primary run button — target by key */
div[data-testid="stButton"] button[kind="primary"],
.run-btn > .stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dim)) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.8rem !important;
    box-shadow: 0 0 24px rgba(47,129,247,0.25) !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    box-shadow: 0 0 32px rgba(47,129,247,0.4) !important;
    transform: translateY(-1px) !important;
}

/* Text inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background: var(--primary) !important;
}

/* File uploader */
.stFileUploader > div {
    background: var(--surface-2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius-lg) !important;
}
.stFileUploader > div:hover {
    border-color: var(--primary) !important;
    background: rgba(47,129,247,0.04) !important;
}

/* Select box */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}

/* Labels */
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stFileUploader label, .stSlider label {
    color: var(--text-2) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.2rem !important;
}

/* Status / alert boxes */
.stAlert {
    border-radius: var(--radius) !important;
    font-size: 0.85rem !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary), #58a6ff) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-2) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
.streamlit-expanderContent {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-3) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: var(--radius) var(--radius) 0 0 !important;
    padding: 0.4rem 1.1rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-bottom: 1px solid var(--surface) !important;
}

/* Checkbox */
.stCheckbox > label { color: var(--text-2) !important; font-size: 0.85rem !important; }

/* Markdown text */
.stMarkdown p { color: var(--text-2); font-size: 0.88rem; line-height: 1.6; }

/* Info box custom */
.info-box {
    background: rgba(47,129,247,0.07);
    border: 1px solid rgba(47,129,247,0.25);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: var(--text-2);
    margin-bottom: 1rem;
}

/* Warning box custom */
.warn-box {
    background: rgba(210,153,34,0.08);
    border: 1px solid rgba(210,153,34,0.3);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #d29922;
    margin-bottom: 1rem;
}

/* Success box */
.ok-box {
    background: rgba(63,185,80,0.08);
    border: 1px solid rgba(63,185,80,0.3);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: var(--success);
    margin-bottom: 1rem;
}

/* Footer area */
.footer-area {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
}
.status-text {
    font-size: 0.82rem;
    color: var(--text-3);
    font-family: 'DM Mono', monospace;
}
.status-text.ok    { color: var(--success); }
.status-text.error { color: var(--danger); }
.status-text.run   { color: var(--primary); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-hover); }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ─────────────────────────────────────────────────────────
RATEBOOKS = ["NGIC", "MM", "NACO", "NAFF", "NICOF", "HICNJ", "CCMIC", "NWAG"]
OPTIONAL_RATEBOOKS = ["CW"]
ALL_KEYS = RATEBOOKS + OPTIONAL_RATEBOOKS

if "file_paths" not in st.session_state:
    st.session_state.file_paths = {k: None for k in ALL_KEYS}
if "save_dir" not in st.session_state:
    st.session_state.save_dir = None
if "sched_rating_mod" not in st.session_state:
    st.session_state.sched_rating_mod = 0
if "status" not in st.session_state:
    st.session_state.status = ("ready", "Ready.")
if "run_result" not in st.session_state:
    st.session_state.run_result = None

# ── Try importing the engine ───────────────────────────────────────────────────
try:
    from BARatePages import run as run_rate_pages
    _import_error = None
except Exception as e:
    run_rate_pages = None
    _import_error = str(e)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="brand-bar">
    <div class="brand-icon">📋</div>
    <div>
        <p class="brand-title">BA Rate Page Builder</p>
        <p class="brand-sub">Bureau of Actuarial Rate Filing System</p>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

if _import_error:
    st.markdown(f"""
    <div class="warn-box">
        ⚠ <strong>Engine not loaded:</strong> Could not import <code>BARatePages.run</code> — {_import_error}<br>
        The UI is functional but <em>Create Rate Pages</em> will not execute until the dependency is resolved.
    </div>
    """, unsafe_allow_html=True)

# ── Stats chips ────────────────────────────────────────────────────────────────
selected_count = sum(1 for v in st.session_state.file_paths.values() if v)
total = len(ALL_KEYS)
has_save = "✓ Set" if st.session_state.save_dir else "Not set"
save_color = "color:var(--success)" if st.session_state.save_dir else "color:var(--text-3)"

st.markdown(f"""
<div class="stats-row">
    <div class="stat-chip">📁 Ratebooks selected <span class="val">{selected_count} / {total}</span></div>
    <div class="stat-chip">📂 Save location <span class="val" style="{save_color}">{has_save}</span></div>
    <div class="stat-chip">📐 Schedule Mod <span class="val">{st.session_state.sched_rating_mod}%</span></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["  📂  Ratebook Files  ", "  ⚙️  Options  ", "  🚀  Run & Output  "])

# ────────────────────────────────────────────────────────────────────────────
# TAB 1 — Ratebook Files
# ────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-label">Required Ratebooks</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Upload each company's proposed ratebook Excel file (.xlsx / .xlsm / .xls).
        All required ratebooks must be provided to generate Rate Pages.
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    def render_file_uploader(key: str, label: str, optional: bool, col):
        with col:
            # Show current state row
            path = st.session_state.file_paths.get(key)
            badge = '<span class="file-row-badge-opt">Optional</span>' if optional else ""
            name_class = "file-row-name selected" if path else "file-row-name"
            display_name = Path(path).name if path else "No file selected"
            tick = "✓" if path else "·"
            st.markdown(f"""
            <div class="file-row">
                <span class="file-row-code">{key}</span>
                <span class="{name_class}">{tick} {display_name}</span>
                {badge}
            </div>
            """, unsafe_allow_html=True)

            uploaded = st.file_uploader(
                label,
                type=["xlsx", "xlsm", "xls"],
                key=f"uploader_{key}",
                label_visibility="collapsed",
            )
            if uploaded is not None:
                # Save the uploaded file to a temp path so BARatePages.run() can read it
                import tempfile, shutil
                tmp_dir = Path(tempfile.gettempdir()) / "ba_rate_pages"
                tmp_dir.mkdir(exist_ok=True)
                tmp_path = tmp_dir / uploaded.name
                with open(tmp_path, "wb") as f:
                    shutil.copyfileobj(uploaded, f)
                st.session_state.file_paths[key] = str(tmp_path)
                st.rerun()

    keys_left  = ["NGIC", "MM", "NACO", "NAFF"]
    keys_right = ["NICOF", "HICNJ", "CCMIC", "NWAG"]

    for k in keys_left:
        render_file_uploader(k, f"Select {k} Ratebook", optional=False, col=col_left)
    for k in keys_right:
        render_file_uploader(k, f"Select {k} Ratebook", optional=False, col=col_right)

    st.markdown('<p class="section-label" style="margin-top:1.5rem">Optional Ratebook</p>', unsafe_allow_html=True)
    col_cw, _ = st.columns([1, 1], gap="large")
    render_file_uploader("CW", "Select CW Ratebook (Optional)", optional=True, col=col_cw)

    # Quick clear all button
    st.markdown("&nbsp;", unsafe_allow_html=True)
    if st.button("🗑 Clear all file selections", key="clear_files"):
        for k in ALL_KEYS:
            st.session_state.file_paths[k] = None
        st.rerun()

# ────────────────────────────────────────────────────────────────────────────
# TAB 2 — Options
# ────────────────────────────────────────────────────────────────────────────
with tab2:
    opt_l, opt_r = st.columns(2, gap="large")

    with opt_l:
        st.markdown('<p class="section-label">Schedule Rating</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            <strong>Rule 417</strong> — State's Schedule Rating Maximum Modification Threshold.<br>
            Enter an integer between <strong>0</strong> and <strong>100</strong> (%).
        </div>
        """, unsafe_allow_html=True)

        sched_val = st.number_input(
            "Schedule Rating Mod (%)",
            min_value=0,
            max_value=100,
            value=st.session_state.sched_rating_mod,
            step=1,
            key="sched_input",
            help="Rule 417: Schedule Rating Maximum Modification Threshold (0–100%)",
        )
        st.session_state.sched_rating_mod = int(sched_val)

        # Visual indicator
        pct = int(sched_val)
        color = "#3fb950" if pct <= 33 else "#d29922" if pct <= 66 else "#f85149"
        st.markdown(f"""
        <div style="margin-top:0.5rem">
            <div style="font-size:0.75rem;color:var(--text-3);margin-bottom:4px">Threshold level</div>
            <div style="background:var(--surface-3);border-radius:4px;height:6px;overflow:hidden">
                <div style="width:{pct}%;background:{color};height:100%;border-radius:4px;transition:width 0.3s"></div>
            </div>
            <div style="font-size:0.75rem;color:{color};margin-top:4px;font-weight:600">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)

    with opt_r:
        st.markdown('<p class="section-label">Save Location</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            Enter the full path of the folder where Rate Pages should be saved.
        </div>
        """, unsafe_allow_html=True)

        save_dir_input = st.text_input(
            "Output folder path",
            value=st.session_state.save_dir or "",
            placeholder="e.g.  C:\\Users\\You\\Documents\\RatePages",
            key="save_dir_input",
            help="Full path to the folder where Rate Pages will be written.",
        )

        if save_dir_input.strip():
            p = Path(save_dir_input.strip())
            if p.exists() and p.is_dir():
                st.session_state.save_dir = str(p)
                st.markdown("""
                <div class="ok-box">✓ Valid directory — output will be saved here.</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warn-box">⚠ Path does not exist or is not a directory.</div>
                """, unsafe_allow_html=True)
                st.session_state.save_dir = None
        else:
            st.session_state.save_dir = None

        # Future: more options can go here
        st.markdown('<p class="section-label" style="margin-top:1.5rem">Additional Options</p>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">More configuration options will appear here in future releases.</div>', unsafe_allow_html=True)

        with st.expander("⚙ Advanced (coming soon)", expanded=False):
            st.markdown('<div style="color:var(--text-3);font-size:0.82rem;padding:0.5rem 0">Future: output format, verbosity, custom templates, etc.</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 3 — Run & Output
# ────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-label">Pre-flight Checklist</p>', unsafe_allow_html=True)

    checks = {
        "BARatePages engine loaded":    _import_error is None,
        "Required ratebooks selected":  all(st.session_state.file_paths[k] for k in RATEBOOKS),
        "Save location configured":      st.session_state.save_dir is not None,
        "Schedule Rating Mod is set":    True,  # always valid (defaults to 0)
    }

    for label, ok in checks.items():
        icon = "✅" if ok else "❌"
        color = "var(--success)" if ok else "var(--danger)"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid var(--border)">
            <span style="font-size:1rem">{icon}</span>
            <span style="font-size:0.85rem;color:{color}">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    all_ready = all(checks.values())
    st.markdown("&nbsp;", unsafe_allow_html=True)

    # Warning notice
    st.markdown("""
    <div class="warn-box">
        ⚠ <strong>Important:</strong> Make sure all Excel ratebook files are <strong>saved and closed</strong>
        before clicking Create. Open files may cause read errors.
    </div>
    """, unsafe_allow_html=True)

    # ── Run button ─────────────────────────────────────────────────────────
    run_col, status_col = st.columns([1, 3], gap="medium")
    with run_col:
        run_clicked = st.button(
            "🚀  Create Rate Pages",
            disabled=not all_ready,
            type="primary",
            use_container_width=True,
            key="run_btn",
        )

    with status_col:
        sk, sm = st.session_state.status
        css_class = {"ready": "", "ok": "ok", "error": "error", "run": "run"}.get(sk, "")
        st.markdown(f'<p class="status-text {css_class}">{sm}</p>', unsafe_allow_html=True)

    # ── Execute ────────────────────────────────────────────────────────────
    if run_clicked and all_ready:
        st.session_state.status = ("run", "⏳ Running… This may take a few minutes.")
        progress_bar = st.progress(0, text="Initialising…")

        # Build args tuple matching BARatePages.run() signature:
        # run(NGICRatebook, MMRatebook, NACORatebook, NICOFRatebook,
        #     NAFFRatebook, HICNJRatebook, CCMICRatebook, NWAGRatebook,
        #     folder_selected, SchedRatingMod, CWRatebook)
        fp = st.session_state.file_paths
        args = (
            fp["NGIC"],
            fp["MM"],
            fp["NACO"],
            fp["NICOF"],
            fp["NAFF"],
            fp["HICNJ"],
            fp["CCMIC"],
            fp["NWAG"],
            st.session_state.save_dir,
            st.session_state.sched_rating_mod if st.session_state.sched_rating_mod != 0 else None,
            fp["CW"],
        )

        progress_bar.progress(20, text="Validating inputs…")

        try:
            progress_bar.progress(40, text="Generating Rate Pages…")
            run_rate_pages(*args)
            progress_bar.progress(100, text="Done!")
            st.session_state.status = ("ok", "✓ Rate Pages created successfully.")
            st.session_state.run_result = "success"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            st.session_state.status = ("error", f"✗ Failed: {e}")
            st.session_state.run_result = ("error", str(e), tb)
            progress_bar.empty()

        st.rerun()

    # ── Result display ─────────────────────────────────────────────────────
    if st.session_state.run_result == "success":
        st.markdown("""
        <div class="ok-box">
            ✅ <strong>Rate Pages created successfully.</strong><br>
            Check your save location for the output files.
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.save_dir:
            st.markdown(f'<div style="font-family:\'DM Mono\',monospace;font-size:0.78rem;color:var(--text-3)">📂 {st.session_state.save_dir}</div>', unsafe_allow_html=True)

    elif isinstance(st.session_state.run_result, tuple) and st.session_state.run_result[0] == "error":
        _, msg, tb = st.session_state.run_result
        st.markdown(f"""
        <div class="warn-box">
            ❌ <strong>Rate Page generation failed.</strong><br>
            <code style="font-size:0.8rem">{msg}</code>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("📋 Full traceback", expanded=False):
            st.code(tb, language="python")

    # ── Reset button ───────────────────────────────────────────────────────
    if st.session_state.run_result is not None:
        if st.button("↺ Reset & Run Again", key="reset_btn"):
            st.session_state.run_result = None
            st.session_state.status = ("ready", "Ready.")
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM STATUS BAR
# ══════════════════════════════════════════════════════════════════════════════
sk, sm = st.session_state.status
engine_status = "🟢 Engine ready" if _import_error is None else "🔴 Engine not loaded"
st.markdown(f"""
<div class="footer-area">
    <span class="status-text">{engine_status}</span>
    <span class="status-text">{selected_count}/{total} ratebooks · Mod: {st.session_state.sched_rating_mod}%</span>
    <span class="status-text">BA Rate Page Builder — v1.0</span>
</div>
""", unsafe_allow_html=True)