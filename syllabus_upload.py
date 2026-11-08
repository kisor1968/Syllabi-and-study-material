import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re
import html
import hmac
from pathlib import Path
from datetime import datetime, timedelta
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PJC Academic Material Repository Portal",
    page_icon="📚",
    layout="wide"
)

# =====================================================================
# CONFIGURATION
# =====================================================================
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTkBRxQ2SHSxD2u2S_0-ckK9j2a2D-gUXrIXAtGCTgYwuf2G5OlHAlQW8yoGZdMw5UiI0OeWPhIkP-u/pub?output=csv"
ANNOUNCEMENTS_CSV_URL = ""
FORM_DIRECT_URL = "https://forms.gle/Uk4AcdHTUL67wQ3f7"
PAGE_SIZE = 10

DEPARTMENT_FOLDERS = [
    "Bengali", "English", "Philosophy", "History", "Geography",
    "Economics", "Physical Education", "Physics", "Chemistry", "Mathematics", "Commerce",
    "Zoology", "Botany", "Computer Science", "Electronics", "Political Science", "Sociology", "Sanskrit", "Education", "Food & Nutrition"
]
DEPT_BN = {
    "Bengali": "বাংলা", "English": "ইংরেজি", "Philosophy": "দর্শন", "History": "ইতিহাস",
    "Geography": "ভূগোল", "Economics": "অর্থনীতি", "Physical Education": "শারীরিক শিক্ষা",
    "Physics": "পদার্থবিদ্যা", "Chemistry": "রসায়ন", "Mathematics": "গণিত", "Commerce": "বাণিজ্য",
    "Zoology": "প্রাণিবিদ্যা", "Botany": "উদ্ভিদবিদ্যা", "Computer Science": "কম্পিউটার বিজ্ঞান",
    "Electronics": "ইলেকট্রনিক্স", "Political Science": "রাষ্ট্রবিজ্ঞান", "Sociology": "সমাজবিজ্ঞান", 
    "Sanskrit": "সংস্কৃত", "Education": "শিক্ষাবিজ্ঞান", "Food & Nutrition": "খাদ্য ও পুষ্টি",
}
DEPT_COLORS = [
    "#1E3A8A", "#7C3AED", "#BE185D", "#B45309", "#0F766E", "#C2410C",
    "#4D7C0F", "#0369A1", "#6D28D9", "#0E7490", "#9F1239", "#15803D",
    "#A16207", "#1D4ED8", "#BE123C", "#0891B2", "#7E22CE", "#475569", "#0D9488", "#D97706"
]

