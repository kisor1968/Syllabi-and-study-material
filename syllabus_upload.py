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
        "search": "Search",
        "search_ph": "🔎 Search by title, e.g. 'CBCS Semester 3'",
        "sort_by": "Sort by",
        "all": "All",
        "all_depts": "All Departments",
        "syllabus": "Syllabus",
        "study_material": "Study Material",
        "assignment": "Assignment",
        "newest": "Newest first",
        "oldest": "Oldest first",
        "az": "Title A–Z",
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
        "tab_browse": "📂 Browse Repository & Syllabi",
        "tab_saved": "⭐ My Saved ({n})",
        "tab_upload": "📤 Upload New Materials",
        "tab_admin": "🔐 Admin",
        "saved_head": "⭐ My Saved Documents",
        "saved_note": "Your saved list is kept in this page's address (URL). Bookmark the page to keep it.",
        "saved_empty": "Nothing saved yet. Press ☆ Save under any document to add it here.",
        "saved_clear": "🗑️ Clear all",
        "upload_head": "🚀 Secure Material Submission",
        "upload_intro": "Click below to open the secure Google Form. Submissions automatically log to the master directory and update this repository portal in real-time.",
        "step1_t": "Open the form", "step1_d": "Use the secure upload button below.",
        "step2_t": "Fill in the details", "step2_d": "Choose the category and department, then attach your file.",
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
        "admin_head": "🔐 Admin Dashboard",
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
        "adm_notices_on": "Notices source: connected ({n} active)",
        "adm_notices_off": "Notices source: not configured (ANNOUNCEMENTS_CSV_URL)",
        "col_date": "Date", "col_dept": "Department", "col_cat": "Category", "col_title": "Title", "col_link": "File link", "col_actions": "Actions",
        "link_ok": "✔ Yes", "link_missing": "✘ Missing",
        "adm_delete": "🗑️ Remove",
    },
    "bn": {
        "site_name": "প্রভু জগদ্বন্ধু কলেজ",
        "site_tagline": "একাডেমিক রিপোজিটরি ও সিলেবাস ব্যবস্থাপনা পোর্টাল",
        "live": "লাইভ রিপোজিটরি",
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
        "search": "অনুসন্ধান",
        "search_ph": "🔎 শিরোনাম দিয়ে খুঁজুন, যেমন 'CBCS সেমিস্টার ৩'",
        "sort_by": "সাজান",
        "all": "সব",
        "all_depts": "সব বিভাগ",
        "syllabus": "সিলেবাস",
        "study_material": "পাঠ্যসামগ্রী",
        "assignment": "অ্যাসাইনমেন্ট",
        "newest": "নতুন আগে",
        "oldest": "পুরনো আগে",
        "az": "শিরোনাম অনুযায়ী",
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
        "tab_browse": "📂 রিপোজিটরি ও সিলেবাস দেখুন",
        "tab_saved": "⭐ আমার সংরক্ষিত ({n})",
        "tab_upload": "📤 নতুন সামগ্রী আপলোড",
        "tab_admin": "🔐 অ্যাডমিন",
        "saved_head": "⭐ আমার সংরক্ষিত নথি",
        "saved_note": "সংরক্ষিত তালিকা এই পেজের ঠিকানায় (URL) জমা থাকে। তালিকা রাখতে পেজটি বুকমার্ক করুন।",
        "saved_empty": "এখনও কিছু সংরক্ষণ করা হয়নি। কোনো নথির নিচে ☆ সংরক্ষণ চাপুন।",
        "saved_clear": "🗑️ সব মুছুন",
        "upload_head": "🚀 নিরাপদ সামগ্রী জমা",
        "upload_intro": "নিচের বোতামে ক্লিক করে নিরাপদ Google Form খুলুন। জমা দেওয়া নথি স্বয়ংক্রিয়ভাবে মূল তালিকায় যুক্ত হয় এবং এই পোর্টালে রিয়েল-টাইমে দেখা যায়।",
        "step1_t": "ফর্মটি খুলুন", "step1_d": "নিচের নিরাপদ আপলোড বোতামটি ব্যবহার করুন।",
        "step2_t": "বিবরণ পূরণ করুন", "step2_d": "ধরন ও বিভাগ বেছে নিন, তারপর ফাইল সংযুক্ত করুন।",
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
        "admin_head": "🔐 অ্যাডমিন ড্যাশবোর্ড",
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
        "adm_notices_on": "নোটিশ উৎস: যুক্ত আছে ({n} টি সক্রিয়)",
        "adm_notices_off": "নোটিশ উৎস: কনফিগার করা হয়নি (ANNOUNCEMENTS_CSV_URL)",
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
# SESSION STATE
# =====================================================================
def _valid_fid(fid):
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{10,}", str(fid or "")))

if "init_done" not in st.session_state:
    qp = st.query_params
    st.session_state["lang"] = "bn" if qp.get("lang") == "bn" else "en"
    st.session_state["dark_mode"] = qp.get("theme") == "dark"
    st.session_state["saved"] = [s for s in str(qp.get("saved", "")).split(",") if _valid_fid(s)][:60]
    st.session_state["deleted_rows"] = []
    st.session_state["init_done"] = True

def toggle_save(fid):
    saved = list(st.session_state.get("saved", []))
    if fid in saved:
        saved.remove(fid)
    else:
        saved.append(fid)
    st.session_state["saved"] = saved[-60:]

def clear_saved():
    st.session_state["saved"] = []

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
# THEME & STYLING
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

html, body, [class*="css"], .stApp, .stMarkdown, button, input, select, textarea {
    font-family: 'Plus Jakarta Sans', 'Noto Sans Bengali', 'Segoe UI', sans-serif;
}
.stApp {
    background:
        radial-gradient(1100px 500px at 90% -10%, var(--glow1), transparent 60%),
        radial-gradient(900px 450px at -10% 10%, var(--glow2), transparent 55%),
        var(--bg);
    color: var(--text);
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1200px; }

.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--text); }
.stApp label p, .stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stCaptionContainer"] { color: var(--text); }
.stApp hr { border-color: var(--border); }
.stApp [data-baseweb="input"], .stApp [data-baseweb="base-input"], .stApp [data-baseweb="select"] > div {
    background-color: var(--surface) !important; border-color: var(--border) !important;
}
.stApp [data-baseweb="input"] input, .stApp [data-baseweb="base-input"] input {
    color: var(--text) !important; -webkit-text-fill-color: var(--text) !important;
}
.stApp input::placeholder { color: var(--muted) !important; -webkit-text-fill-color: var(--muted) !important; }
.stApp [data-baseweb="select"] div { color: var(--text); }
.stApp [data-baseweb="select"] svg { fill: var(--muted); }
[data-baseweb="popover"] > div, [data-baseweb="popover"] ul, [data-baseweb="menu"] { background-color: var(--surface) !important; }
[data-baseweb="popover"] li, [data-baseweb="popover"] li * { color: var(--text) !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] { background-color: var(--hover-bg) !important; }
.stApp [data-testid="stExpander"] details { background: var(--surface); border-color: var(--border); border-radius: 12px; }
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] summary * { color: var(--text); }
.stApp [data-testid="stAlert"] { background-color: var(--surface); border: 1px solid var(--border); }
.stApp [data-testid="stAlert"] * { color: var(--text); }
.stApp [data-testid="stForm"] { background: var(--surface); border-color: var(--border); border-radius: 12px; }
div[role="dialog"] { background-color: var(--surface) !important; color: var(--text); }
div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, div[role="dialog"] p { color: var(--text); }

