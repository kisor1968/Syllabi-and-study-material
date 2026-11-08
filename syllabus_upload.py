import streamlit as st
import pandas as pd
import re
import html
from pathlib import Path
from datetime import datetime, timedelta
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
logo_html = (
    f'<img class="portal-logo" src="data:image/jpeg;base64,{logo_b64}" alt="PJC Logo">'
    if logo_b64
    else '<div class="portal-logo-fallback">🏛️</div>'
)

# --- CUSTOM STYLING & INSTITUTIONAL THEME ---
# (plain string, not an f-string, so CSS braces need no escaping)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, button, input, select, textarea {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
}
.stApp {
    background:
        radial-gradient(1100px 500px at 90% -10%, rgba(37, 99, 235, 0.10), transparent 60%),
        radial-gradient(900px 450px at -10% 10%, rgba(245, 158, 11, 0.10), transparent 55%),
        #F1F5F9;
}
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1200px; }

/* ---------- HEADER ---------- */
.portal-header {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, #1E3A8A, #2563EB, #3B82F6, #1E3A8A);
    background-size: 300% 300%;
    animation: headerFlow 14s ease infinite, riseIn 0.7s ease both;
    padding: 1.8rem 2rem;
    border-radius: 16px;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.4rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 12px 28px -8px rgba(30, 58, 138, 0.45);
    border-bottom: 4px solid #F59E0B;
}
.portal-header::before, .portal-header::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
}
.portal-header::before {
    width: 260px; height: 260px;
    right: -60px; top: -110px;
    background: radial-gradient(circle, rgba(255, 153, 51, 0.35), transparent 70%);
    animation: floaty 9s ease-in-out infinite;
}
.portal-header::after {
    width: 180px; height: 180px;
    right: 180px; bottom: -110px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.18), transparent 70%);
    animation: floaty 11s ease-in-out infinite reverse;
}
.portal-logo {
    height: 78px; width: auto;
    border-radius: 10px;
    background: #FFFFFF;
    padding: 5px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    position: relative; z-index: 1;
}
.portal-logo-fallback { font-size: 2.4rem; position: relative; z-index: 1; }
.portal-header-text { position: relative; z-index: 1; }
.portal-header-text h1 {
    color: #FFFFFF !important;
    margin: 0; padding: 0;
    font-size: 2.15rem; font-weight: 800; line-height: 1.15;
    letter-spacing: -0.02em;
}
.portal-header-text p { color: #E2E8F0; margin: 0.35rem 0 0 0; font-size: 1.05rem; }
.header-live {
    margin-left: auto;
    position: relative; z-index: 1;
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.28);
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem; font-weight: 600;
    backdrop-filter: blur(4px);
}
.live-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: #34D399;
    box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7);
    animation: pulse 1.8s infinite;
}

