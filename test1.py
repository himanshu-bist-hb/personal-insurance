import streamlit as st

st.set_page_config(page_title="Master Ratebook", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>

/* Hide default uploader completely */
[data-testid="stFileUploader"] {
    position: absolute;
    opacity: 0;
    height: 0;
}

/* Title styling */
.title {
    font-size: 26px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 4px;
}

.subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 20px;
}

/* Upload Box */
.upload-box {
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    padding: 25px;
    background-color: #f1f5f9;
    cursor: pointer;
    transition: 0.2s ease;
}

.upload-box:hover {
    background-color: #e2e8f0;
}

/* Row layout */
.upload-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Left text */
.upload-main {
    font-size: 15px;
    color: #334155;
}

.upload-sub {
    font-size: 12px;
    color: #64748b;
}

/* Button */
.browse-btn {
    background-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">Master Ratebook</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Excel/CSV</div>', unsafe_allow_html=True)

# ---------- HIDDEN FILE INPUT ----------
uploaded_file = st.file_uploader(
    "Upload",
    type=["xlsx", "xls", "csv"],
    label_visibility="collapsed"
)

# ---------- CUSTOM UI ----------
st.markdown("""
<label for="fileUploader">
<div class="upload-box">
    <div class="upload-row">
        <div>
            <div class="upload-main">📤 Drag and drop file here</div>
            <div class="upload-sub">Limit 200MB per file • XLSX, XLS, CSV</div>
        </div>
        <div class="browse-btn">Browse files</div>
    </div>
</div>
</label>
""", unsafe_allow_html=True)

# ---------- RESULT ----------
if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")