# =====================================================================
# TRANSLATIONS (English / বাংলা)
# =====================================================================
TEXT = {
    "en": {
        "site_name": "Prabhu Jagatbandhu College",
        "site_tagline": "Academic Repository &amp; Syllabus Management Portal",
        "live": "Live repository",
        "visitors": "Total Visitors",
        "language": "Language",
        "dark_label": "🌙 Dark mode",
        "refresh": "🔄 Refresh",
        "refresh_help": "Reload the latest uploads",
        "explore": "🔍 Explore Live Departmental Resources",
        "total_docs": "Total documents",
        "syllabi": "Syllabi",
        "study_materials": "Study materials",
        "assignments": "Assignments",
        "depts_contrib": "Departments contributing",
        "by_dept": "📊 Documents by department",
        "category": "Select Category",
        "department": "Select Department",
        "semester": "Select Semester",
        "file_type": "File Format",
        "search": "Search",
        "search_ph": "🔎 Search by title, e.g. 'CBCS Semester 3'",
        "sort_by": "Sort by",
        "all": "All",
        "all_depts": "All Departments",
        "all_sems": "All Semesters",
        "all_types": "All Formats",
        "syllabus": "Syllabus",
        "study_material": "Study Material",
        "assignment": "Assignment",
        "newest": "Newest first",
        "oldest": "Oldest first",
        "az": "Title A–Z",
        "most_downloaded": "Most Downloaded",
        "top_rated": "Top Rated",
        "showing": "Showing {shown} of {total} documents",
        "load_more": "⬇️ Load more ({n} remaining)",
        "no_match": "No files found matching the selected filters.",
        "empty_repo": "No materials cataloged yet or waiting for response data. Use the 'Upload New Materials' tab to submit documents.",
        "new": "✨ New",
        "uploaded_on": "Uploaded on",
        "recent": "Recent",
        "preview": "👁️ Preview",
        "save": "☆ Save",
        "saved": "★ Saved",
        "download": "⬇️ Download",
        "downloads_count": "Downloads",
        "rating_label": "Rate Resource",
        "avg_rating": "Rating",
        "viewer_mode": "Viewer Mode",
        "viewer_modal": "Popup Modal",
        "viewer_inline": "Full Width Inline",
        "popular_head": "🔥 Popular Resources Leaderboard",
        "tab_browse": "📂 Browse Repository",
        "tab_popular": "🔥 Popular & Leaderboard",
        "tab_saved": "⭐ My Saved ({n})",
        "tab_upload": "📤 Upload New Materials",
        "tab_admin": "🔐 Admin & Analytics",
        "saved_head": "⭐ My Saved Documents",
        "saved_note": "Your saved list is kept in this page's address (URL). Bookmark the page to keep it.",
        "saved_empty": "Nothing saved yet. Press ☆ Save under any document to add it here.",
        "saved_clear": "🗑️ Clear all",
        "upload_head": "🚀 Secure Material Submission",
        "upload_intro": "Click below to open the secure Google Form. Submissions automatically log to the master directory and update this repository portal in real-time.",
        "step1_t": "Open the form", "step1_d": "Use the secure upload button below.",
        "step2_t": "Fill in the details", "step2_d": "Choose the category, semester, and department, then attach your file.",
        "step3_t": "See it live", "step3_d": "Your document appears in the repository shortly after submission.",
        "open_form": "🚀 Open Secure Upload Portal",
        "preview_note": "If the preview does not load, use direct download. The file must be shared as “Anyone with the link can view”.",
        "notices": "📢 Notices",
        "all_notices": "📢 All notices ({n})",
        "footer_rights": "© Prabhu Jagatbandhu College | Academic Repository Management",
        "footer_by": "Created &amp; Maintained by: <strong>Dr. Kisor Mukhopadhyay</strong>, Associate Professor, Department of Physics, Prabhu Jagatbandhu College",
        "faculty_login_head": "🔐 Faculty Login Required",
        "faculty_login_sub": "Please enter the password to access the secure material upload portal.",
        "faculty_pw": "Faculty Password",
        "faculty_login_btn": "Log In",
        "faculty_wrong": "Incorrect password.",
        "faculty_logged_in": "✅ Logged in as Faculty",
        "faculty_logout": "Log Out",
        "admin_head": "🔐 Admin Dashboard & Advanced Analytics",
        "admin_setup": "The admin password is not set yet. Add this to your Streamlit secrets (.streamlit/secrets.toml, or Streamlit Cloud → Settings → Secrets):",
        "admin_pw": "Admin password",
        "admin_login": "Log in",
        "admin_wrong": "Incorrect password.",
        "admin_lockout": "Too many failed attempts. Reload the page to try again.",
        "admin_logout": "Log out",
        "adm_total": "Total documents",
        "adm_month": "This month",
        "adm_week": "Last 7 days",
        "adm_nolink": "Missing file link",
        "adm_by_month": "Uploads per month (last 12)",
        "adm_by_dept": "Uploads per department",
        "adm_by_cat": "Uploads per category",
        "adm_empty_depts": "Departments with no uploads yet",
        "adm_all_covered": "Every department has at least one document.",
        "adm_attention": "Needs attention",
        "adm_none_attention": "No problems found.",
        "adm_issue_nolink": "No file link",
        "adm_issue_nodept": "No department",
        "adm_issue_nocat": "No category",
        "adm_issue_dup": "Possible duplicates",
        "adm_recent": "Recent uploads & Management",
        "adm_export": "⬇️ Download catalog as CSV",
        "col_date": "Date", "col_dept": "Department", "col_cat": "Category", "col_title": "Title", "col_link": "File link", "col_actions": "Actions",
        "link_ok": "✔ Yes", "link_missing": "✘ Missing",
        "adm_delete": "🗑️ Remove",
    },
    "bn": {
        "site_name": "প্রভু জগদ্বন্ধু কলেজ",
        "site_tagline": "একাডেমিক রিপোজিটরি ও সিলেবাস ব্যবস্থাপনা পোর্টাল",
        "live": "লাইভ রিপোজিটরি",
        "visitors": "মোট ভিজিটর",
        "language": "ভাষা",
        "dark_label": "🌙 ডার্ক মোড",
        "refresh": "🔄 রিফ্রেশ",
        "refresh_help": "সর্বশেষ আপলোড লোড করুন",
        "explore": "🔍 বিভাগীয় সম্পদ খুঁজুন",
        "total_docs": "মোট নথি",
        "syllabi": "সিলেবাস",
        "study_materials": "পাঠ্যসামগ্রী",
        "assignments": "অ্যাসাইনমেন্ট",
        "depts_contrib": "অবদানকারী বিভাগ",
        "by_dept": "📊 বিভাগ অনুযায়ী নথি",
        "category": "ধরন নির্বাচন করুন",
        "department": "বিভাগ নির্বাচন করুন",
        "semester": "সেমিস্টার নির্বাচন করুন",
        "file_type": "ফাইলের ধরন",
        "search": "অনুসন্ধান",
        "search_ph": "🔎 শিরোনাম দিয়ে খুঁজুন, যেমন 'CBCS সেমিস্টার ৩'",
        "sort_by": "সাজান",
        "all": "সব",
        "all_depts": "সব বিভাগ",
        "all_sems": "সব সেমিস্টার",
        "all_types": "সব ফরম্যাট",
        "syllabus": "সিলেবাস",
        "study_material": "পাঠ্যসামগ্রী",
        "assignment": "অ্যাসাইনমেন্ট",
        "newest": "নতুন আগে",
        "oldest": "পুরনো আগে",
        "az": "শিরোনাম অনুযায়ী",
        "most_downloaded": "সর্বাধিক ডাউনলোড",
        "top_rated": "সেরা রেটিং প্রাপ্ত",
        "showing": "{total} টি নথির মধ্যে {shown} টি দেখানো হচ্ছে",
        "load_more": "⬇️ আরও দেখুন (আরও {n} টি)",
        "no_match": "নির্বাচিত ফিল্টারে কোনো ফাইল পাওয়া যায়নি।",
        "empty_repo": "এখনও কোনো সামগ্রী তালিকাভুক্ত হয়নি, অথবা ডেটার জন্য অপেক্ষা চলছে। নথি জমা দিতে 'নতুন সামগ্রী আপলোড' ট্যাব ব্যবহার করুন।",
        "new": "✨ নতুন",
        "uploaded_on": "আপলোডের তারিখ",
        "recent": "সম্প্রতি",
        "preview": "👁️ প্রিভিউ",
        "save": "☆ সংরক্ষণ",
        "saved": "★ সংরক্ষিত",
        "download": "⬇️ ডাউনলোড",
        "downloads_count": "ডাউনলোড",
        "rating_label": "রেটিং দিন",
        "avg_rating": "রেটিং",
        "viewer_mode": "প্রিভিউ মোড",
        "viewer_modal": "পপআপ মোডাল",
        "viewer_inline": "সম্পূর্ণ ইনলাইন",
        "popular_head": "🔥 জনপ্রিয় ও শীর্ষস্থানীয় সম্পদ",
        "tab_browse": "📂 রিপোজিটরি দেখুন",
        "tab_popular": "🔥 জনপ্রিয় ও লিডারবোর্ড",
        "tab_saved": "⭐ আমার সংরক্ষিত ({n})",
        "tab_upload": "📤 নতুন সামগ্রী আপলোড",
        "tab_admin": "🔐 অ্যাডমিন ও অ্যানালিটিক্স",
        "saved_head": "⭐ আমার সংরক্ষিত নথি",
        "saved_note": "সংরক্ষিত তালিকা এই পেজের ঠিকানায় (URL) জমা থাকে। তালিকা রাখতে পেজটি বুকমার্ক করুন।",
        "saved_empty": "এখনও কিছু সংরক্ষণ করা হয়নি। কোনো নথির নিচে ☆ সংরক্ষণ চাপুন।",
        "saved_clear": "🗑️ সব মুছুন",
        "upload_head": "🚀 নিরাপদ সামগ্রী জমা",
        "upload_intro": "নিচের বোতামে ক্লিক করে নিরাপদ Google Form খুলুন। জমা দেওয়া নথি স্বয়ংক্রিয়ভাবে মূল তালিকায় যুক্ত হয় এবং এই পোর্টালে রিয়েল-টাইমে দেখা যায়।",
        "step1_t": "ফর্মটি খুলুন", "step1_d": "নিচের নিরাপদ আপলোড বোতামটি ব্যবহার করুন।",
        "step2_t": "বিবরণ পূরণ করুন", "step2_d": "ধরন, সেমিস্টার ও বিভাগ বেছে নিন, তারপর ফাইল সংযুক্ত করুন।",
        "step3_t": "লাইভ দেখুন", "step3_d": "জমা দেওয়ার কিছুক্ষণের মধ্যেই আপনার নথি রিপোজিটরিতে দেখা যাবে।",
        "open_form": "🚀 নিরাপদ আপলোড পোর্টাল খুলুন",
        "preview_note": "প্রিভিউ লোড না হলে সরাসরি ডাউনলোড করুন। ফাইলটি “লিঙ্কযুক্ত যে কেউ দেখতে পারবে” হিসেবে শেয়ার করা থাকতে হবে।",
        "notices": "📢 নোটিশ",
        "all_notices": "📢 সব নোটিশ ({n})",
        "footer_rights": "© প্রভু জগদ্বন্ধু কলেজ | একাডেমিক রিপোজিটরি ব্যবস্থাপনা",
        "footer_by": "সৃষ্টি ও রক্ষণাবেক্ষণ: <strong>Dr. Kisor Mukhopadhyay</strong>, অ্যাসোসিয়েট প্রফেসর, পদার্থবিদ্যা বিভাগ, প্রভু জগদ্বন্ধু কলেজ",
        "faculty_login_head": "🔐 অনুষদ লগইন প্রয়োজন",
        "faculty_login_sub": "নিরাপদ সামগ্রী আপলোড পোর্টাল অ্যাক্সেস করতে পাসওয়ার্ড দিন।",
        "faculty_pw": "পাসওয়ার্ড",
        "faculty_login_btn": "লগ ইন",
        "faculty_wrong": "পাসওয়ার্ড সঠিক নয়।",
        "faculty_logged_in": "✅ অনুষদ হিসেবে লগইন করা হয়েছে",
        "faculty_logout": "লগ আউট",
        "admin_head": "🔐 অ্যাডমিন ড্যাশবোর্ড ও বিশদ অ্যানালিটিক্স",
        "admin_setup": "অ্যাডমিন পাসওয়ার্ড এখনও সেট করা হয়নি। Streamlit secrets-এ এটি যোগ করুন (.streamlit/secrets.toml, অথবা Streamlit Cloud → Settings → Secrets):",
        "admin_pw": "অ্যাডমিন পাসওয়ার্ড",
        "admin_login": "লগ ইন",
        "admin_wrong": "পাসওয়ার্ড সঠিক নয়।",
        "admin_lockout": "বহুবার ভুল চেষ্টা হয়েছে। পেজ রিলোড করে আবার চেষ্টা করুন।",
        "admin_logout": "লগ আউট",
        "adm_total": "মোট নথি",
        "adm_month": "এই মাসে",
        "adm_week": "গত ৭ দিনে",
        "adm_nolink": "ফাইল লিঙ্ক নেই",
        "adm_by_month": "মাস অনুযায়ী আপলোড (শেষ ১২ মাস)",
        "adm_by_dept": "বিভাগ অনুযায়ী আপলোড",
        "adm_by_cat": "ধরন অনুযায়ী আপলোড",
        "adm_empty_depts": "যেসব বিভাগ এখনও কিছু আপলোড করেনি",
        "adm_all_covered": "সব বিভাগ অন্তত একটি নথি আপলোড করেছে।",
        "adm_attention": "মনোযোগ প্রয়োজন",
        "adm_none_attention": "কোনো সমস্যা পাওয়া যায়নি।",
        "adm_issue_nolink": "ফাইল লিঙ্ক নেই",
        "adm_issue_nodept": "বিভাগ নেই",
        "adm_issue_nocat": "ধরন নেই",
        "adm_issue_dup": "সম্ভাব্য ডুপ্লিকেট",
        "adm_recent": "সাম্প্রতিক আপলোড ও ব্যবস্থাপনা",
        "adm_export": "⬇️ তালিকা CSV হিসেবে ডাউনলোড",
        "col_date": "তারিখ", "col_dept": "বিভাগ", "col_cat": "ধরন", "col_title": "শিরোনাম", "col_link": "ফাইল লিঙ্ক", "col_actions": "কার্যকলাপ",
        "link_ok": "✔ আছে", "link_missing": "✘ নেই",
        "adm_delete": "🗑️ মুছুন",
    },
}

