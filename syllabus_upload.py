import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Upload Portal",
    page_icon="📚",
    layout="wide"
)

# --- CUSTOM STYLING & INSTITUTIONAL DEEP BLUE THEME ---
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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .portal-header h1 { color: #FFFFFF !important; margin: 0; font-size: 1.8rem; font-weight: 700; }
    .portal-header p { color: #E2E8F0; margin-top: 0.5rem; margin-bottom: 0; }
    
    .form-container {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }

    .institutional-footer {
        background-color: #1E3A8A;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 8px;
        margin-top: 2.5rem;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
    }
    .institutional-footer p { margin: 0.3rem 0; color: #F8FAFC; font-size: 0.9rem; }
    .visitor-counter { margin-top: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class="portal-header">
        <h1>Prabhu Jagatbandhu College</h1>
        <p>Academic Repository Upload Portal — Syllabi & Departmental Study Materials</p>
    </div>
""", unsafe_allow_html=True)

# --- CONFIGURATION & LINKS ---
FORM_EMBED_URL = "https://docs.google.com/forms/d/e/1FAIpQLSffjHfJolpUmj58B1Xw-OTSRpfWfc1HvbRkE4o-LEX_nhx20g/viewform?embedded=true"
FORM_DIRECT_URL = "https://forms.gle/Uk4AcdHTUL67wQ3f7"

# Instructions & Fallback Action Button
col1, col2 = st.columns([3, 1])
with col1:
    st.info("ℹ️ Select your Category and Department below to automatically route your files to the right Google Drive folder.")
with col2:
    st.link_button("🔗 Open Form in New Tab", FORM_DIRECT_URL, use_container_width=True)

# --- EMBEDDED GOOGLE FORM ---
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

# --- CENTERED DEEP BLUE FOOTER WITH VISITOR COUNTER ---
st.markdown("""
    <div class="institutional-footer">
        <p>© Prabhu Jagatbandhu College | Academic Repository Management</p>
        <p>Maintained by <strong>Dr. Kisor Mukhopadhyay</strong> (Teacher Council Secretary)</p>
        <div class="visitor-counter">
            <img src="https://visitor-badge.laobi.icu/badge?page_id=pjc_academic_repository_portal" alt="Visitor Counter">
        </div>
    </div>
""", unsafe_allow_html=True)
