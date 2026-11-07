import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Upload Portal",
    page_icon="📚",
    layout="wide"
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .portal-header {
        background-color: #1E3A8A;
        padding: 1.5rem;
        border-radius: 8px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .portal-header h1 { color: #FFFFFF !important; margin: 0; font-size: 1.8rem; }
    .portal-header p { color: #E2E8F0; margin-top: 0.5rem; margin-bottom: 0; }
    .form-container {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    .institutional-footer {
        background-color: #1E3A8A;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 8px;
        margin-top: 2.5rem;
    }
    .institutional-footer p { margin: 0.3rem 0; color: #F8FAFC; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="portal-header">
        <h1>Prabhu Jagatbandhu College</h1>
        <p>Academic Repository Upload Portal — Syllabi & Departmental Study Materials</p>
    </div>
""", unsafe_allow_html=True)

# --- DIRECT LINK & EMBED ---
FORM_EMBED_URL = "https://docs.google.com/forms/d/e/1FAIpQLScUk4AcdHTUL67wQ3f7/viewform?embedded=true"
FORM_DIRECT_URL = "https://forms.gle/Uk4AcdHTUL67wQ3f7"

col1, col2 = st.columns([3, 1])
with col1:
    st.info("ℹ️ Select your Category and Department below to automatically route your files to the right Google Drive folder.")
with col2:
    st.link_button("🔗 Open Form in New Tab", FORM_DIRECT_URL, use_container_width=True)

# Embed Google Form iframe
st.markdown(f"""
    <div class="form-container">
        <iframe 
            src="{FORM_EMBED_URL}" 
            width="100%" 
            height="850" 
            frameborder="0" 
            marginheight="0" 
            marginwidth="0">
            Loading form...
        </iframe>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class="institutional-footer">
        <p>© Prabhu Jagatbandhu College | Academic Repository Management</p>
        <p>Maintained by <strong>Dr. Kisor Mukhopadhyay</strong> (Teacher Council Secretary)</p>
        <div style="margin-top: 0.8rem;">
            <img src="https://visitor-badge.laobi.icu/badge?page_id=pjc_academic_repository_portal" alt="Visitor Counter">
        </div>
    </div>
""", unsafe_allow_html=True)