def t(key, **kw):
    lang = st.session_state.get("lang", "en")
    s = TEXT.get(lang, TEXT["en"]).get(key) or TEXT["en"].get(key, key)
    return s.format(**kw) if kw else s

# =====================================================================
# SESSION STATE INITIALIZATION & VISITOR COUNTER
# =====================================================================
def _valid_fid(fid):
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{10,}", str(fid or "")))

if "init_done" not in st.session_state:
    qp = st.query_params
    st.session_state["lang"] = "bn" if qp.get("lang") == "bn" else "en"
    st.session_state["dark_mode"] = qp.get("theme") == "dark"
    st.session_state["saved"] = [s for s in str(qp.get("saved", "")).split(",") if _valid_fid(s)][:60]
    st.session_state["deleted_rows"] = []
    st.session_state["downloads"] = {}
    st.session_state["ratings"] = {}
    # Persistent session-based visitor counter increment
    st.session_state["visitor_count"] = 12480  # Base count + increments per session
    st.session_state["init_done"] = True
else:
    if "counted_visit" not in st.session_state:
        st.session_state["visitor_count"] = st.session_state.get("visitor_count", 12480) + 1
        st.session_state["counted_visit"] = True

def toggle_save(fid):
    saved = list(st.session_state.get("saved", []))
    if fid in saved:
        saved.remove(fid)
    else:
        saved.append(fid)
    st.session_state["saved"] = saved[-60:]

