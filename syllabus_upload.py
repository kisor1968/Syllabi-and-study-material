import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Upload Portal",
    page_icon="📚",
    layout="wide"
)

# --- CUSTOM STYLING & FOOTER (Institutional Deep Blue Theme) ---
st.markdown("""
    <style>
    /* Main Theme & Header Styling */
    .stApp {
        background-color: #F8FAFC;
    }
    .portal-header {
        background-color: #1E3A8A;
        padding: 1.5rem;
        border-radius: 8px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .portal-header h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-weight: 700;
        font-size: 1.8rem;
    }
    .portal-header p {
        color: #E2E8F0;
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-size: 0.95rem;
    }

    /* Embedded Form Wrapper */
    .form-container {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }

    /* Centered Footer Styling */
    .institutional-footer {
        background-color: #1E3A8A;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 8px;
        margin-top: 2.5rem;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
    }
    .institutional-footer p {
        margin: 0.3rem 0;
        font-size: 0.9rem;
        color: #F8FAFC;
    }
    .visitor-counter {
        margin-top: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class="portal-header">
        <h1>Prabhu Jagatbandhu College</h1>
        <p>Academic Repository Upload Portal — Syllabi & Departmental Study Materials</p>
    </div>
""", unsafe_allow_html=True)

# --- GOOGLE FORM EMBED CONFIGURATION ---
# Appended ?embedded=true to ensure clean rendering inside the Streamlit container frame
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScUk4AcdHTUL67wQ3f7.../viewform?embedded=true" 
# Note: If your short link (forms.gle) doesn't load inside an iframe due to Google's X-Frame headers, 
# use the full Google Form edit/share URL ending with /viewform?embedded=true instead.

st.info("ℹ️ Please select the correct Category (Syllabus or Study Material) and Department in the form below. Uploaded files will automatically route into designated Google Drive folders.")

# Embed Google Form inside Streamlit
st.markdown(f"""
    <div class="form-container">
        <iframe 
            src="https://forms.gle/Uk4AcdHTUL67wQ3f7" 
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