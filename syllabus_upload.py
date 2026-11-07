import streamlit as st
import pandas as pd
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
        padding: 1.2rem 1.5rem;
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

DEPARTMENT_FOLDERS = [
    "Bengali", "English", "Philosophy", "History", "Geography", 
    "Economics", "Physical Education", "Physics", "Chemistry", "Mathematics", "Commerce"
]

# --- LIVE PUBLISHED GOOGLE SHEET CSV URL ---
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTkBRxQ2SHSxD2u2S_0-ckK9j2a2D-gUXrIXAtGCTgYwuf2G5OlHAlQW8yoGZdMw5UiI0OeWPhIkP-u/pub?output=csv"

@st.cache_data(ttl=60)
def load_uploaded_files():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Standardize column headers for robust matching
        df.columns = [str(col).strip().lower() for col in df.columns]
        return df
    except Exception as e:
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
        
        # Flexibly match columns regardless of exact Google Form field names
        cat_col = next((c for c in filtered_df.columns if "cat" in c or "type" in c), None)
        dept_col = next((c for c in filtered_df.columns if "dept" in c or "department" in c), None)
        title_col = next((c for c in filtered_df.columns if "title" in c or "file" in c or "name" in c), None)
        date_col = next((c for c in filtered_col.columns if "date" in c or "time" in c), None)
        id_col = next((c for c in filtered_df.columns if "id" in c or "link" in c or "url" in c), None)

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
                file_id = str(row[id_col]).strip() if id_col and pd.notna(row[id_col]) else ""

                # Extract ID if a full URL was saved in the sheet
                if "id=" in file_id:
                    file_id = file_id.split("id=")[-1].split("&")[0]
                elif "/d/" in file_id:
                    file_id = file_id.split("/d/")[1].split("/")[0]

                preview_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

                st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span style="background: #1E3A8A; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">{dept_val}</span>
                                <span style="background: #059669; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 6px;">{cat_val}</span>
                                <h4 style="margin: 0.6rem 0 0.3rem 0; color: #1E293B;">{title_val}</h4>
                                <small style="color: #64748B;">Uploaded on: {date_val}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                b_col1, b_col2, b_col3 = st.columns([1, 1, 3])
                with b_col1:
                    st.link_button("👁️ Preview", preview_url, use_container_width=True)
                with b_col2:
                    st.link_button("⬇️ Download", download_url, use_container_width=True)
                st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)
        else:
            st.warning("No files found matching the selected filters.")
    else:
        st.info("No materials cataloged yet or waiting for response data. Use the 'Upload New Materials' tab to submit documents.")

# --- TAB 2: UPLOAD PORTAL ---
with tab_upload:
    st.markdown("### 🚀 Secure Material Submission")
    st.markdown("""
        <div class="card">
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