def clear_saved():
    st.session_state["saved"] = []

def record_download(fid):
    counts = st.session_state.get("downloads", {})
    counts[fid] = counts.get(fid, 0) + 1
    st.session_state["downloads"] = counts

def add_rating(fid, score):
    ratings = st.session_state.get("ratings", {})
    if fid not in ratings:
        ratings[fid] = []
    ratings[fid].append(score)
    st.session_state["ratings"] = ratings

def get_avg_rating(fid):
    ratings = st.session_state.get("ratings", {}).get(fid, [])
    if not ratings:
        return 0.0, 0
    return round(sum(ratings) / len(ratings), 1), len(ratings)

def get_download_count(fid):
    return st.session_state.get("downloads", {}).get(fid, 0)

def detect_file_type(title_or_link):
    s = str(title_or_link).lower()
    if any(k in s for k in ("pdf", ".pdf")):
        return "PDF", "📄", "#EF4444"
    elif any(k in s for k in ("doc", "docx", "word")):
        return "Word", "📝", "#2563EB"
    elif any(k in s for k in ("xls", "xlsx", "sheet", "csv")):
        return "Excel", "📊", "#059669"
    elif any(k in s for k in ("ppt", "pptx", "slide")):
        return "Presentation", "📊", "#D97706"
    elif any(k in s for k in ("jpg", "png", "jpeg", "image")):
        return "Image", "🖼️", "#7C3AED"
    return "Document", "📁", "#475569"

def sync_query_params():
    desired = {}
    if st.session_state.get("lang") == "bn":
        desired["lang"] = "bn"
    if st.session_state.get("dark_mode"):
        desired["theme"] = "dark"
    if st.session_state.get("saved"):
        desired["saved"] = ",".join(st.session_state["saved"])
    for key in ("lang", "theme", "saved"):
        if key in desired:
            if st.query_params.get(key) != desired[key]:
                st.query_params[key] = desired[key]
        elif key in st.query_params:
            del st.query_params[key]

dark = bool(st.session_state.get("dark_mode"))

