import streamlit as st
import pandas as pd
import re
from pathlib import Path
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Portal",
    page_icon="📚",
    layout="wide"
)

# --- HELPER: BASE64 LOGO ENCODER ---
def get_base64_image(image_path):
    p = Path(image_path)
    if p.exists():
        with open(p, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = get_base64_image("logo_pjc copy.jpg")
logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="height: 75px; width: auto; margin-right: 1.5rem; border-radius: 6px; background: white; padding: 4px;">' if logo_b64 else '<div style="font-size: 2.2rem; margin-right: 1rem;">🏛️</div>'

# --- CUSTOM STYLING & INSTITUTIONAL THEME ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #F1F5F9; }}
    
    .portal-header {{
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 2rem;
        box-shadow: 0 6px 15px -3px rgba(30, 58, 138, 0.3);
        border-bottom: 4px solid #F59E0B;
    }}
    .portal-header-text h1 {{ color: #FFFFFF !important; margin: 0; font-size: 2.1rem; font-weight: 800; line-height: 1.2; }}
    .portal-header-text p {{ color: #E2E8F0; margin-top: 0.3rem; margin-bottom: 0; font-size: 1.05rem; }}
    
    /* Card Style with Half-Cover Saffron Top Accent */
    .card-item {{
        background: #FFFFFF;
        padding: 1.4rem 1.8rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        border-top: 4px solid #FF9933; /* Saffron/Orange Accent */
        border-top-width: 4px;
        position: relative;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    /* Pseudo-element to make the top accent cover exactly half (50%) of the box */
    .card-item::before {{
        content: "";
        position: absolute;
        top: -4px;
        left: 0;
        width: 50%;
        height: 4px;
        background-color: #FF7700; /* Rich Saffron */
        border-top-left-radius: 12px;
    }}

    .card-item:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(30, 58, 138, 0.1);
    }}
    
    .btn-preview {{
        background-color: #2563EB;
        color: white !important;
        padding: 0.55rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
        text-align: center;
        width: 100%;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        transition: background-color 0.2s;
    }}
    .btn-preview:hover {{
        background-color: #1D4ED8;
    }}
    
    .btn-download {{
        background-color: #059669;
        color: white !important;
        padding: 0.55rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
        text-align: center;
        width: 100%;
        box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
        transition: background-color 0.2s;
    }}
    .btn-download:hover {{
        background-color: #047857;
    }}
    
    .institutional-footer {{
        background-color: #1E3A8A;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 10px;
        margin-top: 3rem;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
        border-top: 3px solid #F59E0B;
    }}
    .institutional-footer p {{ margin: 0.3rem 0; color: #F8FAFC; font-size: 0.9rem; }}
    .visitor-counter {{ margin-top: 0.8rem; }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER WITH INTEGRATED LOGO ---
st.markdown(f"""
    <div class="portal-header">
        {logo_html}
        <div class="portal-header-text">
            <h1>Prabhu Jagatbandhu College</h1>
            <p>Academic Repository & Syllabus Management Portal</p>
        </div>
    </div>
""", unsafe_allow_html=True)

DEPARTMENT_FOLDERS = [
    "Bengali", "English", "Philosophy", "History", "Geography", 
    "Economics", "Physical Education", "Physics", "Chemistry", "Mathematics", "Commerce"
]

# --- LIVE PUBLISHED GOOGLE SHEET CSV URL ---
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTkBRxQ2SHSxD2u2S_0-ckK9j2a2D-gUXrIXAtGCTgYwuf2G5OlHAlQW8yoGZdMw5UiI0OeWPhIkP-u/pub?output=csv"

def extract_drive_id(value):
    if not value or pd.isna(value):
        return ""
    val_str = str(value).strip()
    
    match_d = re.search(r'/d/([a-zA-Z0-9_-]+)', val_str)
    if match_d:
        return match_d.group(1)
        
    match_id = re.search(r'id=([a-zA-Z0-9_-]+)', val_str)
    if match_id:
        return match_id.group(1)
        
    if re.match(r'^[a-zA-Z0-9_-]{25,}$', val_str):
        return val_str
        
    return val_str

@st.cache_data(ttl=60)
def load_uploaded_files():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = [str(col).strip().lower() for col in df.columns]
        return df
    except Exception:
        return pd.DataFrame()

# --- NAVIGATION TABS ---
tab_browse, tab_upload = st.tabs(["📂 Browse Repository & Syllabi", "📤 Upload New Materials"])

# --- TAB 1: BROWSE REPOSITORY ---
with tab_browse:
    st.markdown("### 🔍 Explore Live Departmental Resources")
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_category = st.selectbox("Select Category", ["All", "Syllabus", "Study Material"])
    with f_col2:
        selected_dept = st.selectbox("Select Department", ["All Departments"] + DEPARTMENT_FOLDERS)
    
    st.markdown("---")

    df_files = load_uploaded_files()

    if not df_files.empty:
        filtered_df = df_files.copy()
        
        cat_col = next((c for c in filtered_df.columns if "cat" in c or "type" in c), None)
        dept_col = next((c for c in filtered_df.columns if "dept" in c or "department" in c), None)
        title_col = next((c for c in filtered_df.columns if "title" in c or "file" in c or "name" in c or "upload" in c), None)
        date_col = next((c for c in filtered_df.columns if "date" in c or "time" in c or "timestamp" in c), None)
        id_col = next((c for c in filtered_df.columns if "id" in c or "link" in c or "url" in c or "file" in c or "upload" in c), None)

        if selected_category != "All" and cat_col:
            filtered_df = filtered_df[filtered_df[cat_col].astype(str).str.contains(selected_category, case=False, na=False)]
            
        if selected_dept != "All Departments" and dept_col:
            filtered_df = filtered_df[filtered_df[dept_col].astype(str).str.contains(selected_dept, case=False, na=False)]

        if not filtered_df.empty:
            for idx, row in filtered_df.iterrows():
                dept_val = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else "General"
                cat_val = str(row[cat_col]) if cat_col and pd.notna(row[cat_col]) else "Material"
                title_val = str(row[title_col]) if title_col and pd.notna(row[title_col]) else f"Document #{idx+1}"
                date_val = str(row[date_col]) if date_col and pd.notna(row[date_col]) else "Recent"
                
                raw_id_val = row[id_col] if id_col and pd.notna(row[id_col]) else ""
                clean_file_id = extract_drive_id(raw_id_val)

                if clean_file_id:
                    preview_url = f"https://drive.google.com/file/d/{clean_file_id}/view?usp=sharing"
                    download_url = f"https://drive.google.com/uc?export=download&id={clean_file_id}"
                else:
                    preview_url = "#"
                    download_url = "#"

                with st.container():
                    st.markdown('<div class="card-item">', unsafe_allow_html=True)
                    card_left, card_right = st.columns([3.5, 1.2])
                    
                    with card_left:
                        st.markdown(f"""
                            <div>
                                <span style="background: #1E3A8A; color: white; padding: 3px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">{dept_val}</span>
                                <span style="background: #059669; color: white; padding: 3px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; margin-left: 6px;">{cat_val}</span>
                                <h4 style="margin: 0.6rem 0 0.3rem 0; color: #1E293B;">{title_val}</h4>
                                <small style="color: #64748B;">Uploaded on: {date_val}</small>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with card_right:
                        st.markdown("<div style='margin-top: 0.4rem;'></div>", unsafe_allow_html=True)
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            st.markdown(f'<a href="{preview_url}" target="_blank" class="btn-preview">👁️ Preview</a>', unsafe_allow_html=True)
                        with btn_col2:
                            st.markdown(f'<a href="{download_url}" target="_blank" class="btn-download">⬇️ Download</a>', unsafe_allow_html=True)
                            
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No files found matching the selected filters.")
    else:
        st.info("No materials cataloged yet or waiting for response data. Use the 'Upload New Materials' tab to submit documents.")

# --- TAB 2: UPLOAD PORTAL ---
with tab_upload:
    st.markdown("### 🚀 Secure Material Submission")
    st.markdown("""
        <div class="card-item">
            <p style="color: #334155; margin-bottom: 1rem;">
               Click below to open the secure Google Form. Submissions automatically log to the master directory and update this repository portal in real-time.
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
