import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Upload Portal",
    page_icon="📚",
    layout="centered"
)

# --- CUSTOM STYLING & INSTITUTIONAL DEEP BLUE THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .portal-header {
        background-color: #1E3A8A;
        padding: 2rem 1.5rem;
        border-radius: 10px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .portal-header h1 { color: #FFFFFF !important; margin: 0; font-size: 2rem; font-weight: 700; }
    .portal-header p { color: #E2E8F0; margin-top: 0.5rem; margin-bottom: 0; font-size: 1.05rem; }
    
    .action-card {
        background-color: #FFFFFF;
        padding: 2.5rem 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .action-card h3 { color: #1E3A8A; margin-top: 0; }
    .action-card p { color: #475569; font-size: 1rem; margin-bottom: 1.5rem; }

    .institutional-footer {
        background-color: #1E3A8A;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 10px;
        margin-top: 3rem;
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
FORM_DIRECT_URL = "https://forms.gle/Uk4AcdHTUL67wQ3f7"

# --- CENTRAL SUBMISSION CARD ---
st.markdown("""
    <div class="action-card">
        <h3>📄 Submit Academic Materials</h3>
        <p>Click the secure portal button below to upload your Departmental Study Materials or Syllabi. 
           Files submitted through the form are automatically sorted and routed to the correct Google Drive folders.</p>
    </div>
""", unsafe_allow_html=True)

# Centered large action button for submission
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.link_button("🚀 Open Secure Upload Portal", FORM_DIRECT_URL, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("ℹ️ **Note:** Submissions open in a secure Google Form tab to ensure smooth file uploads and seamless Google account authentication.")

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