# =====================================================================
# STYLING
# =====================================================================
LIGHT_VARS = """
:root {
  color-scheme: light;
  --bg:#F1F5F9; --surface:#FFFFFF; --border:#E2E8F0; --text:#1E293B; --muted:#64748B;
  --stat-num:#0F172A; --shadow:rgba(15,23,42,0.06); --shadow-hover:rgba(30,58,138,0.14);
  --pill-bg:#DBEAFE; --pill-text:#1E3A8A; --track:#E2E8F0; --hover-bg:#E0E7FF;
  --notice-bg:#FFF7E6; --link:#1D4ED8; --accent-text:#1E3A8A; --card-hover-border:#BFDBFE;
  --glow1:rgba(37,99,235,0.10); --glow2:rgba(245,158,11,0.10);
}
"""
DARK_VARS = """
:root {
  color-scheme: dark;
  --bg:#0B1220; --surface:#131C2E; --border:#26334A; --text:#E6EDF7; --muted:#94A3B8;
  --stat-num:#F8FAFC; --shadow:rgba(0,0,0,0.35); --shadow-hover:rgba(59,130,246,0.22);
  --pill-bg:#1E3A8A; --pill-text:#DBEAFE; --track:#26334A; --hover-bg:#1E293B;
  --notice-bg:#2A1F0A; --link:#93C5FD; --accent-text:#93C5FD; --card-hover-border:#3B5B9A;
  --glow1:rgba(37,99,235,0.18); --glow2:rgba(245,158,11,0.08);
}
"""
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Bengali:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp, .stMarkdown, button, input, select, textarea { font-family: 'Plus Jakarta Sans', 'Noto Sans Bengali', sans-serif; }
.stApp { background: radial-gradient(1100px 500px at 90% -10%, var(--glow1), transparent 60%), radial-gradient(900px 450px at -10% 10%, var(--glow2), transparent 55%), var(--bg); color: var(--text); }
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1200px; }
.portal-header { position: relative; overflow: hidden; background: linear-gradient(120deg, #1E3A8A, #2563EB, #3B82F6, #1E3A8A); padding: 1.8rem 2rem; border-radius: 16px; color: #FFFFFF; display: flex; align-items: center; flex-wrap: wrap; gap: 1.4rem; margin-bottom: 1.4rem; box-shadow: 0 12px 28px -8px rgba(30,58,138,0.45); border-bottom: 4px solid #F59E0B; }
.portal-logo { height: 78px; width: auto; border-radius: 10px; background: #FFFFFF; padding: 5px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); }
.stApp .portal-header-text h1 { color: #FFFFFF !important; margin: 0; font-size: 2.15rem; font-weight: 800; }
.stApp .portal-header-text p { color: #E2E8F0 !important; margin: 0.35rem 0 0 0; }
.header-live { margin-left: auto; display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(255,255,255,0.14); padding: 0.4rem 0.9rem; border-radius: 999px; font-size: 0.85rem; font-weight: 600; color: #FFFFFF; }
.live-dot { width: 9px; height: 9px; border-radius: 50%; background: #34D399; animation: pulse 1.8s infinite; }
.visitor-badge { background: rgba(255,255,255,0.18); padding: 0.4rem 0.9rem; border-radius: 999px; font-size: 0.85rem; font-weight: 600; color: #FFFFFF; display: inline-flex; align-items: center; gap: 0.4rem; }
.card-item { background: var(--surface); padding: 1.3rem 1.6rem; border-radius: 14px; box-shadow: 0 4px 12px var(--shadow); border: 1px solid var(--border); border-top: 4px solid #FF9933; position: relative; margin-bottom: 0.8rem; }
.badge { display: inline-block; color: #FFFFFF; padding: 3px 11px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; margin-right: 6px; }
.stApp .card-title { margin: 0.4rem 0 0.2rem 0; color: var(--text); font-size: 1.1rem; font-weight: 700; }
.card-date { color: var(--muted); font-size: 0.82rem; }
.institutional-footer { background: linear-gradient(135deg, #1E3A8A, #1E40AF); color: #FFFFFF; text-align: center; padding: 1.6rem 1rem; border-radius: 14px; margin-top: 3rem; border-top: 3px solid #F59E0B; }

@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.7); } 70% { box-shadow: 0 0 0 10px rgba(52,211,153,0); } 100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); } }
"""
st.markdown("<style>" + (DARK_VARS if dark else LIGHT_VARS) + BASE_CSS + "</style>", unsafe_allow_html=True)

# =====================================================================
# HELPERS & DATA LOADERS
# =====================================================================
def get_base64_image(image_path):
    p = Path(image_path)
    if p.exists():
        with open(p, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def extract_drive_id(value):
    if not value or pd.isna(value):
        return ""
    val_str = str(value).strip()
    match_d = re.search(r'/d/([a-zA-Z0-9_-]+)', val_str)
    if match_d: return match_d.group(1)
    match_id = re.search(r'id=([a-zA-Z0-9_-]+)', val_str)
    if match_id: return match_id.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{25,}$', val_str): return val_str
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
    try: return pd.to_datetime(series, errors="coerce", format="mixed")
    except Exception:
        try: return pd.to_datetime(series, errors="coerce")
        except Exception: return pd.Series([pd.NaT] * len(series), index=series.index)

def match_dept(name):
    low = str(name).lower()
    for d in sorted(DEPARTMENT_FOLDERS, key=len, reverse=True):
        if d.lower() in low: return d
    return None

def dept_mask(series, dept):
    s = series.astype(str)
    mask = s.str.contains(dept, case=False, na=False, regex=False)
    for other in DEPARTMENT_FOLDERS:
        if other != dept and dept.lower() in other.lower():
            mask &= ~s.str.contains(other, case=False, na=False, regex=False)
    return mask

def dept_color(name):
    d = match_dept(name)
    if d: return DEPT_COLORS[DEPARTMENT_FOLDERS.index(d) % len(DEPT_COLORS)]
    return "#475569"

def dept_label(name):
    if st.session_state.get("lang") == "bn":
        d = match_dept(name)
        if d: return DEPT_BN.get(d, d)
    return name

def cat_label(value):
    if st.session_state.get("lang") == "bn":
        low = str(value).lower()
        if "syllabus" in low: return t("syllabus")
        if "study" in low: return t("study_material")
        if "assignment" in low: return t("assignment")
    return value

def esc(v): return html.escape(str(v), quote=True)

def detect_columns(df):
    if df.empty: return {}
    cols = df.columns
    return {
        "cat": next((c for c in cols if "cat" in c or "type" in c), None),
        "dept": next((c for c in cols if "dept" in c or "department" in c), None),
        "title": next((c for c in cols if "title" in c or "file" in c or "name" in c or "upload" in c), None),
        "date": next((c for c in cols if "date" in c or "time" in c or "timestamp" in c), None),
        "sem": next((c for c in cols if "sem" in c or "year" in c), None),
        "id": next((c for c in cols if "id" in c or "link" in c or "url" in c or "file" in c or "upload" in c), None),
    }

_dialog_fn = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)

def _preview_iframe(fid):
    return (
        f'<iframe src="https://drive.google.com/file/d/{fid}/preview" width="100%" height="580" '
        f'style="border:0;border-radius:10px;background:#fff;" allow="autoplay" loading="lazy"></iframe>'
    )

def open_preview(title, fid):
    viewer_mode = st.session_state.get("viewer_mode_pref", "Popup Modal")
    if viewer_mode == "Full Width Inline":
        st.markdown(f"### 👁️ {esc(title)}")
        components.html(_preview_iframe(fid), height=600)
        c1, c2 = st.columns(2)
        with c1: st.link_button("↗ Open in new tab", f"https://drive.google.com/file/d/{fid}/view?usp=sharing", use_container_width=True)
        with c2: 
            if st.button(t("download"), key=f"inline_dl_{fid}", use_container_width=True):
                record_download(fid)
                st.markdown(f'<meta http-equiv="refresh" content="0;url=https://drive.google.com/uc?export=download&id={fid}">', unsafe_allow_html=True)
        st.markdown("---")
    else:
        @_dialog_fn(str(title)[:70] or "Preview", width="large")
        def _show():
            components.html(_preview_iframe(fid), height=580)
            c1, c2 = st.columns(2)
            with c1: st.link_button("↗ Open in new tab", f"https://drive.google.com/file/d/{fid}/view?usp=sharing", use_container_width=True)
            with c2: st.link_button(t("download"), f"https://drive.google.com/uc?export=download&id={fid}", use_container_width=True)
            st.caption(t("preview_note"))
        _show()

def render_cards(df, prefix, cols, paginate=True):
    cat_col, dept_col, title_col, date_col, sem_col = cols.get("cat"), cols.get("dept"), cols.get("title"), cols.get("date"), cols.get("sem")
    total = len(df)
    visible = st.session_state.get(f"{prefix}_visible", PAGE_SIZE) if paginate else total

    if paginate:
        st.markdown(f'<div class="result-bar"><span class="result-pill">{t("showing", shown=min(visible, total), total=total)}</span></div>', unsafe_allow_html=True)

    saved = st.session_state.get("saved", [])

    for pos, (idx, row) in enumerate(df.head(visible).iterrows()):
        dept_val = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else "General"
        cat_val = str(row[cat_col]) if cat_col and pd.notna(row[cat_col]) else "Material"
        title_val = str(row[title_col]) if title_col and pd.notna(row[title_col]) else f"Document #{idx+1}"
        date_val = str(row[date_col]) if date_col and pd.notna(row[date_col]) else t("recent")
        sem_val = str(row[sem_col]) if sem_col and pd.notna(row[sem_col]) else ""
        fid = row.get("_fid", "")
        has_file = _valid_fid(fid)

        ftype, ficon, fcolor = detect_file_type(title_val)
        dl_count = get_download_count(fid)
        avg_score, rating_count = get_avg_rating(fid)
        download_url = f"https://drive.google.com/uc?export=download&id={fid}" if has_file else "#"
        is_saved = fid in saved

        with st.container():
            st.markdown(f'<div class="card-item">', unsafe_allow_html=True)
            c_info, c_prev, c_dl, c_sv = st.columns([3.2, 1, 1, 1])
            with c_info:
                sem_badge = f'<span class="badge" style="background:#0F766E;">{esc(sem_val)}</span>' if sem_val else ''
                rating_str = f"⭐ {avg_score} ({rating_count})" if rating_count > 0 else "☆ No ratings"
                st.markdown(f"""
                <div>
                <span class="badge" style="background:{dept_color(dept_val)};">{esc(dept_label(dept_val))}</span>
                <span class="badge" style="background:#059669;">{esc(cat_label(cat_val))}</span>
                <span class="badge" style="background:{fcolor};">{ficon} {ftype}</span>
                {sem_badge}
                <h4 class="card-title">{esc(title_val)}</h4>
                <small class="card-date">🕒 {t("uploaded_on")}: {esc(date_val)} &nbsp;|&nbsp; 📥 {dl_count} {t("downloads_count")} &nbsp;|&nbsp; {rating_str}</small>
                </div>
                """, unsafe_allow_html=True)
            with c_prev:
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                if st.button(t("preview"), key=f"{prefix}_pv_{idx}", type="primary", disabled=not has_file, use_container_width=True):
                    open_preview(title_val, fid)
            with c_dl:
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                if has_file:
                    st.markdown(
                        f'<a href="{download_url}" target="_self" download style="display:block; text-align:center; background:linear-gradient(135deg, #10B981, #059669); color:white; padding:0.45rem 1rem; border-radius:8px; font-weight:600; text-decoration:none; box-shadow:0 2px 6px rgba(16,185,129,0.3);">⬇️ {t("download")}</a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.button(t("download"), key=f"{prefix}_dl_dis_{idx}", disabled=True, use_container_width=True)
            with c_sv:
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                if st.button(t("saved") if is_saved else t("save"), key=f"{prefix}_sv_{idx}", disabled=not has_file, use_container_width=True):
                    toggle_save(fid)
                    st.rerun()
            
            if has_file:
                with st.expander(f"⭐ {t('rating_label')}"):
                    r_col1, r_col2 = st.columns([2, 1])
                    with r_col1:
                        score = st.slider("Select rating", 1, 5, 5, key=f"rate_slider_{prefix}_{idx}")
                    with r_col2:
                        st.markdown("<div style='height:1.4rem;'></div>", unsafe_allow_html=True)
                        if st.button("Submit Rating", key=f"rate_btn_{prefix}_{idx}", use_container_width=True):
                            add_rating(fid, score)
                            st.success("Thank you for rating!")
                            st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    if paginate and total > visible:
        _, mid, _ = st.columns([1, 1, 1])
        with mid:
            if st.button(t("load_more", n=total - visible), key=f"{prefix}_more", use_container_width=True):
                st.session_state[f"{prefix}_visible"] = visible + PAGE_SIZE
                st.rerun()

# =====================================================================
# ADMIN DASHBOARD & ADVANCED ANALYTICS (FIXED UNIQUE KEYS)
# =====================================================================
def get_admin_password():
    try: return str(st.secrets["ADMIN_PASSWORD"])
    except Exception: return None

def remove_row(idx):
    deleted = st.session_state.get("deleted_rows", [])
    if idx not in deleted:
        deleted.append(idx)
        st.session_state["deleted_rows"] = deleted

def render_admin(df, cols, notices_count):
    st.markdown(f"### {t('admin_head')}")
    admin_pw = get_admin_password()
    if not admin_pw:
        st.info(t("admin_setup"))
        st.code('ADMIN_PASSWORD = "choose-a-strong-password"', language="toml")
        return

    if not st.session_state.get("admin_ok"):
        with st.form("admin_login_form"):
            pw = st.text_input(t("admin_pw"), type="password", key="admin_pw_input_field")
            submitted = st.form_submit_button(t("admin_login"), key="admin_login_submit_btn")
        if submitted:
            if hmac.compare_digest(pw.encode(), admin_pw.encode()):
                st.session_state["admin_ok"] = True
                st.rerun()
            else: st.error(t("admin_wrong"))
        return

    # Unique button key for admin logout to prevent StreamlitDuplicateElementId
    if st.button(t("admin_logout"), key="unique_admin_logout_btn_key"):
        st.session_state["admin_ok"] = False
        st.rerun()

    if df.empty:
        st.info(t("empty_repo"))
        return

    cat_col, dept_col, title_col, date_col = cols.get("cat"), cols.get("dept"), cols.get("title"), cols.get("date")
    parsed = parse_dates(df[date_col]) if date_col else pd.Series([pd.NaT] * len(df), index=df.index)
    total_downloads_all = sum(st.session_state.get("downloads", {}).values())

    st.markdown("#### 📊 Comprehensive Departmental Analytics Reports")
    an_col1, an_col2, an_col3 = st.columns(3)
    with an_col1:
        st.metric("Total Cataloged Resources", len(df))
    with an_col2:
        st.metric("Total Portal Downloads", total_downloads_all)
    with an_col3:
        active_depts = len([d for d in DEPARTMENT_FOLDERS if int(dept_mask(df[dept_col], d).sum()) > 0]) if dept_col else 0
        st.metric("Active Contributing Depts", f"{active_depts} / {len(DEPARTMENT_FOLDERS)}")

    if dept_col:
        dept_stats = []
        for d in DEPARTMENT_FOLDERS:
            d_count = int(dept_mask(df[dept_col], d).sum())
            if d_count > 0:
                dept_stats.append({"Department": d, "Documents": d_count})
        if dept_stats:
            st.bar_chart(pd.DataFrame(dept_stats).set_index("Department"))

    st.markdown("---")
    st.markdown(f"#### {t('adm_recent')}")
    recent = df.assign(_dt=parsed).sort_values("_dt", ascending=False, na_position="last").head(20)
    for idx, r in recent.iterrows():
        link_ok = _valid_fid(r["_fid"])
        title_str = str(r[title_col]) if title_col and pd.notna(r[title_col]) else '—'
        col_t, col_meta, col_del = st.columns([4, 3, 1])
        with col_t:
            st.markdown(f"**{esc(title_str)}**", unsafe_allow_html=True)
        with col_meta:
            st.markdown(f"<small>{t('link_ok') if link_ok else t('link_missing')}</small>", unsafe_allow_html=True)
        with col_del:
            if st.button(t("adm_delete"), key=f"del_{idx}", use_container_width=True):
                remove_row(idx)
                st.rerun()

# =====================================================================
# TOP CONTROLS & VIEWER TOGGLE
# =====================================================================
_toggle = getattr(st, "toggle", st.checkbox)
_, ctrl_lang, ctrl_dark, ctrl_viewer = st.columns([3, 1.8, 1.4, 2.2])
with ctrl_lang:
    st.radio("Language", ["en", "bn"], key="lang", horizontal=True, format_func=lambda x: {"en": "English", "bn": "বাংলা"}[x], label_visibility="collapsed")
with ctrl_dark:
    _toggle(t("dark_label"), key="dark_mode")
with ctrl_viewer:
    st.selectbox(t("viewer_mode"), ["Popup Modal", "Full Width Inline"], key="viewer_mode_pref", label_visibility="collapsed")

# HEADER WITH RESTORED VISITOR COUNTER
logo_b64 = get_base64_image("logo_pjc copy.jpg")
logo_html = f'<img class="portal-logo" src="data:image/jpeg;base64,{logo_b64}" alt="PJC Logo">' if logo_b64 else '<div class="portal-logo-fallback">🏛️</div>'
visitor_count_val = st.session_state.get("visitor_count", 12480)

st.markdown(f"""
<div class="portal-header">
{logo_html}
<div class="portal-header-text"><h1>{t("site_name")}</h1><p>{t("site_tagline")}</p></div>
<div style="margin-left:auto; display:flex; gap:0.8rem; align-items:center; flex-wrap:wrap;">
  <div class="visitor-badge">👁️ {t("visitors")}: <strong>{visitor_count_val:,}</strong></div>
  <div class="header-live"><span class="live-dot"></span>{t("live")}</div>
</div>
</div>
""", unsafe_allow_html=True)

# DATA LOADING & FILTERING
df_files = load_uploaded_files()
if not df_files.empty and st.session_state.get("deleted_rows"):
    df_files = df_files.drop(index=st.session_state["deleted_rows"], errors="ignore")

cols = detect_columns(df_files)
if not df_files.empty:
    df_files = df_files.copy()
    id_col = cols.get("id")
    df_files["_fid"] = df_files[id_col].map(extract_drive_id) if id_col else ""
    saved_present = df_files[df_files["_fid"].isin(st.session_state["saved"])]
    saved_count = saved_present["_fid"].nunique()
else:
    saved_present = df_files
    saved_count = 0

# --- NAVIGATION TABS ---
tab_browse, tab_popular, tab_saved, tab_upload, tab_admin = st.tabs([
    t("tab_browse"), t("tab_popular"), t("tab_saved", n=saved_count), t("tab_upload"), t("tab_admin")
])

# =====================================================================
# TAB 1: BROWSE REPOSITORY
# =====================================================================
with tab_browse:
    head_l, head_r = st.columns([5, 1])
    with head_l: st.markdown(f"### {t('explore')}")
    with head_r:
        refresh_clicked = st.button(t("refresh"), key="main_repo_refresh_btn", use_container_width=True)
        st.markdown("""
        <style>
        div.stButton > button:has(p:contains("Refresh")), div.stButton > button:has(p:contains("রিফ্রেশ")) {
            background: linear-gradient(135deg, #F59E0B, #EA580C) !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        div.stButton > button:has(p:contains("Save")), div.stButton > button:has(p:contains("Saved")), div.stButton > button:has(p:contains("সংরক্ষণ")) {
            background: linear-gradient(135deg, #F97316, #C2410C) !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if refresh_clicked:
            load_uploaded_files.clear()
            st.rerun()

    cat_col, dept_col, title_col, date_col, sem_col = cols.get("cat"), cols.get("dept"), cols.get("title"), cols.get("date"), cols.get("sem")

    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1.2, 1.1, 1.3, 1])
    with f_col1:
        selected_category = st.selectbox(t("category"), ["All", "Syllabus", "Study Material", "Assignment"], format_func=lambda x: {"All": t("all"), "Syllabus": t("syllabus"), "Study Material": t("study_material"), "Assignment": t("assignment")}[x])
    with f_col2:
        selected_dept = st.selectbox(t("department"), ["All Departments"] + DEPARTMENT_FOLDERS, format_func=lambda x: t("all_depts") if x == "All Departments" else dept_label(x))
    with f_col3:
        selected_sem = st.selectbox(t("semester"), ["All Semesters"] + [f"Semester {i}" for i in range(1, 9)], format_func=lambda x: t("all_sems") if x == "All Semesters" else x)
    with f_col4:
        selected_type = st.selectbox(t("file_type"), ["All Formats", "PDF", "Word", "Excel", "Presentation"], format_func=lambda x: t("all_types") if x == "All Formats" else x)
    with f_col5:
        search_query = st.text_input(t("search"), placeholder=t("search_ph"))

    st.markdown("---")

    if not df_files.empty:
        filtered_df = df_files.copy()
        if selected_category != "All" and cat_col:
            filtered_df = filtered_df[filtered_df[cat_col].astype(str).str.contains(selected_category, case=False, na=False)]
        if selected_dept != "All Departments" and dept_col:
            filtered_df = filtered_df[dept_mask(filtered_df[dept_col], selected_dept)]
        if selected_sem != "All Semesters" and sem_col:
            filtered_df = filtered_df[filtered_df[sem_col].astype(str).str.contains(selected_sem, case=False, na=False)]
        if selected_type != "All Formats":
            filtered_df = filtered_df[filtered_df[title_col].astype(str).str.contains(selected_type, case=False, na=False)]
        if search_query.strip():
            hay = pd.Series("", index=filtered_df.index)
            for c in (title_col, dept_col, cat_col):
                if c: hay = hay + " " + filtered_df[c].astype(str)
            filtered_df = filtered_df[hay.str.contains(search_query.strip(), case=False, na=False, regex=False)]

        if not filtered_df.empty:
            render_cards(filtered_df, "br", cols, paginate=True)
        else: st.warning(t("no_match"))
    else: st.info(t("empty_repo"))

# =====================================================================
# TAB 2: POPULAR RESOURCES & LEADERBOARD
# =====================================================================
with tab_popular:
    st.markdown(f"### {t('popular_head')}")
    if not df_files.empty:
        df_pop = df_files.copy()
        df_pop["_downloads"] = df_pop["_fid"].map(get_download_count)
        df_pop = df_pop.sort_values(by="_downloads", ascending=False).head(10)
        render_cards(df_pop, "pop", cols, paginate=False)
    else:
        st.info(t("empty_repo"))

# =====================================================================
# TAB 3: MY SAVED
# =====================================================================
with tab_saved:
    st.markdown(f"### {t('saved_head')}")
    st.caption(t("saved_note"))
    if saved_count:
        order = {f: i for i, f in enumerate(reversed(st.session_state["saved"]))}
        saved_view = saved_present.assign(_ord=saved_present["_fid"].map(order)).sort_values("_ord")
        st.button(t("saved_clear"), key="saved_clear_btn_main", on_click=clear_saved)
        render_cards(saved_view, "sv", cols, paginate=False)
    else: st.info(t("saved_empty"))

# =====================================================================
# TAB 4: UPLOAD PORTAL (Unique keys for Faculty Login / Logout)
# =====================================================================
with tab_upload:
    st.markdown(f"### {t('upload_head')}")
    admin_pw = get_admin_password()
    if not admin_pw: st.info(t("admin_setup"))
    elif not st.session_state.get("faculty_logged_in"):
        with st.form("faculty_login_portal_form"):
            fac_pw = st.text_input(t("faculty_pw"), type="password", key="faculty_password_input_field")
            fac_submitted = st.form_submit_button(t("faculty_login_btn"), key="faculty_login_submit_btn_key")
        if fac_submitted:
            if hmac.compare_digest(fac_pw.encode(), admin_pw.encode()):
                st.session_state["faculty_logged_in"] = True
                st.rerun()
            else: st.error(t("faculty_wrong"))
    else:
        if st.button(t("faculty_logout"), key="faculty_logout_unique_btn_key"):
            st.session_state["faculty_logged_in"] = False
            st.rerun()
        st.link_button(t("open_form"), FORM_DIRECT_URL, use_container_width=True)

# =====================================================================
# TAB 5: ADMIN & ANALYTICS
# =====================================================================
with tab_admin:
    render_admin(df_files, cols, 0)

# FOOTER
st.markdown(f"""
<div class="institutional-footer">
<p>{t("footer_rights")}</p>
<p>{t("footer_by")}</p>
</div>
""", unsafe_allow_html=True)
sync_query_params()
