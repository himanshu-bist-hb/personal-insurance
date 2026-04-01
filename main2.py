# ba_rate_pages_app.py
# Run with:  streamlit run app.py

import streamlit as st
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog
    _TK_OK = True
except Exception:
    _TK_OK = False

st.set_page_config(
    page_title="BA Rate Page Builder · Nationwide",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── session state ──────────────────────────────────────────────────────────────
REQUIRED = ["NGIC", "MM", "NACO", "NAFF", "NICOF", "HICNJ", "CCMIC", "NWAG"]
OPTIONAL = ["CW"]
ALL_KEYS = REQUIRED + OPTIONAL

for k in ALL_KEYS:
    st.session_state.setdefault(f"file_{k}", None)
st.session_state.setdefault("save_dir", "")
st.session_state.setdefault("sched_mod", 0)
st.session_state.setdefault("run_status", "idle")
st.session_state.setdefault("run_msg", "")
st.session_state.setdefault("lob", "Business Auto")

# ── helpers ───────────────────────────────────────────────────────────────────
def n_req():    return sum(1 for k in REQUIRED if st.session_state[f"file_{k}"])
def all_req():  return n_req() == len(REQUIRED)

def chip(f):
    if f:
        name = Path(f.name).stem[:17]
        return f'<span class="chip-ok">✓ {name}</span>'
    return '<span class="chip-none">— none</span>'

def browse_folder():
    if not _TK_OK:
        return None
    try:
        root = tk.Tk(); root.withdraw()
        root.wm_attributes('-topmost', True)
        folder = filedialog.askdirectory(title="Select Save Location")
        root.destroy()
        return folder or None
    except Exception:
        return None

def spacer(px=20):
    st.markdown(f"<div style='height:{px}px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Libre+Baskerville:wght@700&display=swap');

:root {
  --nw-blue:   #1A5DAB;
  --nw-deep:   #0D3F7A;
  --nw-lt:     #EBF2FB;
  --gold:      #C8A951;
  --gold-lt:   #EDD97A;
  --off:       #F4F7FB;
  --surface:   #FFFFFF;
  --border:    #D4DFEF;
  --text:      #0C1A35;
  --muted:     #6B7A9E;
  --ok-bg:     #EAF5EE;
  --ok-fg:     #196B38;
  --radius:    10px;
  --shadow:    0 2px 12px rgba(13,63,122,0.08);
}

/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main, .block-container {
  background: var(--off) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text) !important;
  padding-top: 0 !important;
}
/* Fix header overlap issue */
.block-container {
  position: relative;
  z-index: 1;
  margin-top: 64px;  /* push content below header */
}

#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--nw-deep) !important;
  border-right: none !important;
  min-width: 220px !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
}

/* Hide sidebar collapse toggle (we use our own) */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
  display: none !important;
}

/* ── Sidebar radio — styled as nav menu ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
  display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap: 0 !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] {
  padding: 0 !important;
  margin: 0 !important;
}
/* Hide the actual radio circle dot */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
  display: none !important;
}
/* Each option label */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  display: flex !important;
  align-items: center !important;
  width: 100% !important;
  padding: 12px 20px !important;
  margin: 0 !important;
  border-radius: 0 !important;
  cursor: pointer !important;
  font-size: 13px !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 500 !important;
  color: rgba(255,255,255,0.65) !important;
  border-left: 3px solid transparent !important;
  transition: background 0.13s ease, color 0.13s ease !important;
  background: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,0.08) !important;
  color: rgba(255,255,255,0.92) !important;
}
/* Selected item */
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] div[data-baseweb="radio"]:has(input:checked) label {
  background: rgba(200,169,81,0.15) !important;
  color: var(--gold-lt) !important;
  border-left: 3px solid var(--gold) !important;
  font-weight: 700 !important;
}
            
