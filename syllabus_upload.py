import streamlit as st
import base64
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Portal",
    page_icon="📚",
    layout="wide"
)

# --- CUSTOM STYLING & COLORFUL INSTITUTIONAL THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F5F9; }
    
    /* Vibrant Header Banner with Deep Blue & Gold Accents */
    .portal-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 15px -3px rgba(30, 58, 138, 0.3);
        border-bottom: 4px solid #F59E0B;
    }
    .portal-header h1 { color: #FFFFFF !important; margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: 0.5px; }
    .portal-header p { color: #E2E8F0; margin-top: 0.5rem; margin-bottom: 0; font-size: 1.1rem; font-weight: 400; }
    
    /* Card Styles */
    .card {
        background-color: #FFFFFF;
        padding: 1.8rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    
    /* Institutional Footer */
    .institutional-footer {
        background-color: #1E3A8A;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 10px;
        margin-top: 3rem;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
        border-top: 3px solid #F59E0B;
    }
    .institutional-footer p { margin: 0.3rem 0; color: #F8FAFC; font-size: 0.9rem; }
    .visitor-counter { margin-top: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER WITH LOGO INTEGRATION ---
col_logo, col_title = st.columns([1, 5])

with col_logo:
    # Check if local logo file exists, otherwise use a placeholder emoji/icon
    logo_path = Path("logo_pjc copy.jpg")
    if logo_path.exists():
        st.image(str(logo_path), width=110)
    else:
        st.markdown("### 🏛️ PJC")

with col_title:
    st.markdown("""
        <div class="portal-header" style="margin-bottom: 0; padding: 1.2rem;">
            <h1>Prabhu Jagatbandhu College</h1>
            <p>Academic Repository & Syllabus Management Portal</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab_browse, tab_upload = st.tabs(["📂 Browse Repository & Syllabi", "📤 Upload New Materials"])

# --- TAB 1: BROWSE AVAILABLE SYLLABI & STUDY MATERIALS ---
with tab_browse:
    st.markdown("### 🔍 Filter & Explore Academic Resources")
    
    # Filter Controls
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_category = st.selectbox("Select Category", ["All", "Syllabus", "Study Material"])
    with f_col2:
        selected_dept = st.selectbox("Select Department", [
            "All Departments", "Bengali", "English", "Philosophy", "History", 
            "Geography", "Economics", "Physical Education", "Physics", 
            "Chemistry", "Mathematics", "Commerce"
        ])
    
    st.markdown("---")
    
    # Mock / Dynamic Display of Files (Connected to your Drive mapping structure)
    # In full dynamic mode, you can query Google Drive API using your folder IDs here.
    st.info(f"Showing repository files for **{selected_dept}** under category: **{selected_category}**")
    
    # Example dynamic table display matching your specifications format
    sample_data = [
        {"Department": "Physics", "Category": "Syllabus", "Title": "CCF Physics Core Syllabus 2026", "Uploaded": "2026-11-06", "File ID": "1LTh4Wag8BU1VTLACnYir-0voANQSD9Ky"},
        {"Department": "Bengali", "Category": "Study Material", "Title": "Adhunik Kabita Notes - Semester V", "Uploaded": "2026-11-05", "File ID": "1vGTsX5d8drocNRfXG_DZjKkB3egI8TLd"},
        {"Department": "Mathematics", "Category": "Syllabus", "Title": "B.Sc. Mathematics Honours Curriculum", "Uploaded": "2026-10-28", "File ID": "1NJl9U9cGVdEPwz--vV3Di2kgzP8iipYW"}
    ]
    
    # Filter logic
    filtered_items = [
        item for item in sample_data 
        if (selected_category == "All" or item["Category"] == selected_category) and
           (selected_dept == "All Departments" or item["Department"] == selected_dept)
    ]
    
    if filtered_items:
        for item in filtered_items:
            with st.container():
                st.markdown(f"""
                    <div class="card" style="padding: 1rem 1.5rem; margin-bottom: 0.8rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="background: #1E3A8A; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">{item['Department']}</span>
                                <span style="background: #059669; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 6px;">{item['Category']}</span>
                                <h4 style="margin: 0.5rem 0 0.2rem 0; color: #1E293B;">{item['Title']}</h4>
                                <small style="color: #64748B;">Uploaded on: {item['Uploaded']}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No files found matching the selected filters.")

# --- TAB_UPLOAD: SECURE UPLOAD FORM ---
with tab_upload:
    st.markdown("### 🚀 Secure Material Submission")
    st.markdown("""
        <div class="card">
            <p style="color: #334155; margin-bottom: 1.2rem;">
               Use the secure Google Form portal below to upload new syllabi or departmental notes. 
               Our automated Apps Script backend will instantly route your files to the corresponding Google Drive folder.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    FORM_DIRECT_URL = "https://forms.gle/Uk4AcdHTUL67wQ3f7"
    
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        st.link_button("🚀 Open Secure Upload Portal", FORM_DIRECT_URL, use_container_width=True)

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