.stApp div.stButton > button, .stApp [data-testid="stDownloadButton"] button, .stApp [data-testid="stFormSubmitButton"] button {
    background: var(--surface); color: var(--text); border: 1px solid var(--border);
    border-radius: 10px; font-weight: 700;
    transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.stApp button p { color: inherit; }
.stApp div.stButton > button:hover:not(:disabled) { transform: translateY(-1px); border-color: #2563EB; color: var(--accent-text); }
.stApp div.stButton > button[kind="primary"], .stApp div.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #2563EB, #1D4ED8); color: #FFFFFF; border: none;
    box-shadow: 0 3px 8px rgba(37, 99, 235, 0.28);
}
.stApp div.stButton > button[kind="primary"]:hover:not(:disabled), .stApp div.stButton > button[data-testid="stBaseButton-primary"]:hover:not(:disabled) { color: #FFFFFF; filter: brightness(1.1); }
div[data-testid="stLinkButton"] a {
    background: linear-gradient(135deg, #F59E0B, #FF7700);
    color: #FFFFFF !important; border: none; border-radius: 10px; font-weight: 700; padding: 0.7rem 1rem;
    box-shadow: 0 6px 16px rgba(255, 119, 0, 0.35);
    transition: transform 0.15s ease, box-shadow 0.2s ease;
}
div[data-testid="stLinkButton"] a:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(255, 119, 0, 0.45); }

/* ---------- HEADER ---------- */
.portal-header {
    position: relative; overflow: hidden;
    background: linear-gradient(120deg, #1E3A8A, #2563EB, #3B82F6, #1E3A8A);
    background-size: 300% 300%;
    animation: headerFlow 14s ease infinite, riseIn 0.7s ease both;
    padding: 1.8rem 2rem; border-radius: 16px; color: #FFFFFF;
    display: flex; align-items: center; flex-wrap: wrap; gap: 1.4rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 12px 28px -8px rgba(30, 58, 138, 0.45);
    border-bottom: 4px solid #F59E0B;
}
.portal-header::before, .portal-header::after { content: ""; position: absolute; border-radius: 50%; pointer-events: none; }
.portal-header::before { width: 260px; height: 260px; right: -60px; top: -110px; background: radial-gradient(circle, rgba(255,153,51,0.35), transparent 70%); animation: floaty 9s ease-in-out infinite; }
.portal-header::after { width: 180px; height: 180px; right: 180px; bottom: -110px; background: radial-gradient(circle, rgba(255,255,255,0.18), transparent 70%); animation: floaty 11s ease-in-out infinite reverse; }
.portal-logo { height: 78px; width: auto; border-radius: 10px; background: #FFFFFF; padding: 5px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); position: relative; z-index: 1; }
.portal-logo-fallback { font-size: 2.4rem; position: relative; z-index: 1; }
.portal-header-text { position: relative; z-index: 1; }
.stApp .portal-header-text h1 { color: #FFFFFF !important; margin: 0; padding: 0; font-size: 2.15rem; font-weight: 800; line-height: 1.2; letter-spacing: -0.01em; }
.stApp .portal-header-text p { color: #E2E8F0 !important; margin: 0.35rem 0 0 0; font-size: 1.05rem; }
.header-live {
    margin-left: auto; position: relative; z-index: 1;
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.28);
    padding: 0.4rem 0.9rem; border-radius: 999px; font-size: 0.85rem; font-weight: 600;
    backdrop-filter: blur(4px); color: #FFFFFF;
}
.live-dot { width: 9px; height: 9px; border-radius: 50%; background: #34D399; box-shadow: 0 0 0 0 rgba(52,211,153,0.7); animation: pulse 1.8s infinite; }

/* ---------- ANNOUNCEMENT TICKER ---------- */
.notice-bar {
    display: flex; align-items: center; gap: 0.9rem;
    background: var(--notice-bg); border: 1px solid var(--border); border-left: 5px solid #F59E0B;
    border-radius: 12px; padding: 0.6rem 0.9rem; margin: 0 0 1.2rem 0;
    box-shadow: 0 4px 12px var(--shadow); animation: riseIn 0.6s ease both;
}
.notice-label { flex: 0 0 auto; background: linear-gradient(135deg, #F59E0B, #FF7700); color: #FFFFFF; font-weight: 800; font-size: 0.82rem; padding: 3px 12px; border-radius: 999px; }
.ticker { flex: 1; overflow: hidden; -webkit-mask-image: linear-gradient(90deg, transparent, #000 4%, #000 96%, transparent); mask-image: linear-gradient(90deg, transparent, #000 4%, #000 96%, transparent); }
.ticker-track { display: inline-flex; white-space: nowrap; animation: tick linear infinite; }
.ticker:hover .ticker-track { animation-play-state: paused; }
.ticker-item { margin-right: 3.5rem; color: var(--text); font-weight: 600; font-size: 0.92rem; }
.ticker-item a, .notice-list a { color: var(--link) !important; text-decoration: underline; }
.notice-list { margin: 0; padding-left: 1.1rem; color: var(--text); }
.notice-list li { margin: 0.35rem 0; }

/* ---------- STAT TILES ---------- */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin: 0.4rem 0 1.2rem 0; }
.stat-tile {
    background: var(--surface); border: 1px solid var(--border); border-left: 5px solid var(--accent, #2563EB);
    border-radius: 14px; padding: 1rem 1.2rem; display: flex; align-items: center; gap: 0.9rem;
    box-shadow: 0 4px 12px var(--shadow); animation: riseIn 0.6s ease both;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-tile:hover { transform: translateY(-3px); box-shadow: 0 10px 22px var(--shadow-hover); }
.stat-icon { width: 46px; height: 46px; flex: 0 0 46px; border-radius: 12px; display: grid; place-items: center; font-size: 1.4rem; background: color-mix(in srgb, var(--accent, #2563EB) 16%, var(--surface)); }
.stat-num { font-size: 1.7rem; font-weight: 800; color: var(--stat-num); line-height: 1.1; }
.stat-label { font-size: 0.82rem; color: var(--muted); font-weight: 600; }

/* ---------- RESULT CARDS ---------- */
.card-item {
    background: var(--surface); padding: 1.3rem 1.6rem; border-radius: 14px;
    box-shadow: 0 4px 12px var(--shadow); border: 1px solid var(--border); border-top: 4px solid #FF9933;
    position: relative; margin-bottom: 0.8rem; animation: riseIn 0.55s ease both;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.card-item::before { content: ""; position: absolute; top: -4px; left: -1px; width: 50%; height: 4px; background-color: #FF7700; border-top-left-radius: 14px; transition: width 0.45s ease; }
.card-item:hover { transform: translateY(-3px); box-shadow: 0 14px 28px var(--shadow-hover); border-color: var(--card-hover-border); }
.card-item:hover::before { width: calc(100% + 2px); border-top-right-radius: 14px; }
.badge { display: inline-block; color: #FFFFFF; padding: 3px 11px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; margin-right: 6px; }
.badge-new { background: linear-gradient(135deg, #F59E0B, #EF4444); animation: pulse-soft 2s ease-in-out infinite; }
.stApp .card-title { margin: 0.4rem 0 0.2rem 0; color: var(--text); font-size: 1.1rem; font-weight: 700; overflow-wrap: anywhere; }
.card-date { color: var(--muted); font-size: 0.82rem; }

/* ---------- RESULT BAR & BARS ---------- */
.result-bar { display: flex; align-items: center; justify-content: space-between; margin: 0.2rem 0 1rem 0; color: var(--muted); font-size: 0.92rem; font-weight: 600; }
.result-pill { background: var(--pill-bg); color: var(--pill-text); padding: 3px 12px; border-radius: 999px; font-weight: 700; }
.dept-row { display: flex; align-items: center; gap: 0.8rem; margin: 0.45rem 0; font-size: 0.88rem; color: var(--text); font-weight: 600; }
.dept-name { flex: 0 0 150px; }
.dept-track { flex: 1; height: 10px; background: var(--track); border-radius: 999px; overflow: hidden; }
.dept-fill { display: block; height: 100%; border-radius: 999px; background: linear-gradient(90deg, #2563EB, #F59E0B); transform-origin: left; animation: grow 1s ease both; }
.dept-count { flex: 0 0 32px; text-align: right; color: var(--accent-text); }

/* ---------- UPLOAD TAB ---------- */
.stApp .note-text { color: var(--text); margin: 0; }
.upload-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin: 1rem 0 1.4rem 0; }
.step-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1.1rem 1.2rem; box-shadow: 0 4px 12px var(--shadow); animation: riseIn 0.6s ease both; transition: transform 0.2s ease; }
.step-card:hover { transform: translateY(-3px); }
.step-no { width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; background: linear-gradient(135deg, #F59E0B, #FF7700); color: #FFFFFF; font-weight: 800; margin-bottom: 0.6rem; }
.stApp .step-card h4 { margin: 0 0 0.25rem 0; color: var(--text); font-size: 1rem; }
.stApp .step-card p { margin: 0; color: var(--muted); font-size: 0.88rem; }

/* ---------- ADMIN ---------- */
.admin-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1rem 1.2rem; box-shadow: 0 4px 12px var(--shadow); margin-bottom: 1rem; }
.stApp .admin-panel h4 { margin: 0 0 0.6rem 0; font-size: 1rem; color: var(--text); }
.issue-list { margin: 0; padding-left: 1.1rem; color: var(--text); font-size: 0.9rem; }
.issue-list li { margin: 0.3rem 0; }
.ok-text { color: #059669; font-weight: 700; }

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; border-bottom: 2px solid var(--border); flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { height: 48px; padding: 0 1.2rem; border-radius: 10px 10px 0 0; font-weight: 700; color: var(--muted); transition: background 0.2s ease, color 0.2s ease; }
.stTabs [data-baseweb="tab"]:hover { background: var(--hover-bg); color: var(--accent-text); }
.stTabs [aria-selected="true"] { color: var(--pill-text) !important; background: var(--pill-bg); }
.stTabs [data-baseweb="tab-highlight"] { background-color: #F59E0B !important; height: 3px; }

/* ---------- FOOTER ---------- */
.institutional-footer { background: linear-gradient(135deg, #1E3A8A, #1E40AF); color: #FFFFFF; text-align: center; padding: 1.6rem 1rem; border-radius: 14px; margin-top: 3rem; box-shadow: 0 -4px 10px rgba(0,0,0,0.05); border-top: 3px solid #F59E0B; }
.stApp .institutional-footer p { margin: 0.3rem 0; color: #F8FAFC; font-size: 0.9rem; }
.visitor-counter { margin-top: 0.8rem; }

/* ---------- MOTION ---------- */
@keyframes headerFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes floaty { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(14px); } }
@keyframes riseIn { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.7); } 70% { box-shadow: 0 0 0 10px rgba(52,211,153,0); } 100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); } }
@keyframes pulse-soft { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.07); } }
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes tick { from { transform: translateX(0); } to { transform: translateX(-50%); } }

@media (max-width: 720px) {
    .stApp .portal-header-text h1 { font-size: 1.6rem; }
    .header-live { margin-left: 0; }
    .dept-name { flex-basis: 100px; }
    .notice-bar { flex-wrap: wrap; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
    .ticker { overflow: visible; -webkit-mask-image: none; mask-image: none; }
    .ticker-track { display: block; white-space: normal; }
}
"""
st.markdown("<style>" + (DARK_VARS if dark else LIGHT_VARS) + BASE_CSS + "</style>", unsafe_allow_html=True)

# =====================================================================
# HELPERS
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

@st.cache_data(ttl=60)
def load_announcements():
    if not ANNOUNCEMENTS_CSV_URL:
        return pd.DataFrame()
    try:
        df = pd.read_csv(ANNOUNCEMENTS_CSV_URL)
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

def match_dept(name):
    low = str(name).lower()
    for d in sorted(DEPARTMENT_FOLDERS, key=len, reverse=True):
        if d.lower() in low:
            return d
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
    if d:
        return DEPT_COLORS[DEPARTMENT_FOLDERS.index(d) % len(DEPT_COLORS)]
    return "#475569"

def dept_label(name):
    if st.session_state.get("lang") == "bn":
        d = match_dept(name)
        if d:
            return DEPT_BN.get(d, d)
    return name

def cat_label(value):
    if st.session_state.get("lang") == "bn":
        low = str(value).lower()
        if "syllabus" in low:
            return t("syllabus")
        if "study" in low:
            return t("study_material")
        if "assignment" in low:
            return t("assignment")
    return value

def esc(v):
    return html.escape(str(v), quote=True)

def bar_rows(items):
    if not items:
        return ""
    max_n = max(n for _, n in items) or 1
    return "".join(
        f'<div class="dept-row"><span class="dept-name">{esc(label)}</span>'
        f'<span class="dept-track"><span class="dept-fill" style="width:{n / max_n * 100:.0f}%;"></span></span>'
        f'<span class="dept-count">{n}</span></div>'
        for label, n in items
    )

def detect_columns(df):
    if df.empty:
        return {}
    cols = df.columns
    return {
        "cat": next((c for c in cols if "cat" in c or "type" in c), None),
        "dept": next((c for c in cols if "dept" in c or "department" in c), None),
        "title": next((c for c in cols if "title" in c or "file" in c or "name" in c or "upload" in c), None),
        "date": next((c for c in cols if "date" in c or "time" in c or "timestamp" in c), None),
        "id": next((c for c in cols if "id" in c or "link" in c or "url" in c or "file" in c or "upload" in c), None),
    }

# =====================================================================
# ANNOUNCEMENTS
# =====================================================================
def get_notices(df, lang):
    notices = []
    if df.empty:
        return notices
    cols = list(df.columns)
    bn_col = next((c for c in cols if "bengali" in c or c == "bn" or c.endswith("_bn")), None)
    msg_col = next((c for c in cols if c != bn_col and any(k in c for k in ("message", "notice", "announcement", "title", "text"))), None)
    link_col = next((c for c in cols if "link" in c or "url" in c), None)
    active_col = next((c for c in cols if any(k in c for k in ("active", "show", "visible", "display"))), None)
    exp_col = next((c for c in cols if any(k in c for k in ("expir", "until", "valid"))), None)
    if not msg_col:
        return notices
    today = datetime.now().date()
    for _, r in df.iterrows():
        text = str(r[msg_col]).strip() if pd.notna(r[msg_col]) else ""
        if lang == "bn" and bn_col and pd.notna(r[bn_col]) and str(r[bn_col]).strip():
            text = str(r[bn_col]).strip()
        if not text:
            continue
        if active_col and pd.notna(r[active_col]) and str(r[active_col]).strip().lower() in {"no", "false", "0", "n", "hide", "inactive"}:
            continue
        if exp_col and pd.notna(r[exp_col]):
            exp = pd.to_datetime(r[exp_col], errors="coerce")
            if pd.notna(exp) and exp.date() < today:
                continue
        link = str(r[link_col]).strip() if link_col and pd.notna(r[link_col]) else ""
        if link and not link.lower().startswith(("http://", "https://")):
            link = ""
        notices.append({"text": text, "link": link})
    return notices

def _notice_html(n):
    body = esc(n["text"])
    if n["link"]:
        body = f'<a href="{esc(n["link"])}" target="_blank" rel="noopener">{body}</a>'
    return body

def render_notices(notices):
    if not notices:
        return
    items = "".join(f'<span class="ticker-item">📌 {_notice_html(n)}</span>' for n in notices)
    duration = max(20, int(sum(len(n["text"]) for n in notices) * 0.28))
    st.markdown(
        f'<div class="notice-bar"><span class="notice-label">{t("notices")}</span>'
        f'<div class="ticker"><div class="ticker-track" style="animation-duration:{duration}s;">{items}{items}</div></div></div>',
        unsafe_allow_html=True,
    )
    if len(notices) > 1:
        with st.expander(t("all_notices", n=len(notices))):
            lis = "".join(f"<li>{_notice_html(n)}</li>" for n in notices)
            st.markdown(f'<ul class="notice-list">{lis}</ul>', unsafe_allow_html=True)

# =====================================================================
# PREVIEW DIALOG
# =====================================================================
_dialog_fn = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)

def _preview_iframe(fid):
    return (
        f'<iframe src="https://drive.google.com/file/d/{fid}/preview" width="100%" height="580" '
        f'style="border:0;border-radius:10px;background:#fff;" allow="autoplay" loading="lazy"></iframe>'
    )

def _preview_links(fid):
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("↗ Open in new tab", f"https://drive.google.com/file/d/{fid}/view?usp=sharing", use_container_width=True)
    with c2:
        st.link_button(t("download"), f"https://drive.google.com/uc?export=download&id={fid}", use_container_width=True)
    st.caption(t("preview_note"))

def open_preview(title, fid):
    @_dialog_fn(str(title)[:70] or "Preview", width="large")
    def _show():
        components.html(_preview_iframe(fid), height=590)
        _preview_links(fid)

    _show()

# =====================================================================
# CARD RENDERING
# =====================================================================
def render_cards(df, prefix, cols, paginate=True):
    cat_col, dept_col, title_col, date_col = cols.get("cat"), cols.get("dept"), cols.get("title"), cols.get("date")
    total = len(df)
    visible = st.session_state.get(f"{prefix}_visible", PAGE_SIZE) if paginate else total

    if paginate:
        st.markdown(
            f'<div class="result-bar"><span class="result-pill">{t("showing", shown=min(visible, total), total=total)}</span></div>',
            unsafe_allow_html=True,
        )

    now = datetime.now()
    saved = st.session_state.get("saved", [])

    for pos, (idx, row) in enumerate(df.head(visible).iterrows()):
        dept_val = str(row[dept_col]) if dept_col and pd.notna(row[dept_col]) else "General"
        cat_val = str(row[cat_col]) if cat_col and pd.notna(row[cat_col]) else "Material"
        title_val = str(row[title_col]) if title_col and pd.notna(row[title_col]) else f"Document #{idx+1}"
        date_val = str(row[date_col]) if date_col and pd.notna(row[date_col]) else t("recent")
        fid = row.get("_fid", "")
        has_file = _valid_fid(fid)

        if has_file:
            download_url = f"https://drive.google.com/uc?export=download&id={fid}"
        else:
            download_url = "#"

        new_badge = ""
        if date_col:
            try:
                dt = pd.to_datetime(row[date_col], errors="coerce")
                if pd.notna(dt) and now - dt.to_pydatetime() <= timedelta(days=7):
                    new_badge = f'<span class="badge badge-new">{t("new")}</span>'
            except Exception:
                pass

        delay = min(pos * 0.06, 0.5)

        with st.container():
            st.markdown(f'<div class="card-item" style="animation-delay:{delay:.2f}s;">', unsafe_allow_html=True)
            c_info, c_prev, c_dl, c_sv = st.columns([3.2, 1, 1, 1])
            with c_info:
                st.markdown(f"""
                <div>
                <span class="badge" style="background:{dept_color(dept_val)};">{esc(dept_label(dept_val))}</span>
                <span class="badge" style="background:#059669;">{esc(cat_label(cat_val))}</span>
                {new_badge}
                <h4 class="card-title">{esc(title_val)}</h4>
                <small class="card-date">🕒 {t("uploaded_on")}: {esc(date_val)}</small>
                </div>
                """, unsafe_allow_html=True)
            with c_prev:
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                if st.button(t("preview"), key=f"{prefix}_pv_{idx}", type="primary", disabled=not has_file, use_container_width=True):
                    open_preview(title_val, fid)
            with c_dl:
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                if has_file:
                    st.link_button(t("download"), download_url, use_container_width=True)
                else:
                    st.button(t("download"), key=f"{prefix}_dl_{idx}", disabled=True, use_container_width=True)
            with c_sv:
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                st.button(
                    t("saved") if fid in saved else t("save"),
                    key=f"{prefix}_sv_{idx}",
                    disabled=not has_file,
                    on_click=toggle_save,
                    args=(fid,),
                    use_container_width=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        if _dialog_fn is None and has_file and st.session_state.get("inline_preview") == fid:
            components.html(_preview_iframe(fid), height=590)
            _preview_links(fid)

    if paginate and total > visible:
        _, mid, _ = st.columns([1, 1, 1])
        with mid:
            if st.button(t("load_more", n=total - visible), key=f"{prefix}_more", use_container_width=True):
                st.session_state[f"{prefix}_visible"] = visible + PAGE_SIZE
                st.rerun()

# =====================================================================
# ADMIN & DELETE HANDLER
# =====================================================================
def get_admin_password():
    try:
        val = st.secrets["ADMIN_PASSWORD"]
        return str(val) if val else None
    except Exception:
        return None

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
            pw = st.text_input(t("admin_pw"), type="password")
            submitted = st.form_submit_button(t("admin_login"))
        if submitted:
            if st.session_state.get("admin_fail", 0) >= 5:
                st.error(t("admin_lockout"))
            elif hmac.compare_digest(pw.encode(), admin_pw.encode()):
                st.session_state["admin_ok"] = True
                st.session_state["admin_fail"] = 0
                st.rerun()
            else:
                st.session_state["admin_fail"] = st.session_state.get("admin_fail", 0) + 1
                st.error(t("admin_wrong"))
        return

    if st.button(t("admin_logout")):
        st.session_state["admin_ok"] = False
        st.rerun()

    if df.empty:
        st.info(t("empty_repo"))
        return

    cat_col, dept_col, title_col, date_col = cols.get("cat"), cols.get("dept"), cols.get("title"), cols.get("date")
    parsed = parse_dates(df[date_col]) if date_col else pd.Series([pd.NaT] * len(df), index=df.index)
    now = pd.Timestamp.now()
    has_dates = parsed.notna().any()
    this_month = int(((parsed.dt.year == now.year) & (parsed.dt.month == now.month)).sum()) if has_dates else 0
    last_week = int((parsed >= now - pd.Timedelta(days=7)).sum()) if has_dates else 0
    nolink_mask = ~df["_fid"].map(_valid_fid)

    st.markdown(f"""
<div class="stat-grid">
<div class="stat-tile" style="--accent:#2563EB;"><div class="stat-icon">📚</div><div><div class="stat-num">{len(df)}</div><div class="stat-label">{t("adm_total")}</div></div></div>
<div class="stat-tile" style="--accent:#F59E0B;"><div class="stat-icon">🗓️</div><div><div class="stat-num">{this_month}</div><div class="stat-label">{t("adm_month")}</div></div></div>
<div class="stat-tile" style="--accent:#10B981;"><div class="stat-icon">⚡</div><div><div class="stat-num">{last_week}</div><div class="stat-label">{t("adm_week")}</div></div></div>
<div class="stat-tile" style="--accent:#EF4444;"><div class="stat-icon">⚠️</div><div><div class="stat-num">{int(nolink_mask.sum())}</div><div class="stat-label">{t("adm_nolink")}</div></div></div>
</div>
""", unsafe_allow_html=True)

    month_items = []
    if has_dates:
        counts = parsed.dropna().dt.to_period("M").value_counts().sort_index().tail(12)
        month_items = [(str(p), int(n)) for p, n in counts.items()]
    dept_counts = {}
    if dept_col:
        for d in DEPARTMENT_FOLDERS:
            dept_counts[d] = int(dept_mask(df[dept_col], d).sum())
    dept_items = sorted([(dept_label(d), n) for d, n in dept_counts.items() if n], key=lambda x: -x[1])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="admin-panel"><h4>{t("adm_by_month")}</h4>{bar_rows(month_items)}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="admin-panel"><h4>{t("adm_by_dept")}</h4>{bar_rows(dept_items)}</div>', unsafe_allow_html=True)

    cat_items = []
    if cat_col:
        vc = df[cat_col].fillna("—").astype(str).str.strip().value_counts().head(8)
        cat_items = [(cat_label(k), int(v)) for k, v in vc.items()]
    empty_depts = [dept_label(d) for d, n in dept_counts.items() if n == 0] if dept_col else []

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f'<div class="admin-panel"><h4>{t("adm_by_cat")}</h4>{bar_rows(cat_items)}</div>', unsafe_allow_html=True)
    with c4:
        body = (
            "".join(f'<span class="badge" style="background:#B45309;margin-bottom:6px;">{esc(d)}</span>' for d in empty_depts)
            if empty_depts else f'<span class="ok-text">✔ {t("adm_all_covered")}</span>'
        )
        st.markdown(f'<div class="admin-panel"><h4>{t("adm_empty_depts")}</h4>{body}</div>', unsafe_allow_html=True)

    def _titles(mask):
        if not title_col:
            return ""
        return "; ".join(esc(x)[:60] for x in df.loc[mask, title_col].astype(str).head(5))

    issues = []
    if nolink_mask.any():
        issues.append((t("adm_issue_nolink"), int(nolink_mask.sum()), _titles(nolink_mask)))
    if dept_col:
        m = df[dept_col].isna() | (df[dept_col].astype(str).str.strip() == "")
        if m.any():
            issues.append((t("adm_issue_nodept"), int(m.sum()), _titles(m)))
    if cat_col:
        m = df[cat_col].isna() | (df[cat_col].astype(str).str.strip() == "")
        if m.any():
            issues.append((t("adm_issue_nocat"), int(m.sum()), _titles(m)))
    if title_col and dept_col:
        m = df.duplicated(subset=[title_col, dept_col], keep=False)
        if m.any():
            issues.append((t("adm_issue_dup"), int(m.sum()), _titles(m)))
    issue_html = (
        '<ul class="issue-list">' + "".join(f"<li><b>{lbl}: {n}</b> — {names}</li>" for lbl, n, names in issues) + "</ul>"
        if issues else f'<span class="ok-text">✔ {t("adm_none_attention")}</span>'
    )
    st.markdown(f'<div class="admin-panel"><h4>{t("adm_attention")}</h4>{issue_html}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="admin-panel"><h4>{t("adm_recent")}</h4>', unsafe_allow_html=True)
    recent = df.assign(_dt=parsed).sort_values("_dt", ascending=False, na_position="last").head(20)
    for idx, r in recent.iterrows():
        link_ok = _valid_fid(r["_fid"])
        dt_str = str(r[date_col]) if date_col and pd.notna(r[date_col]) else '—'
        dept_str = str(dept_label(r[dept_col])) if dept_col and pd.notna(r[dept_col]) else '—'
        cat_str = str(cat_label(r[cat_col])) if cat_col and pd.notna(r[cat_col]) else '—'
        title_str = str(r[title_col]) if title_col and pd.notna(r[title_col]) else '—'
        
        col_t, col_meta, col_del = st.columns([4, 3, 1])
        with col_t:
            st.markdown(f"**{esc(title_str)}**<br><small style='color:var(--muted);'>{dt_str} | {dept_str} ({cat_str})</small>", unsafe_allow_html=True)
        with col_meta:
            st.markdown(f"<small>{t('link_ok') if link_ok else t('link_missing')}</small>", unsafe_allow_html=True)
        with col_del:
            if st.button(t("adm_delete"), key=f"del_{idx}", use_container_width=True):
                remove_row(idx)
                st.rerun()
        st.markdown("<hr style='margin:0.4rem 0;'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    export_df = df.drop(columns=[c for c in df.columns if c.startswith("_")])
    st.download_button(t("adm_export"), export_df.to_csv(index=False).encode("utf-8-sig"),
                       file_name="pjc_repository_catalog.csv", mime="text/csv")
    st.caption(t("adm_notices_on", n=notices_count) if ANNOUNCEMENTS_CSV_URL else t("adm_notices_off"))

# =====================================================================
# TOP CONTROLS: language + dark mode
# =====================================================================
_toggle = getattr(st, "toggle", st.checkbox)
_, ctrl_lang, ctrl_dark = st.columns([5, 2.4, 1.8])
with ctrl_lang:
    st.radio(
        "Language", ["en", "bn"], key="lang", horizontal=True,
        format_func=lambda x: {"en": "English", "bn": "বাংলা"}[x],
        label_visibility="collapsed",
    )
with ctrl_dark:
    _toggle(t("dark_label"), key="dark_mode")

# =====================================================================
# HEADER WITH INTEGRATED LOGO
# =====================================================================
logo_b64 = get_base64_image("logo_pjc copy.jpg")
logo_html = (
    f'<img class="portal-logo" src="data:image/jpeg;base64,{logo_b64}" alt="PJC Logo">'
    if logo_b64
    else '<div class="portal-logo-fallback">🏛️</div>'
)
st.markdown(f"""
<div class="portal-header">
{logo_html}
<div class="portal-header-text">
<h1>{t("site_name")}</h1>
<p>{t("site_tagline")}</p>
</div>
<div class="header-live"><span class="live-dot"></span>{t("live")}</div>
</div>
""", unsafe_allow_html=True)

notices = get_notices(load_announcements(), st.session_state.get("lang", "en"))
render_notices(notices)

# =====================================================================
# DATA & DELETION FILTERING
# =====================================================================
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
tab_browse, tab_saved, tab_upload, tab_admin = st.tabs([
    t("tab_browse"), t("tab_saved", n=saved_count), t("tab_upload"), t("tab_admin")
])

# =====================================================================
# TAB 1: BROWSE REPOSITORY
# =====================================================================
with tab_browse:
    head_l, head_r = st.columns([5, 1])
    with head_l:
        st.markdown(f"### {t('explore')}")
    with head_r:
        if st.button(t("refresh"), use_container_width=True, help=t("refresh_help")):
            load_uploaded_files.clear()
            load_announcements.clear()
            st.rerun()

    cat_col, dept_col, title_col, date_col = cols.get("cat"), cols.get("dept"), cols.get("title"), cols.get("date")

    if not df_files.empty:
        total_docs = len(df_files)
        syllabus_docs = int(df_files[cat_col].astype(str).str.contains("syllabus", case=False, na=False).sum()) if cat_col else 0
        study_docs = int(df_files[cat_col].astype(str).str.contains("study", case=False, na=False).sum()) if cat_col else 0
        assignment_docs = int(df_files[cat_col].astype(str).str.contains("assignment", case=False, na=False).sum()) if cat_col else 0
        dept_counts = {}
        if dept_col:
            for d in DEPARTMENT_FOLDERS:
                n = int(dept_mask(df_files[dept_col], d).sum())
                if n:
                    dept_counts[d] = n

        st.markdown(f"""
<div class="stat-grid">
<div class="stat-tile" style="--accent:#2563EB; animation-delay:0s;"><div class="stat-icon">📚</div><div><div class="stat-num">{total_docs}</div><div class="stat-label">{t("total_docs")}</div></div></div>
<div class="stat-tile" style="--accent:#F59E0B; animation-delay:0.08s;"><div class="stat-icon">📘</div><div><div class="stat-num">{syllabus_docs}</div><div class="stat-label">{t("syllabi")}</div></div></div>
<div class="stat-tile" style="--accent:#10B981; animation-delay:0.16s;"><div class="stat-icon">📝</div><div><div class="stat-num">{study_docs}</div><div class="stat-label">{t("study_materials")}</div></div></div>
<div class="stat-tile" style="--accent:#D97706; animation-delay:0.20s;"><div class="stat-icon">📋</div><div><div class="stat-num">{assignment_docs}</div><div class="stat-label">{t("assignments")}</div></div></div>
<div class="stat-tile" style="--accent:#7C3AED; animation-delay:0.24s;"><div class="stat-icon">🏫</div><div><div class="stat-num">{len(dept_counts)}</div><div class="stat-label">{t("depts_contrib")}</div></div></div>
</div>
""", unsafe_allow_html=True)

        if dept_counts:
            with st.expander(t("by_dept")):
                st.markdown(
                    bar_rows([(dept_label(d), n) for d, n in sorted(dept_counts.items(), key=lambda x: -x[1])]),
                    unsafe_allow_html=True,
                )

    # --- FILTERS ---
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.1, 1.4, 1.6, 1.1])
    with f_col1:
        selected_category = st.selectbox(
            t("category"), ["All", "Syllabus", "Study Material", "Assignment"],
            format_func=lambda x: {"All": t("all"), "Syllabus": t("syllabus"), "Study Material": t("study_material"), "Assignment": t("assignment")}[x],
        )
    with f_col2:
        selected_dept = st.selectbox(
            t("department"), ["All Departments"] + DEPARTMENT_FOLDERS,
            format_func=lambda x: t("all_depts") if x == "All Departments" else dept_label(x),
        )
    with f_col3:
        search_query = st.text_input(t("search"), placeholder=t("search_ph"))
    with f_col4:
        sort_choice = st.selectbox(t("sort_by"), ["newest", "oldest", "az"], format_func=lambda x: t(x))

    st.markdown("---")

    if not df_files.empty:
        filtered_df = df_files.copy()

        if selected_category != "All" and cat_col:
            filtered_df = filtered_df[filtered_df[cat_col].astype(str).str.contains(selected_category, case=False, na=False)]

        if selected_dept != "All Departments" and dept_col:
            filtered_df = filtered_df[dept_mask(filtered_df[dept_col], selected_dept)]

        if search_query.strip():
            hay = pd.Series("", index=filtered_df.index)
            for c in (title_col, dept_col, cat_col):
                if c:
                    hay = hay + " " + filtered_df[c].astype(str)
            filtered_df = filtered_df[hay.str.contains(search_query.strip(), case=False, na=False, regex=False)]

        parsed_dates = parse_dates(filtered_df[date_col]) if date_col else None
        if sort_choice == "az" and title_col:
            filtered_df = filtered_df.sort_values(title_col, key=lambda s: s.astype(str).str.lower())
        elif parsed_dates is not None and parsed_dates.notna().any():
            filtered_df = filtered_df.assign(_sort_dt=parsed_dates).sort_values(
                "_sort_dt", ascending=(sort_choice == "oldest"), na_position="last"
            )
        elif sort_choice == "newest":
            filtered_df = filtered_df.iloc[::-1]

        signature = (selected_category, selected_dept, search_query, sort_choice)
        if st.session_state.get("filter_signature") != signature:
            st.session_state["filter_signature"] = signature
            st.session_state["br_visible"] = PAGE_SIZE

        if not filtered_df.empty:
            render_cards(filtered_df, "br", cols, paginate=True)
        else:
            st.warning(t("no_match"))
    else:
        st.info(t("empty_repo"))

# =====================================================================
# TAB 2: MY SAVED
# =====================================================================
with tab_saved:
    st.markdown(f"### {t('saved_head')}")
    st.caption(t("saved_note"))
    if saved_count:
        order = {f: i for i, f in enumerate(reversed(st.session_state["saved"]))}
        saved_view = saved_present.assign(_ord=saved_present["_fid"].map(order)).sort_values("_ord")
        st.button(t("saved_clear"), key="saved_clear_btn", on_click=clear_saved)
        render_cards(saved_view, "sv", cols, paginate=False)
    else:
        st.info(t("saved_empty"))

# =====================================================================
# TAB 3: UPLOAD PORTAL (Restricted to Faculty with Password)
# =====================================================================
with tab_upload:
    st.markdown(f"### {t('upload_head')}")
    
    admin_pw = get_admin_password()
    if not admin_pw:
        st.info(t("admin_setup"))
    elif not st.session_state.get("faculty_logged_in"):
        st.markdown(f"""
        <div class="card-item">
        <h4>{t("faculty_login_head")}</h4>
        <p class="note-text">{t("faculty_login_sub")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("faculty_login_portal_form"):
            fac_pw = st.text_input(t("faculty_pw"), type="password")
            fac_submitted = st.form_submit_button(t("faculty_login_btn"))
        if fac_submitted:
            if hmac.compare_digest(fac_pw.encode(), admin_pw.encode()):
                st.session_state["faculty_logged_in"] = True
                st.rerun()
            else:
                st.error(t("faculty_wrong"))
    else:
        col_lg1, col_lg2 = st.columns([4, 1])
        with col_lg1:
            st.success(t("faculty_logged_in"))
        with col_lg2:
            if st.button(t("faculty_logout"), use_container_width=True):
                st.session_state["faculty_logged_in"] = False
                st.rerun()

        st.markdown(f"""
        <div class="card-item">
        <p class="note-text">{t("upload_intro")}</p>
        </div>
        <div class="upload-steps">
        <div class="step-card" style="animation-delay:0.05s;"><div class="step-no">1</div><h4>{t("step1_t")}</h4><p>{t("step1_d")}</p></div>
        <div class="step-card" style="animation-delay:0.15s;"><div class="step-no">2</div><h4>{t("step2_t")}</h4><p>{t("step2_d")}</p></div>
        <div class="step-card" style="animation-delay:0.25s;"><div class="step-no">3</div><h4>{t("step3_t")}</h4><p>{t("step3_d")}</p></div>
        </div>
        """, unsafe_allow_html=True)

        col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
        with col_b2:
            st.link_button(t("open_form"), FORM_DIRECT_URL, use_container_width=True)

# =====================================================================
# TAB 4: ADMIN
# =====================================================================
with tab_admin:
    render_admin(df_files, cols, len(notices))

# --- FOOTER ---
st.markdown(f"""
<div class="institutional-footer">
<p>{t("footer_rights")}</p>
<p>{t("footer_by")}</p>
<div class="visitor-counter">
<img src="https://visitor-badge.laobi.icu/badge?page_id=pjc_academic_repository_portal" alt="Visitor Counter">
</div>
</div>
""", unsafe_allow_html=True)

sync_query_params()