/* Make header always on top */
.nw-header {
  position: fixed;
  top: 0;
  left: 220px;  /* same as sidebar width */
  right: 0;
  z-index: 9999;
}
.nw-header-left { display:flex; align-items:center; gap:14px; }
.nw-eagle {
  width:32px; height:32px;
  background:rgba(255,255,255,0.15);
  border:1px solid rgba(255,255,255,0.22);
  border-radius:7px;
  display:flex; align-items:center; justify-content:center;
  font-size:17px;
}
.nw-brand { font-family:'Libre Baskerville',serif; font-size:16px; color:#fff; }
.nw-brand span { color:var(--gold-lt); }
.nw-sep { width:1px; height:18px; background:rgba(255,255,255,0.18); }
.nw-pgname { font-size:12px; font-weight:500; color:rgba(255,255,255,0.68); }
.nw-right { font-size:10px; color:rgba(255,255,255,0.35); letter-spacing:1.2px; text-transform:uppercase; }

.gold-line {
  height:3px;
  background:linear-gradient(90deg,var(--gold) 0%,var(--gold-lt) 45%,transparent 100%);
  margin:0 -40px 32px;
}

/* ── SECTION LABEL ── */
.sec-label {
  font-size:10px; font-weight:700;
  letter-spacing:2.2px; text-transform:uppercase;
  color:var(--nw-blue);
  display:flex; align-items:center; gap:10px;
  margin:0 0 16px;
}
.sec-label::after { content:''; flex:1; height:1px; background:var(--border); }

/* ── FIELD LABEL ── */
.f-label { font-size:10px; font-weight:700; letter-spacing:1.8px; text-transform:uppercase; color:var(--nw-blue); margin:0 0 8px; }
.f-hint  { font-size:10px; color:var(--muted); margin:5px 0 0; }
.f-ok    { font-size:10px; color:var(--ok-fg); margin:5px 0 0; }

/* ── FILE CHIP ── */
.chip-ok {
  display:inline-flex; align-items:center; gap:4px;
  background:var(--ok-bg); border:1px solid #9ECDB0;
  border-radius:5px; padding:2px 8px;
  font-size:10px; color:var(--ok-fg); font-weight:600;
  max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}
.chip-none {
  display:inline-flex; align-items:center; gap:4px;
  border:1px dashed var(--border); border-radius:5px; padding:2px 8px;
  font-size:10px; color:var(--muted);
}

/* ── FILE UPLOADER compact ── */
[data-testid="stFileUploader"] {
  background:var(--surface) !important;
  border:1.5px dashed var(--border) !important;
  border-radius:7px !important;
}
[data-testid="stFileUploader"] section { padding:6px 10px !important; min-height:unset !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { display:none !important; }
[data-testid="stFileUploaderDropzone"] { padding:4px !important; }
[data-testid="stFileUploaderDropzone"] > div { flex-direction:row !important; align-items:center !important; gap:8px !important; }
[data-testid="stFileUploaderDropzone"] button {
  font-size:10px !important; font-weight:600 !important;
  padding:4px 10px !important; border-radius:5px !important;
  white-space:nowrap !important; min-height:unset !important;
  background:var(--nw-blue) !important; color:#fff !important; border:none !important;
}
[data-testid="stFileUploaderDropzone"] button:hover { background:var(--nw-deep) !important; }
[data-testid="stFileUploadedFile"] { padding:3px 6px !important; font-size:10px !important; }

/* ── WIDGET LABELS ── */
label[data-testid="stWidgetLabel"] p {
  font-size:10px !important; font-weight:700 !important;
  letter-spacing:1.5px !important; text-transform:uppercase !important;
  color:var(--nw-blue) !important; margin-bottom:4px !important;
}

/* ── TEXT / NUMBER INPUT ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
  border:1.5px solid var(--border) !important;
  border-radius:7px !important; background:var(--surface) !important;
  font-family:'Inter',sans-serif !important; font-size:13px !important;
  color:var(--text) !important; padding:9px 12px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
  border-color:var(--nw-blue) !important;
  box-shadow:0 0 0 3px rgba(26,93,171,0.10) !important;
  outline:none !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] { padding:4px 0 !important; }
[data-baseweb="slider"] div[role="slider"] {
  background:var(--nw-blue) !important;
  border:2px solid #fff !important;
  box-shadow:0 0 0 2px var(--nw-blue) !important;
  width:18px !important; height:18px !important;
}
[data-baseweb="slider"] div[role="progressbar"] { background:var(--nw-blue) !important; }

/* ── EXPANDER ── */
[data-testid="stExpander"] {
  border:1px solid var(--border) !important;
  border-radius:var(--radius) !important;
  background:var(--surface) !important;
  box-shadow:var(--shadow) !important;
  margin-bottom:0 !important;
}
details summary {
  font-family:'Inter',sans-serif !important;
  font-size:10px !important; font-weight:700 !important;
  letter-spacing:2px !important; text-transform:uppercase !important;
  color:var(--nw-blue) !important; padding:13px 20px !important;
}
details[open] summary { border-bottom:1px solid var(--border); }

/* ── READINESS CARD ── */
.rdy-card { border:1px solid var(--border); border-radius:var(--radius); background:var(--surface); padding:8px 16px 4px; margin-bottom:22px; }
.rdy-row  { display:flex; align-items:flex-start; gap:11px; padding:11px 0; border-bottom:1px solid var(--border); }
.rdy-row:last-child { border-bottom:none; padding-bottom:6px; }
.rdy-dot  { width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; flex-shrink:0; margin-top:1px; }
.dot-ok   { background:var(--ok-bg);  color:var(--ok-fg); }
.dot-wait { background:var(--nw-lt);  color:var(--nw-blue); }
.rdy-title { font-size:12px; font-weight:600; color:var(--text); line-height:1.4; }
.rdy-sub   { font-size:10px; color:var(--muted); margin-top:2px; }

/* ── RUN BUTTON ── */
div.btn-ready > div > button {
  background:linear-gradient(135deg,var(--nw-deep) 0%,var(--nw-blue) 100%) !important;
  color:#fff !important; border:none !important; border-radius:9px !important;
  font-weight:700 !important; font-size:13px !important;
  letter-spacing:0.5px !important; padding:13px 28px !important;
  width:100% !important; box-shadow:0 4px 18px rgba(13,63,122,0.28) !important;
  transition:all 0.18s !important;
}
div.btn-ready > div > button:hover {
  background:linear-gradient(135deg,#0a2f5e 0%,var(--nw-deep) 100%) !important;
  box-shadow:0 7px 26px rgba(13,63,122,0.36) !important;
  transform:translateY(-1px) !important;
}
div.btn-wait > div > button {
  background:var(--border) !important; color:var(--muted) !important;
  border:none !important; border-radius:9px !important;
  font-weight:600 !important; font-size:13px !important;
  padding:13px 28px !important; width:100% !important; box-shadow:none !important;
}

/* ── SECONDARY BUTTON ── */
.stButton > button[kind="secondary"] {
  background:transparent !important; color:var(--nw-blue) !important;
  border:1.5px solid var(--border) !important; border-radius:7px !important;
  font-size:11px !important; font-weight:500 !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color:var(--nw-blue) !important; background:var(--nw-lt) !important;
}

[data-testid="stAlert"] { border-radius:8px !important; font-size:12px !important; }
[data-testid="column"]  { padding: 0 6px !important; }

/* ── COMING SOON placeholder ── */
.coming-soon {
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding: 80px 32px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  text-align: center;
  margin-top: 24px;
}
.coming-soon .cs-icon  { font-size:52px; margin-bottom:16px; }
.coming-soon .cs-title { font-family:'Libre Baskerville',serif; font-size:22px; font-weight:700; color:var(--nw-deep); margin-bottom:8px; }
.coming-soon .cs-sub   { font-size:13px; color:var(--muted); max-width:380px; line-height:1.6; }
.coming-soon .cs-tag   {
  margin-top:20px; display:inline-block;
  background:var(--nw-lt); color:var(--nw-blue);
  border:1px solid var(--border); border-radius:20px;
  font-size:10px; font-weight:700; letter-spacing:1.5px;
  text-transform:uppercase; padding:5px 14px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  — collapsible, LOB navigation
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Brand block
    st.markdown("""
    <div style="padding:24px 20px 18px; border-bottom:1px solid rgba(255,255,255,0.1);">
      <div style="font-family:'Libre Baskerville',serif; font-size:17px;
                  color:#ffffff; line-height:1; margin-bottom:3px;">
        Nationwide <span style="color:#EDD97A;">Insurance</span>
      </div>
      <div style="font-size:9px; font-weight:700; letter-spacing:2px;
                  text-transform:uppercase; color:rgba(255,255,255,0.35); margin-top:4px;">
        BA Analytics Platform
      </div>
    </div>
    <div style="padding:14px 20px 8px; font-size:9px; font-weight:700;
                letter-spacing:2px; text-transform:uppercase;
                color:rgba(255,255,255,0.30);">
      Line of Business
    </div>
    """, unsafe_allow_html=True)

    # LOB radio — this is the ONLY reliable way to get persistent selected state in Streamlit
    LOB_OPTIONS = [
        "🚗  Business Auto",
        "⚖️  General Liability",
        "🚜  Farm Auto",
        "🏠  Property",
    ]
    LOB_NAMES = ["Business Auto", "General Liability", "Farm Auto", "Property"]

    current_idx = LOB_NAMES.index(st.session_state.lob) if st.session_state.lob in LOB_NAMES else 0

    selected_option = st.radio(
        "lob_nav",
        options=LOB_OPTIONS,
        index=current_idx,
        key="lob_radio",
        label_visibility="collapsed",
    )

    new_lob = LOB_NAMES[LOB_OPTIONS.index(selected_option)]
    if new_lob != st.session_state.lob:
        st.session_state.lob        = new_lob
        st.session_state.run_status = "idle"
        st.rerun()

    # # Footer links
    # st.markdown("""
    # <div style="position:absolute; bottom:0; left:0; right:0;
    #             padding:16px 20px; border-top:1px solid rgba(255,255,255,0.08);">
    #   <div style="font-size:10px; color:rgba(255,255,255,0.30);
    #               line-height:2; letter-spacing:0.5px;">
    #     ❓ &nbsp;Support<br>
    #     📄 &nbsp;Documentation
    #   </div>
    # </div>
    # """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER  (same across all LOBs)
# ══════════════════════════════════════════════════════════════════════════════
active_lob = st.session_state.lob

lob_subtitles = {
    "Business Auto":     "Upload proposed ratebooks · Configure options · Generate output",
    "General Liability": "General Liability rate page configuration",
    "Farm Auto":         "Farm Auto rate page configuration",
    "Property":          "Property rate page configuration",
}
lob_icons = {
    "Business Auto":     "🚗",
    "General Liability": "⚖️",
    "Farm Auto":         "🚜",
    "Property":          "🏠",
}

st.markdown(f"""
<div class="nw-header">
  <div class="nw-header-left">
    <div class="nw-eagle">🦅</div>
    <div class="nw-brand">Nationwide <span>Insurance</span></div>
    <div class="nw-sep"></div>
    <div class="nw-pgname">{lob_icons[active_lob]} &nbsp;{active_lob} · Rate Page Builder</div>
  </div>
  <div class="nw-right">BA &nbsp;·&nbsp; Analytics &nbsp;·&nbsp; Internal Tool</div>
</div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADING
# ══════════════════════════════════════════════════════════════════════════════
h1, h2 = st.columns([3, 1])
with h1:
    st.markdown(f"""
    <p style="font-family:'Libre Baskerville',serif;font-size:25px;font-weight:700;
              color:#0D3F7A;margin:0 0 5px;">Build {active_lob} Rate Pages</p>
    <p style="font-size:13px;color:#6B7A9E;margin:0;">{lob_subtitles[active_lob]}</p>
    """, unsafe_allow_html=True)

with h2:
    if active_lob == "Business Auto":
        nr = n_req(); tot = len(REQUIRED); pct = int(nr / tot * 100)
        fg = "#196B38" if nr == tot else "#1A5DAB"
        st.markdown(f"""
        <div style="text-align:right;padding-top:4px;">
          <div style="font-size:10px;color:#6B7A9E;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:5px;">Required Files</div>
          <div style="font-size:28px;font-weight:700;color:{fg};line-height:1;font-family:'Libre Baskerville',serif;">
            {nr}<span style="font-size:13px;font-weight:400;color:#6B7A9E;">/{tot}</span>
          </div>
          <div style="background:#D4DFEF;border-radius:3px;height:3px;margin-top:8px;overflow:hidden;">
            <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,#0D3F7A,#1A5DAB);border-radius:3px;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

spacer(28)


# ══════════════════════════════════════════════════════════════════════════════
# BUSINESS AUTO  — full real UI
# ══════════════════════════════════════════════════════════════════════════════
if active_lob == "Business Auto":

    L, R = st.columns([13, 7], gap="large")

    # ── LEFT: Ratebook uploads ────────────────────────────────────────────────
    with L:
        st.markdown('<div class="sec-label">📂 &nbsp;Proposed Ratebooks</div>', unsafe_allow_html=True)

        nr_loaded = n_req()
        with st.expander(f"REQUIRED RATEBOOKS  ·  {nr_loaded} of {len(REQUIRED)} loaded", expanded=True):
            spacer(6)
            r1 = st.columns(4)
            r2 = st.columns(4)
            for idx, key in enumerate(REQUIRED):
                row, col = divmod(idx, 4)
                with [r1, r2][row][col]:
                    up = st.file_uploader(key, type=["xlsx","xlsm","xls"],
                                          key=f"up_{key}", label_visibility="visible")
                    if up:
                        st.session_state[f"file_{key}"] = up
                    st.markdown(chip(st.session_state[f"file_{key}"]), unsafe_allow_html=True)
                    spacer(4)

        spacer(10)

        n_cw = bool(st.session_state["file_CW"])
        with st.expander(
            f"OPTIONAL  ·  CW RATEBOOK  {'— Loaded ✓' if n_cw else '— Not loaded'}",
            expanded=True
        ):
            spacer(6)
            cw_c, _, _ = st.columns([1, 1, 1])
            with cw_c:
                cw_up = st.file_uploader("CW", type=["xlsx","xlsm","xls"],
                                         key="up_CW", label_visibility="visible")
                if cw_up:
                    st.session_state["file_CW"] = cw_up
                st.markdown(chip(st.session_state["file_CW"]), unsafe_allow_html=True)
            spacer(6)

        if any(st.session_state[f"file_{k}"] for k in ALL_KEYS):
            spacer(6)
            _, clr = st.columns([5, 1])
            with clr:
                if st.button("Clear all", type="secondary"):
                    for k in ALL_KEYS:
                        st.session_state[f"file_{k}"] = None
                    st.session_state.run_status = "idle"
                    st.rerun()

    # ── RIGHT: Config + Readiness + Run ───────────────────────────────────────
    with R:
        st.markdown('<div class="sec-label">⚙ &nbsp;Configuration</div>', unsafe_allow_html=True)

        # Save Location
        st.markdown('<p class="f-label">📁 &nbsp;Save Location</p>', unsafe_allow_html=True)
        typed = st.text_input(
            "save_path", value=st.session_state.save_dir,
            placeholder="Paste path or click Browse",
            label_visibility="collapsed",
        )
        if typed != st.session_state.save_dir:
            st.session_state.save_dir = typed

        if st.button("📂  Browse", key="browse_btn"):
            folder = browse_folder()
            if folder:
                st.session_state.save_dir = folder
                st.rerun()

        if st.session_state.save_dir:
            p = st.session_state.save_dir
            display = ("…" + p[-38:]) if len(p) > 40 else p
            st.markdown(f'<p class="f-ok">✓ &nbsp;{display}</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="f-hint">Browse your device or paste the full folder path</p>', unsafe_allow_html=True)

        spacer(6)

        # Schedule Rating Mod
        st.markdown('<p class="f-label">📊 &nbsp;Schedule Rating Mod</p>', unsafe_allow_html=True)
        num_col, pct_col = st.columns([3, 1])
        with num_col:
            typed_mod = st.number_input(
                "mod_num", min_value=0, max_value=100,
                value=st.session_state.sched_mod, step=1,
                label_visibility="collapsed",
            )
            if typed_mod != st.session_state.sched_mod:
                st.session_state.sched_mod = int(typed_mod)
        with pct_col:
            st.markdown(
                f"""<div style="display:flex;align-items:center;height:42px;padding-left:4px;">
                    <span style="font-size:22px;font-weight:700;color:#1A5DAB;line-height:1;">
                      {st.session_state.sched_mod}
                      <span style="font-size:13px;font-weight:400;color:#6B7A9E;">%</span>
                    </span></div>""",
                unsafe_allow_html=True,
            )

        spacer(6)

        slider_val = st.slider(
            "mod_slider", min_value=0, max_value=100,
            value=st.session_state.sched_mod,
            step=1, format="%d%%",
            label_visibility="collapsed",
        )
        if slider_val != st.session_state.sched_mod:
            st.session_state.sched_mod = slider_val
            st.rerun()

        st.markdown(
            '<p class="f-hint">Rule 417 · State Schedule Rating Maximum Modification Threshold</p>',
            unsafe_allow_html=True,
        )

        spacer(6)

        # Readiness
        st.markdown('<div class="sec-label">📋 &nbsp;Readiness</div>', unsafe_allow_html=True)

        req_ok   = all_req()
        save_ok  = bool(st.session_state.save_dir)
        nr_now   = n_req()
        save_dir_val = st.session_state.save_dir
        mod_val  = st.session_state.sched_mod

        req_sub  = f"All {len(REQUIRED)} ratebooks selected" if req_ok else f"{len(REQUIRED) - nr_now} file(s) still needed"
        save_sub = (("…" + save_dir_val[-36:]) if len(save_dir_val) > 38 else save_dir_val) if save_ok else "Not yet selected"

        def rdy_html(ok, title, subtitle):
            dot = "dot-ok" if ok else "dot-wait"
            icon = "✓" if ok else "○"
            return (
                f'<div class="rdy-row">'
                f'  <div class="rdy-dot {dot}">{icon}</div>'
                f'  <div><div class="rdy-title">{title}</div>'
                f'  <div class="rdy-sub">{subtitle}</div></div>'
                f'</div>'
            )

        req_title = f'Ratebooks &nbsp;<span style="font-size:10px;color:#6B7A9E;font-weight:400;">{nr_now}/{len(REQUIRED)}</span>'
        mod_title = f'Schedule Mod &nbsp;<span style="font-size:10px;color:#6B7A9E;font-weight:400;">{mod_val}%</span>'

        st.markdown(
            '<div class="rdy-card">'
            + rdy_html(req_ok,  req_title, req_sub)
            + rdy_html(save_ok, "Save location", save_sub)
            + rdy_html(True,    mod_title, "Rule 417 threshold")
            + '</div>',
            unsafe_allow_html=True,
        )

        # Run button
        ready = req_ok and save_ok
        if ready:
            st.markdown('<div class="btn-ready">', unsafe_allow_html=True)
            run = st.button("🦅  Create Rate Pages", key="run_btn", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            missing = []
            if not req_ok:  missing.append(f"{len(REQUIRED) - nr_now} ratebook(s)")
            if not save_ok: missing.append("save location")
            st.markdown('<div class="btn-wait">', unsafe_allow_html=True)
            st.button(
                f"⚠  Waiting — {', '.join(missing)}",
                key="run_btn_dis", use_container_width=True, disabled=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
            run = False

        if st.session_state.run_status == "success":
            spacer(10)
            st.success("✓  Rate pages created successfully.")
        elif st.session_state.run_status == "error":
            spacer(10)
            st.error(st.session_state.run_msg)

        spacer(24)
        st.markdown("""
        <div style="padding-top:14px;border-top:1px solid var(--border);">
          <p style="font-size:10px;color:#8892A4;letter-spacing:0.8px;
                    text-transform:uppercase;text-align:center;margin:0;line-height:1.9;">
            Nationwide Insurance &nbsp;·&nbsp; BA Analytics Division<br>Internal Use Only
          </p>
        </div>""", unsafe_allow_html=True)

    # ── Run logic ──────────────────────────────────────────────────────────────
    if run:
        st.warning("⚠️ Ensure all Excel files are **saved and closed** before continuing.")
        # ── Wire your real run() here ──
        # from BARatePages import run as run_rate_pages
        # try:
        #     run_rate_pages(
        #         NGICRatebook    = st.session_state["file_NGIC"],
        #         MMRatebook      = st.session_state["file_MM"],
        #         NACORatebook    = st.session_state["file_NACO"],
        #         NICOFRatebook   = st.session_state["file_NICOF"],
        #         NAFFRatebook    = st.session_state["file_NAFF"],
        #         HICNJRatebook   = st.session_state["file_HICNJ"],
        #         CCMICRatebook   = st.session_state["file_CCMIC"],
        #         NWAGRatebook    = st.session_state["file_NWAG"],
        #         folder_selected = st.session_state.save_dir,
        #         SchedRatingMod  = int(st.session_state.sched_mod) or None,
        #         CWRatebook      = st.session_state["file_CW"],
        #     )
        #     st.session_state.run_status = "success"
        # except Exception as e:
        #     st.session_state.run_status = "error"
        #     st.session_state.run_msg    = str(e)
        st.session_state.run_status = "success"   # placeholder — remove when wiring real run()
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# OTHER LOBs  — Coming Soon placeholders  (same structure, ready to wire up)
# ══════════════════════════════════════════════════════════════════════════════
else:
    cs_info = {
        "General Liability": {
            "icon": "⚖️",
            "title": "General Liability",
            "desc":  "GL ratebook uploads, territory factors, and ISO rating configuration will live here. Wire up your GL backend in the <code>elif active_lob == \"General Liability\"</code> block.",
            "tag":   "Coming Soon",
        },
        "Farm Auto": {
            "icon": "🚜",
            "title": "Farm Auto",
            "desc":  "Farm Auto ratebook processing including NAFF schedules and farm-specific territory modifiers. Wire up your FA backend in the <code>elif active_lob == \"Farm Auto\"</code> block.",
            "tag":   "Coming Soon",
        },
        "Property": {
            "icon": "🏠",
            "title": "Property",
            "desc":  "Property ratebook uploads, replacement cost factors, and state-specific endorsements will appear here. Wire up your Property backend in the <code>elif active_lob == \"Property\"</code> block.",
            "tag":   "Coming Soon",
        },
    }

    info = cs_info[active_lob]
    st.markdown(f"""
    <div class="coming-soon">
      <div class="cs-icon">{info["icon"]}</div>
      <div class="cs-title">{info["title"]} Rate Pages</div>
      <div class="cs-sub">{info["desc"]}</div>
      <div class="cs-tag">{info["tag"]}</div>
    </div>
    """, unsafe_allow_html=True)