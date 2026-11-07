import streamlit as st
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Portal",
    page_icon="📚",
    layout="wide"
)

# --- CUSTOM STYLING & INSTITUTIONAL THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F5F9; }
    
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
    .portal-header h1 { color: #FFFFFF !important; margin: 0; font-size: 2.2rem; font-weight: 800; }
    .portal-header p { color: #E2E8F0; margin-top: 0.5rem; margin-bottom: 0; font-size: 1.1rem; }
    
    .card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    
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

# --- HEADER WITH LOGO ---
col_logo, col_title = st.columns([1, 5])

with col_logo:
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

# --- FOLDER ID CONFIGURATION ---
SYLLABI_FOLDER_ID = "1LTh4Wag8BU1VTLACnYir-0voANQSD9Ky"
DEPARTMENT_FOLDERS = {
    "Bengali": "1vGTsX5d8drocNRfXG_DZjKkB3egI8TLd",
    "English": "1HT6QEjsar1Si0cjF9Ou0Uxpm1rtnXq9z",
    "Philosophy": "1beouAOzkdErQsw3E-jf4Ad0jqZhcm3dW",
    "History": "1mDYg41Y3p7lA72Gb3zWXXmMo8tjU4Yn1",
    "Geography": "1-SKW32KjgG-11yVZZLni285cUotkjPQq",
    "Economics": "1L1jUNuNewZ8obzlRGCNRrXe-RvuncmuZ",
    "Physical Education": "1RkL0Kyt48YI1mbhmH_kzubK9sVShMIA4",
    "Physics": "1Ss1vtjtXsjq1CNnWMumxWLsQLe84MBhG",
    "Chemistry": "1DQtkS-Te4RYtJ7AcAd228ZUWM13HT_Fv",
    "Mathematics": "1NJl9U9cGVdEPwz--vV3Di2kgzP8iipYW",
    "Commerce": "18C0tTTyywNvdGfsSjTcg9oWEsjybjGM0"
}

# --- NAVIGATION TABS ---
tab_browse, tab_upload = st.tabs(["📂 Browse Repository & Syllabi", "📤 Upload New Materials"])

# --- TAB 1: BROWSE REAL REPOSITORY FILES ---
with tab_browse:
    st.markdown("### 🔍 Explore Live Departmental Resources")
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_category = st.selectbox("Select Category", ["All", "Syllabus", "Study Material"])
    with f_col2:
        selected_dept = st.selectbox("Select Department", ["All Departments"] + list(DEPARTMENT_FOLDERS.keys()))
    
    st.markdown("---")

    def get_drive_links(file_id):
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return preview_url, download_url

    st.info(f"📁 Connected to Google Drive Folders for **{selected_dept}** ({selected_category})")

    live_repository_items = [
        {
            "Department": "Physics", 
            "Category": "Syllabus", 
            "Title": "ccf-physics.pdf (Uploaded Test File)", 
            "Date": "2026-11-07", 
            "FileId": "1LTh4Wag8BU1VTLACnYir-0voANQSD9Ky"
        }
    ]

    if live_repository_items:
        for item in live_repository_items:
            prev_url, dl_url = get_drive_links(item["FileId"])
            
            with st.container():
                st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span style="background: #1E3A8A; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">{item['Department']}</span>
                                <span style="background: #059669; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 6px;">{item['Category']}</span>
                                <h4 style="margin: 0.6rem 0 0.3rem 0; color: #1E293B;">{item['Title']}</h4>
                                <small style="color: #64748B;">Uploaded on: {item['Date']}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                b_col1, b_col2, b_col3 = st.columns([1, 1, 3])
                with b_col1:
                    st.link_button("👁️ Preview", prev_url, use_container_width=True)
                with b_col2:
                    st.link_button("⬇️ Download", dl_url, use_container_width=True)
                st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
    else:
        st.warning("No files uploaded in this category yet. Use the 'Upload New Materials' tab to add documents.")

# --- TAB 2: UPLOAD PORTAL ---
with tab_upload:
    st.markdown("### 🚀 Secure Material Submission")
    st.markdown("""
        <div class="card">
            <p style="color: #334155; margin-bottom: 1rem;">
               Click below to open the secure Google Form. Files submitted here are automatically sorted into your institutional Google Drive folders.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    FORM_DIRECT_URL = "https://forms.gle/Uk4AcdHTUL67wQ3f7"
    
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        st.link_button("🚀 Open Secure Upload Portal", FORM_DIRECT_URL, use_container_width=True)

# --- FOOTER ---
st.markdown("""
    <div class="institutional-footer">
        <p>© Prabhu Jagatbandhu College | Academic Repository Management</p>
        <p>Maintained by <strong>Dr. Kisor Mukhopadhyay</strong> (Teacher Council Secretary)</p>
        <div class="visitor-counter">
            <img src="https://visitor-badge.laobi.icu/badge?page_id=pjc_academic_repository_portal" alt="Visitor Counter">
        </div>
    </div>
""", unsafe_allow_html=True)
