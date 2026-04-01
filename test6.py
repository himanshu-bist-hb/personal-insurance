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

# ── helpers ───────────────────────────────────────────────────────────────────
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

# ── CSS (FIXED HEADER ISSUE INCLUDED) ─────────────────────────────────────────
st.markdown("""
<style>

/* MAIN FIX */
.block-container {
  max-width: 100% !important;
  padding: 0 40px 64px !important;
  position: relative;
  z-index: 1;
  margin-top: 64px;
}

.nw-header {
  position: fixed;
  top: 0;
  left: 220px;
  right: 0;
  z-index: 9999;
  background: #1A5DAB;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  color: white;
}

[data-testid="stSidebar"] {
  z-index: 10000;
}

body {
  background: #F4F7FB;
}

</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Nationwide Insurance")
    lob = st.radio("LOB", ["Business Auto", "General Liability"])

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nw-header">
  <div>🦅 Nationwide Insurance</div>
  <div>Internal Tool</div>
</div>
""", unsafe_allow_html=True)

# ── MAIN UI ──────────────────────────────────────────────────────────────────
st.title("Build Business Auto Rate Pages")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Upload Files")
    st.file_uploader("Upload Excel", type=["xlsx"])

with col2:
    st.subheader("Configuration")
    path = st.text_input("Save Path")
    if st.button("Browse"):
        folder = browse_folder()
        if folder:
            st.success(folder)

st.button("Create Rate Pages")