/* ---------- STAT TILES ---------- */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 0.4rem 0 1.4rem 0;
}
.stat-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 5px solid var(--accent, #2563EB);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    display: flex; align-items: center; gap: 0.9rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    animation: riseIn 0.6s ease both;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-tile:hover { transform: translateY(-3px); box-shadow: 0 10px 22px rgba(30, 58, 138, 0.12); }
.stat-icon {
    width: 46px; height: 46px; flex: 0 0 46px;
    border-radius: 12px;
    display: grid; place-items: center;
    font-size: 1.4rem;
    background: color-mix(in srgb, var(--accent, #2563EB) 14%, white);
}
.stat-num { font-size: 1.7rem; font-weight: 800; color: #0F172A; line-height: 1.1; }
.stat-label { font-size: 0.82rem; color: #64748B; font-weight: 600; }

/* ---------- RESULT CARDS ---------- */
.card-item {
    background: #FFFFFF;
    padding: 1.3rem 1.6rem;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    border: 1px solid #E2E8F0;
    border-top: 4px solid #FF9933;
    position: relative;
    margin-bottom: 1.1rem;
    animation: riseIn 0.55s ease both;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
/* Half-cover saffron accent that sweeps to full width on hover */
.card-item::before {
    content: "";
    position: absolute;
    top: -4px; left: -1px;
    width: 50%; height: 4px;
    background-color: #FF7700;
    border-top-left-radius: 14px;
    transition: width 0.45s ease;
}
.card-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 28px rgba(30, 58, 138, 0.14);
    border-color: #BFDBFE;
}
.card-item:hover::before { width: calc(100% + 2px); border-top-right-radius: 14px; }

.card-row { display: flex; align-items: center; justify-content: space-between; gap: 1.2rem; flex-wrap: wrap; }
.card-main { flex: 1 1 320px; min-width: 0; }
.card-actions { display: flex; gap: 0.6rem; flex: 0 0 auto; min-width: 270px; }
.card-actions a { flex: 1; }

.badge {
    display: inline-block;
    color: #FFFFFF;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.78rem; font-weight: 700;
    margin-right: 6px;
}
.badge-new {
    background: linear-gradient(135deg, #F59E0B, #EF4444);
    animation: pulse-soft 2s ease-in-out infinite;
}
.card-title { margin: 0.65rem 0 0.3rem 0; color: #1E293B; font-size: 1.1rem; font-weight: 700; overflow-wrap: anywhere; }
.card-date { color: #64748B; font-size: 0.82rem; }

.btn-preview, .btn-download {
    color: #FFFFFF !important;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    text-decoration: none !important;
    display: inline-block;
    font-weight: 700;
    font-size: 0.9rem;
    text-align: center;
    white-space: nowrap;
    transition: transform 0.15s ease, box-shadow 0.2s ease, filter 0.2s ease;
}
.btn-preview  { background: linear-gradient(135deg, #2563EB, #1D4ED8); box-shadow: 0 3px 8px rgba(37, 99, 235, 0.28); }
.btn-download { background: linear-gradient(135deg, #10B981, #047857); box-shadow: 0 3px 8px rgba(5, 150, 105, 0.28); }
.btn-preview:hover, .btn-download:hover { transform: translateY(-2px); filter: brightness(1.08); }
.btn-preview:active, .btn-download:active { transform: translateY(0); }
.btn-disabled { background: #CBD5E1 !important; box-shadow: none !important; pointer-events: none; }

/* ---------- RESULT BAR ---------- */
.result-bar {
    display: flex; align-items: center; justify-content: space-between;
    margin: 0.2rem 0 1rem 0;
    color: #475569; font-size: 0.92rem; font-weight: 600;
}
.result-pill {
    background: #DBEAFE; color: #1E3A8A;
    padding: 3px 12px; border-radius: 999px; font-weight: 700;
}

/* ---------- DEPARTMENT BARS ---------- */
.dept-row { display: flex; align-items: center; gap: 0.8rem; margin: 0.45rem 0; font-size: 0.88rem; color: #334155; font-weight: 600; }
.dept-name { flex: 0 0 150px; }
.dept-track { flex: 1; height: 10px; background: #E2E8F0; border-radius: 999px; overflow: hidden; }
.dept-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #2563EB, #F59E0B);
    transform-origin: left;
    animation: grow 1s ease both;
}
.dept-count { flex: 0 0 32px; text-align: right; color: #1E3A8A; }

/* ---------- UPLOAD TAB ---------- */
.upload-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin: 1rem 0 1.4rem 0; }
.step-card {
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    animation: riseIn 0.6s ease both;
    transition: transform 0.2s ease;
}
.step-card:hover { transform: translateY(-3px); }
.step-no {
    width: 34px; height: 34px; border-radius: 50%;
    display: grid; place-items: center;
    background: linear-gradient(135deg, #F59E0B, #FF7700);
    color: #FFFFFF; font-weight: 800; margin-bottom: 0.6rem;
}
.step-card h4 { margin: 0 0 0.25rem 0; color: #1E293B; font-size: 1rem; }
.step-card p { margin: 0; color: #64748B; font-size: 0.88rem; }

/* ---------- TABS / WIDGETS ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 2px solid #E2E8F0; }
.stTabs [data-baseweb="tab"] {
    height: 48px; padding: 0 1.2rem;
    border-radius: 10px 10px 0 0;
    font-weight: 700; color: #475569;
    transition: background 0.2s ease, color 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover { background: #E0E7FF; color: #1E3A8A; }
.stTabs [aria-selected="true"] { color: #1E3A8A !important; background: #DBEAFE; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #F59E0B !important; height: 3px; }
div[data-testid="stLinkButton"] a, div.stButton > button {
    border-radius: 10px; font-weight: 700;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
}
div[data-testid="stLinkButton"] a {
    background: linear-gradient(135deg, #F59E0B, #FF7700);
    color: #FFFFFF !important; border: none; padding: 0.7rem 1rem;
    box-shadow: 0 6px 16px rgba(255, 119, 0, 0.35);
}
div[data-testid="stLinkButton"] a:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(255, 119, 0, 0.45); }
div.stButton > button:hover { transform: translateY(-1px); border-color: #2563EB; color: #1E3A8A; }

/* ---------- FOOTER ---------- */
.institutional-footer {
    background: linear-gradient(135deg, #1E3A8A, #1E40AF);
    color: #FFFFFF;
    text-align: center;
    padding: 1.6rem 1rem;
    border-radius: 14px;
    margin-top: 3rem;
    box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.05);
    border-top: 3px solid #F59E0B;
}
.institutional-footer p { margin: 0.3rem 0; color: #F8FAFC; font-size: 0.9rem; }
.visitor-counter { margin-top: 0.8rem; }

/* ---------- MOTION ---------- */
@keyframes headerFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes floaty { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(14px); } }
@keyframes riseIn { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(52, 211, 153, 0); } 100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); } }
@keyframes pulse-soft { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.07); } }
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }

@media (max-width: 720px) {
    .portal-header-text h1 { font-size: 1.6rem; }
    .header-live { margin-left: 0; }
    .card-actions { min-width: 100%; }
    .dept-name { flex-basis: 100px; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- HEADER WITH INTEGRATED LOGO ---
st.markdown(f"""
<div class="portal-header">
{logo_html}
<div class="portal-header-text">
<h1>Prabhu Jagatbandhu College</h1>
<p>Academic Repository &amp; Syllabus Management Portal</p>
</div>
<div class="header-live"><span class="live-dot"></span>Live repository</div>
</div>
""", unsafe_allow_html=True)

DEPARTMENT_FOLDERS = [
    "Bengali", "English", "Philosophy", "History", "Geography",
    "Economics", "Physical Education", "Physics", "Chemistry", "Mathematics", "Commerce"
]

# Distinct badge colour per department
DEPT_COLORS = [
    "#1E3A8A", "#7C3AED", "#BE185D", "#B45309", "#0F766E", "#C2410C",
    "#4D7C0F", "#0369A1", "#6D28D9", "#0E7490", "#9F1239",
]
def dept_color(name):
    for i, d in enumerate(DEPARTMENT_FOLDERS):
        if d.lower() in str(name).lower():
            return DEPT_COLORS[i % len(DEPT_COLORS)]
    return "#475569"

# --- LIVE PUBLISHED GOOGLE SHEET CSV URL ---
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTkBRxQ2SHSxD2u2S_0-ckK9j2a2D-gUXrIXAtGCTgYwuf2G5OlHAlQW8yoGZdMw5UiI0OeWPhIkP-u/pub?output=csv"

PAGE_SIZE = 10

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

def parse_dates(series):
    try:
        return pd.to_datetime(series, errors="coerce", format="mixed")
    except Exception:
        try:
            return pd.to_datetime(series, errors="coerce")
        except Exception:
            return pd.Series([pd.NaT] * len(series), index=series.index)

# --- NAVIGATION TABS ---
tab_browse, tab_upload = st.tabs(["📂 Browse Repository & Syllabi", "📤 Upload New Materials"])

# --- TAB 1: BROWSE REPOSITORY ---
with tab_browse:
    head_l, head_r = st.columns([5, 1])
    with head_l:
        st.markdown("### 🔍 Explore Live Departmental Resources")
    with head_r:
        if st.button("🔄 Refresh", use_container_width=True, help="Reload the latest uploads"):
            load_uploaded_files.clear()
            st.rerun()

    df_files = load_uploaded_files()

    # Column detection (same rules as before)
    cat_col = dept_col = title_col = date_col = id_col = None
    if not df_files.empty:
        cat_col = next((c for c in df_files.columns if "cat" in c or "type" in c), None)
        dept_col = next((c for c in df_files.columns if "dept" in c or "department" in c), None)
        title_col = next((c for c in df_files.columns if "title" in c or "file" in c or "name" in c or "upload" in c), None)
        date_col = next((c for c in df_files.columns if "date" in c or "time" in c or "timestamp" in c), None)
        id_col = next((c for c in df_files.columns if "id" in c or "link" in c or "url" in c or "file" in c or "upload" in c), None)

        # --- LIVE STATS ---
        total_docs = len(df_files)
        syllabus_docs = (
            int(df_files[cat_col].astype(str).str.contains("syllabus", case=False, na=False).sum())
            if cat_col else 0
        )
        study_docs = (
            int(df_files[cat_col].astype(str).str.contains("study", case=False, na=False).sum())
            if cat_col else 0
        )
        dept_counts = {}
        if dept_col:
            for d in DEPARTMENT_FOLDERS:
                n = int(df_files[dept_col].astype(str).str.contains(d, case=False, na=False).sum())
                if n:
                    dept_counts[d] = n
        dept_total = len(dept_counts)

        st.markdown(f"""
<div class="stat-grid">
<div class="stat-tile" style="--accent:#2563EB; animation-delay:0s;"><div class="stat-icon">📚</div><div><div class="stat-num">{total_docs}</div><div class="stat-label">Total documents</div></div></div>
<div class="stat-tile" style="--accent:#F59E0B; animation-delay:0.08s;"><div class="stat-icon">📘</div><div><div class="stat-num">{syllabus_docs}</div><div class="stat-label">Syllabi</div></div></div>
<div class="stat-tile" style="--accent:#10B981; animation-delay:0.16s;"><div class="stat-icon">📝</div><div><div class="stat-num">{study_docs}</div><div class="stat-label">Study materials</div></div></div>
<div class="stat-tile" style="--accent:#7C3AED; animation-delay:0.24s;"><div class="stat-icon">🏫</div><div><div class="stat-num">{dept_total}</div><div class="stat-label">Departments contributing</div></div></div>
</div>
""", unsafe_allow_html=True)

        if dept_counts:
            with st.expander("📊 Documents by department"):
                max_n = max(dept_counts.values())
                rows = "".join(
                    f'<div class="dept-row"><span class="dept-name">{html.escape(d)}</span>'
                    f'<span class="dept-track"><span class="dept-fill" style="display:block;width:{n / max_n * 100:.0f}%;"></span></span>'
                    f'<span class="dept-count">{n}</span></div>'
                    for d, n in sorted(dept_counts.items(), key=lambda x: -x[1])
                )
                st.markdown(rows, unsafe_allow_html=True)

    # --- FILTERS ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.1, 1.4, 1.6, 1.1])
    with f_col1:
        selected_category = st.selectbox("Select Category", ["All", "Syllabus", "Study Material"])
    with f_col2:
        selected_dept = st.selectbox("Select Department", ["All Departments"] + DEPARTMENT_FOLDERS)
    with f_col3:
        search_query = st.text_input("Search", placeholder="🔎 Search by title, e.g. 'CBCS Semester 3'")
    with f_col4:
        sort_choice = st.selectbox("Sort by", ["Newest first", "Oldest first", "Title A–Z"])

    st.markdown("---")

    if not df_files.empty:
        filtered_df = df_files.copy()

        if selected_category != "All" and cat_col:
            filtered_df = filtered_df[filtered_df[cat_col].astype(str).str.contains(selected_category, case=False, na=False)]

        if selected_dept != "All Departments" and dept_col:
            filtered_df = filtered_df[filtered_df[dept_col].astype(str).str.contains(selected_dept, case=False, na=False)]

        if search_query.strip():
            q = search_query.strip()
            hay = pd.Series("", index=filtered_df.index)
            for c in (title_col, dept_col, cat_col):
                if c:
                    hay = hay + " " + filtered_df[c].astype(str)
            filtered_df = filtered_df[hay.str.contains(q, case=False, na=False, regex=False)]

        # Sorting
        parsed_dates = parse_dates(filtered_df[date_col]) if date_col else None
        if sort_choice == "Title A–Z" and title_col:
            filtered_df = filtered_df.sort_values(title_col, key=lambda s: s.astype(str).str.lower())
        elif parsed_dates is not None and parsed_dates.notna().any():
            filtered_df = filtered_df.assign(_sort_dt=parsed_dates).sort_values(
                "_sort_dt", ascending=(sort_choice == "Oldest first"), na_position="last"
            )
        elif sort_choice == "Newest first":
            filtered_df = filtered_df.iloc[::-1]

        # Reset pagination when filters change
        signature = (selected_category, selected_dept, search_query, sort_choice)
        if st.session_state.get("filter_signature") != signature:
            st.session_state["filter_signature"] = signature
            st.session_state["visible_count"] = PAGE_SIZE
        visible_count = st.session_state.get("visible_count", PAGE_SIZE)

        if not filtered_df.empty:
            total_found = len(filtered_df)
            st.markdown(
                f'<div class="result-bar"><span>Showing <span class="result-pill">{min(visible_count, total_found)} of {total_found}</span> documents</span></div>',
                unsafe_allow_html=True
            )

            now = datetime.now()
            for pos, (idx, row) in enumerate(filtered_df.head(visible_count).iterrows()):
                dept_val = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else "General"
                cat_val = str(row[cat_col]) if cat_col and pd.notna(row[cat_col]) else "Material"
                title_val = str(row[title_col]) if title_col and pd.notna(row[title_col]) else f"Document #{idx+1}"
                date_val = str(row[date_col]) if date_col and pd.notna(row[date_col]) else "Recent"

                raw_id_val = row[id_col] if id_col and pd.notna(row[id_col]) else ""
                clean_file_id = extract_drive_id(raw_id_val)

                if clean_file_id:
                    preview_url = f"https://drive.google.com/file/d/{clean_file_id}/view?usp=sharing"
                    download_url = f"https://drive.google.com/uc?export=download&id={clean_file_id}"
                    preview_btn = f'<a href="{preview_url}" target="_blank" class="btn-preview">👁️ Preview</a>'
                    download_btn = f'<a href="{download_url}" target="_blank" class="btn-download">⬇️ Download</a>'
                else:
                    preview_btn = '<a class="btn-preview btn-disabled">👁️ Preview</a>'
                    download_btn = '<a class="btn-download btn-disabled">⬇️ Download</a>'

                # "New" badge for uploads in the last 7 days
                new_badge = ""
                if date_col:
                    try:
                        dt = pd.to_datetime(row[date_col], errors="coerce")
                        if pd.notna(dt) and now - dt.to_pydatetime() <= timedelta(days=7):
                            new_badge = '<span class="badge badge-new">✨ New</span>'
                    except Exception:
                        pass

                delay = min(pos * 0.06, 0.5)
                st.markdown(f"""
<div class="card-item" style="animation-delay:{delay:.2f}s;">
<div class="card-row">
<div class="card-main">
<span class="badge" style="background:{dept_color(dept_val)};">{html.escape(dept_val)}</span>
<span class="badge" style="background:#059669;">{html.escape(cat_val)}</span>
{new_badge}
<h4 class="card-title">{html.escape(title_val)}</h4>
<small class="card-date">🕒 Uploaded on: {html.escape(date_val)}</small>
</div>
<div class="card-actions">{preview_btn}{download_btn}</div>
</div>
</div>
""", unsafe_allow_html=True)

            if total_found > visible_count:
                _, mid, _ = st.columns([1, 1, 1])
                with mid:
                    if st.button(f"⬇️ Load more ({total_found - visible_count} remaining)", use_container_width=True):
                        st.session_state["visible_count"] = visible_count + PAGE_SIZE
                        st.rerun()
        else:
            st.warning("No files found matching the selected filters.")
    else:
        st.info("No materials cataloged yet or waiting for response data. Use the 'Upload New Materials' tab to submit documents.")

# --- TAB 2: UPLOAD PORTAL ---
with tab_upload:
    st.markdown("### 🚀 Secure Material Submission")
    st.markdown("""
<div class="card-item">
<p style="color: #334155; margin-bottom: 0;">
Click below to open the secure Google Form. Submissions automatically log to the master directory and update this repository portal in real-time.
</p>
</div>
<div class="upload-steps">
<div class="step-card" style="animation-delay:0.05s;"><div class="step-no">1</div><h4>Open the form</h4><p>Use the secure upload button below.</p></div>
<div class="step-card" style="animation-delay:0.15s;"><div class="step-no">2</div><h4>Fill in the details</h4><p>Choose the category and department, then attach your file.</p></div>
<div class="step-card" style="animation-delay:0.25s;"><div class="step-no">3</div><h4>See it live</h4><p>Your document appears in the repository shortly after submission.</p></div>
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
<p>Created &amp; Maintained by: <strong>Dr. Kisor Mukhopadhyay</strong>, Associate Professor, Department of Physics, Prabhu Jagatbandhu College</p>
<div class="visitor-counter">
<img src="https://visitor-badge.laobi.icu/badge?page_id=pjc_academic_repository_portal" alt="Visitor Counter">
</div>
</div>
""", unsafe_allow_html=True)
