import base64
import datetime
import getpass
import os
import platform
import random
import secrets
import socket
import sqlite3
import time

import geocoder
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from geopy.geocoders import Nominatim
from pdfminer.high_level import extract_text
from PIL import Image
from streamlit_tags import st_tags

from Courses import (
    android_course,
    ds_course,
    interview_videos,
    ios_course,
    resume_videos,
    uiux_course,
    web_course,
)
from resume_parser_local import ResumeParser


APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_DIR, "data")
UPLOAD_DIR = os.path.join(APP_DIR, "Uploaded_Resumes")
LOGO_ICON = os.path.join(APP_DIR, "Logo", "recommend.png")
LOGO_BANNER = os.path.join(APP_DIR, "Logo", "RESUM.png")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.chdir(APP_DIR)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon=LOGO_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

THEME = {
    "bg": "#F0F4FF",
    "surface": "rgba(255,255,255,0.82)",
    "surface_strong": "#ffffff",
    "surface_alt": "rgba(245, 248, 255, 0.92)",
    "border": "rgba(124, 58, 237, 0.14)",
    "border_strong": "rgba(124, 58, 237, 0.24)",
    "text": "#1A1A2E",
    "muted": "#9CA3AF",
    "primary": "#7C3AED",
    "primary_dark": "#5B21B6",
    "secondary": "#00D9FF",
    "accent": "#ff006e",
    "danger": "#ef4444",
    "shadow": "0 24px 80px rgba(26, 26, 46, 0.12)",
    "success": "#10b981",
}

FIELD_CATALOG = {
    "Data Science": {
        "keywords": {
            "tensorflow",
            "keras",
            "pytorch",
            "machine learning",
            "deep learning",
            "flask",
            "streamlit",
        },
        "skills": [
            "Data Visualization",
            "Predictive Analysis",
            "Statistical Modeling",
            "Data Mining",
            "Clustering",
            "ML Algorithms",
            "Scikit-learn",
            "TensorFlow",
            "PyTorch",
            "Probability",
            "Flask",
            "Streamlit",
        ],
        "courses": ds_course,
        "message": "Analysis says target role is Data Science.",
    },
    "Web Development": {
        "keywords": {
            "react",
            "django",
            "node js",
            "react js",
            "php",
            "laravel",
            "magento",
            "wordpress",
            "javascript",
            "angular js",
            "c#",
            "asp.net",
            "flask",
        },
        "skills": [
            "React",
            "TypeScript",
            "Django",
            "Node.js",
            "REST APIs",
            "Testing",
            "System Design",
            "Accessibility",
            "Performance",
            "Cloud Deployment",
        ],
        "courses": web_course,
        "message": "Analysis says target role is Web Development.",
    },
    "Android Development": {
        "keywords": {
            "android",
            "android development",
            "flutter",
            "kotlin",
            "xml",
            "kivy",
        },
        "skills": [
            "Android",
            "Kotlin",
            "Flutter",
            "Jetpack",
            "SDK",
            "Room DB",
            "SQLite",
            "Testing",
            "Play Store Ops",
        ],
        "courses": android_course,
        "message": "Analysis says target role is Android Development.",
    },
    "IOS Development": {
        "keywords": {
            "ios",
            "ios development",
            "swift",
            "cocoa",
            "cocoa touch",
            "xcode",
        },
        "skills": [
            "Swift",
            "SwiftUI",
            "UIKit",
            "Auto Layout",
            "StoreKit",
            "Core Data",
            "AV Foundation",
            "Testing",
        ],
        "courses": ios_course,
        "message": "Analysis says target role is IOS Development.",
    },
    "UI/UX Development": {
        "keywords": {
            "ux",
            "adobe xd",
            "figma",
            "zeplin",
            "balsamiq",
            "ui",
            "prototyping",
            "wireframes",
            "storyframes",
            "adobe photoshop",
            "photoshop",
            "editing",
            "adobe illustrator",
            "illustrator",
            "adobe after effects",
            "after effects",
            "adobe premier pro",
            "premier pro",
            "adobe indesign",
            "indesign",
            "wireframe",
            "solid",
            "grasp",
            "user research",
            "user experience",
        },
        "skills": [
            "Figma",
            "Design Systems",
            "Interaction Design",
            "Wireframing",
            "User Research",
            "Accessibility",
            "Prototyping",
            "Visual Hierarchy",
            "Design QA",
        ],
        "courses": uiux_course,
        "message": "Analysis says target role is UI/UX Development.",
    },
}

GENERALIST_KEYWORDS = {
    "english",
    "communication",
    "writing",
    "microsoft office",
    "leadership",
    "customer management",
    "social media",
}

SCORE_RULES = [
    ("Objective / Summary", ["objective", "summary", "profile"], 6, "Add a concise profile summary."),
    ("Education", ["education", "school", "college", "university"], 12, "Add clear education details."),
    ("Experience", ["experience", "work experience", "employment"], 16, "Show work experience or role-based impact."),
    ("Internships", ["internship", "internships", "trainee"], 6, "Internship work helps signal practical exposure."),
    ("Skills", ["skills", "tech stack", "competencies"], 7, "A dedicated skills section helps ATS parsing."),
    ("Hobbies", ["hobbies", "interests outside work"], 4, "Optional, but useful for personality signals."),
    ("Interests", ["interests", "areas of interest"], 5, "Add interests that support your role direction."),
    ("Achievements", ["achievements", "awards", "accomplishments"], 13, "Highlight measurable wins or awards."),
    ("Certifications", ["certifications", "certification", "certified"], 12, "Certifications increase trust."),
    ("Projects", ["projects", "project", "case study"], 19, "Projects are high-value proof of execution."),
]


def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


def pdf_reader(file):
    return extract_text(file) or ""


def show_pdf(file_path):
    with open(file_path, "rb") as file_obj:
        base64_pdf = base64.b64encode(file_obj.read()).decode("utf-8")
    pdf_display = f"""
        <div class="pdf-frame">
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="780" type="application/pdf"></iframe>
        </div>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


def normalize_skills(skills):
    if not skills:
        return []
    return [str(skill).strip() for skill in skills if str(skill).strip()]


def contains_any(text, terms):
    text = text.lower()
    return any(term in text for term in terms)


def infer_candidate_level(resume_text, no_of_pages):
    text = resume_text.lower()
    if no_of_pages < 1:
        return "NA", "Resume pages not detected."
    if any(term in text for term in ["work experience", "experience", "employment history"]):
        return "Experienced", "Resume shows direct experience history."
    if any(term in text for term in ["internship", "internships", "trainee"]):
        return "Intermediate", "Resume shows internship-level exposure."
    return "Fresher", "Resume looks more entry-level."


def infer_recommendation(skills):
    normalized = {skill.lower() for skill in skills}
    for field_name, meta in FIELD_CATALOG.items():
        if normalized & meta["keywords"]:
            return field_name, meta["skills"], meta["courses"], meta["message"]
    if normalized & GENERALIST_KEYWORDS:
        return "NA", ["No Recommendations"], [], "Current model supports DS, Web, Android, IOS, and UI/UX."
    return "General", ["Communication", "Projects", "Quantified Impact", "Role Keywords"], [], "No exact field match. Showing universal resume upgrades."


def build_resume_checks(resume_text):
    checks = []
    score = 0
    for title, terms, points, tip in SCORE_RULES:
        passed = contains_any(resume_text, terms)
        if passed:
            score += points
        checks.append(
            {
                "title": title,
                "passed": passed,
                "points": points,
                "tip": tip,
            }
        )
    return checks, score


def get_client_location():
    try:
        geodata = geocoder.ip("me")
        latlong = geodata.latlng or []
        if len(latlong) != 2:
            return "", "", "", ""
        geolocator = Nominatim(user_agent="ai-resume-analyzer")
        location = geolocator.reverse(latlong, language="en", timeout=5)
        address = location.raw.get("address", {}) if location else {}
        return latlong, address.get("city", ""), address.get("state", ""), address.get("country", "")
    except Exception:
        return "", "", "", ""


DB_KIND = os.getenv("RESUME_ANALYZER_DB", "sqlite").lower()
if DB_KIND == "mysql":
    import pymysql

    connection = pymysql.connect(
        host=os.getenv("RESUME_ANALYZER_MYSQL_HOST", "localhost"),
        user=os.getenv("RESUME_ANALYZER_MYSQL_USER", "root"),
        password=os.getenv("RESUME_ANALYZER_MYSQL_PASSWORD", ""),
        db=os.getenv("RESUME_ANALYZER_MYSQL_DB", "cv"),
    )
else:
    DB_KIND = "sqlite"
    connection = sqlite3.connect(os.path.join(DATA_DIR, "cv.sqlite3"), check_same_thread=False)
cursor = connection.cursor()


def db_placeholder():
    return "%s" if DB_KIND == "mysql" else "?"


def db_text(column):
    return f"convert({column} using utf8)" if DB_KIND == "mysql" else column


def init_database():
    if DB_KIND == "mysql":
        cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
        id_column = "ID INT NOT NULL AUTO_INCREMENT"
        primary_key = ", PRIMARY KEY (ID)"
    else:
        id_column = "ID INTEGER PRIMARY KEY AUTOINCREMENT"
        primary_key = ""

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS user_data
        ({id_column},
        sec_token varchar(20) NOT NULL,
        ip_add varchar(50) NULL,
        host_name varchar(50) NULL,
        dev_user varchar(50) NULL,
        os_name_ver varchar(50) NULL,
        latlong varchar(50) NULL,
        city varchar(50) NULL,
        state varchar(50) NULL,
        country varchar(50) NULL,
        act_name varchar(50) NOT NULL,
        act_mail varchar(50) NOT NULL,
        act_mob varchar(20) NOT NULL,
        Name varchar(500) NOT NULL,
        Email_ID VARCHAR(500) NOT NULL,
        resume_score VARCHAR(8) NOT NULL,
        Timestamp VARCHAR(50) NOT NULL,
        Page_no VARCHAR(5) NOT NULL,
        Predicted_Field BLOB NOT NULL,
        User_level BLOB NOT NULL,
        Actual_skills BLOB NOT NULL,
        Recommended_skills BLOB NOT NULL,
        Recommended_courses BLOB NOT NULL,
        pdf_name varchar(50) NOT NULL
        {primary_key}
        );
        """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS user_feedback
        ({id_column},
        feed_name varchar(50) NOT NULL,
        feed_email VARCHAR(50) NOT NULL,
        feed_score VARCHAR(5) NOT NULL,
        comments VARCHAR(100) NULL,
        Timestamp VARCHAR(50) NOT NULL
        {primary_key}
        );
        """
    )
    connection.commit()


def insert_data(
    sec_token,
    ip_add,
    host_name,
    dev_user,
    os_name_ver,
    latlong,
    city,
    state,
    country,
    act_name,
    act_mail,
    act_mob,
    name,
    email,
    res_score,
    timestamp,
    no_of_pages,
    reco_field,
    cand_level,
    skills,
    recommended_skills,
    courses,
    pdf_name,
):
    columns = """sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country,
        act_name, act_mail, act_mob, Name, Email_ID, resume_score, Timestamp, Page_no,
        Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses, pdf_name"""
    insert_sql = f"insert into user_data ({columns}) values ({','.join([db_placeholder()] * 23)})"
    rec_values = (
        str(sec_token),
        str(ip_add),
        host_name,
        dev_user,
        os_name_ver,
        str(latlong),
        city,
        state,
        country,
        act_name,
        act_mail,
        act_mob,
        name,
        email,
        str(res_score),
        timestamp,
        str(no_of_pages),
        reco_field,
        cand_level,
        skills,
        recommended_skills,
        courses,
        pdf_name,
    )
    cursor.execute(insert_sql, rec_values)
    connection.commit()


def insertf_data(feed_name, feed_email, feed_score, comments, timestamp):
    insertfeed_sql = f"""
        insert into user_feedback (feed_name, feed_email, feed_score, comments, Timestamp)
        values ({','.join([db_placeholder()] * 5)})
    """
    cursor.execute(insertfeed_sql, (feed_name, feed_email, feed_score, comments, timestamp))
    connection.commit()


def inject_theme():
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;700&display=swap');

            :root {{
                --primary: {THEME["primary"]};
                --primary-dark: {THEME["primary_dark"]};
                --secondary: {THEME["secondary"]};
                --accent: {THEME["accent"]};
                --success: {THEME["success"]};
                --danger: {THEME["danger"]};
                --text: {THEME["text"]};
                --text-secondary: {THEME["muted"]};
                --border: {THEME["border"]};
                --border-strong: {THEME["border_strong"]};
                --bg: {THEME["bg"]};
                --surface: {THEME["surface"]};
                --surface-strong: {THEME["surface_strong"]};
                --surface-alt: {THEME["surface_alt"]};
                --shadow: {THEME["shadow"]};
                --shadow-sm: 0 10px 30px rgba(26, 26, 46, 0.08);
                --shadow-md: 0 18px 48px rgba(26, 26, 46, 0.11);
                --shadow-lg: 0 28px 72px rgba(26, 26, 46, 0.16);
                --radius-xs: 12px;
                --radius-sm: 16px;
                --radius-md: 20px;
                --radius-lg: 28px;
                --space-1: 8px;
                --space-2: 16px;
                --space-3: 24px;
                --space-4: 32px;
                --space-5: 40px;
                --space-6: 48px;
            }}

            * {{ box-sizing: border-box; }}

            html, body, [class*="css"] {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}

            code, pre {{
                font-family: 'IBM Plex Mono', monospace;
            }}

            .stApp {{
                background:
                    radial-gradient(circle at top left, rgba(124, 58, 237, 0.16), transparent 28%),
                    radial-gradient(circle at top right, rgba(0, 217, 255, 0.18), transparent 24%),
                    linear-gradient(180deg, #f8fbff 0%, var(--bg) 42%, #eef4ff 100%);
                color: var(--text);
                overflow-x: hidden;
            }}

            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background:
                    linear-gradient(135deg, rgba(255,255,255,0.32), transparent 45%),
                    radial-gradient(circle at 20% 20%, rgba(255, 0, 110, 0.07), transparent 22%);
                pointer-events: none;
                z-index: 0;
            }}

            .block-container {{
                position: relative;
                z-index: 1;
                max-width: 1360px;
                padding: var(--space-5) var(--space-4) 5rem !important;
            }}

            [data-testid="stSidebar"] {{
                background:
                    linear-gradient(180deg, rgba(26, 26, 46, 0.98) 0%, rgba(38, 38, 68, 0.98) 100%),
                    radial-gradient(circle at top right, rgba(0, 217, 255, 0.18), transparent 30%);
                border-right: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 18px 0 44px rgba(26, 26, 46, 0.18);
            }}

            [data-testid="stSidebar"] * {{
                color: #eef2ff !important;
            }}

            [data-testid="stSidebar"] label {{
                color: #eef2ff !important;
            }}

            div[data-testid="stForm"],
            div[data-testid="stVerticalBlockBorderWrapper"],
            .modern-card,
            .glass-effect {{
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: var(--radius-md);
                box-shadow: var(--shadow-sm);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
                transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            }}

            div[data-testid="stVerticalBlockBorderWrapper"] {{
                padding: var(--space-3) !important;
                margin-bottom: var(--space-3);
                background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(248,250,255,0.88));
            }}

            div[data-testid="stVerticalBlockBorderWrapper"]:hover,
            .modern-card:hover,
            .metric-card:hover,
            .course-card:hover {{
                transform: translateY(-4px);
                box-shadow: var(--shadow-md);
                border-color: var(--border-strong);
            }}

            .hero-section {{
                background:
                    linear-gradient(135deg, rgba(124, 58, 237, 0.16) 0%, rgba(0, 217, 255, 0.12) 52%, rgba(255, 0, 110, 0.10) 100%),
                    linear-gradient(180deg, rgba(255,255,255,0.78), rgba(255,255,255,0.56));
                border: 1px solid rgba(255, 255, 255, 0.7);
                border-radius: var(--radius-lg);
                padding: clamp(2rem, 4vw, 3.75rem);
                margin-bottom: var(--space-4);
                position: relative;
                overflow: hidden;
                box-shadow: var(--shadow-md);
            }}

            .hero-section::before {{
                content: '';
                position: absolute;
                top: -20%;
                right: -6%;
                width: 320px;
                height: 320px;
                background: radial-gradient(circle, rgba(124, 58, 237, 0.26), transparent 68%);
                border-radius: 50%;
                pointer-events: none;
                filter: blur(8px);
            }}

            .hero-section::after {{
                content: '';
                position: absolute;
                bottom: -22%;
                left: -6%;
                width: 280px;
                height: 280px;
                background: radial-gradient(circle, rgba(0, 217, 255, 0.24), transparent 72%);
                border-radius: 50%;
                pointer-events: none;
                filter: blur(10px);
            }}

            .hero-badge {{
                display: inline-flex;
                align-items: center;
                gap: 0.625rem;
                padding: 0.75rem 1.25rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.64);
                color: var(--primary);
                font-weight: 700;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                margin-bottom: var(--space-2);
                border: 1px solid rgba(124, 58, 237, 0.14);
                box-shadow: 0 10px 24px rgba(124, 58, 237, 0.08);
            }}

            .hero-title {{
                font-size: clamp(2.4rem, 5vw, 4.4rem);
                font-weight: 800;
                line-height: 1.02;
                color: var(--text);
                margin: 0 0 1rem 0;
                letter-spacing: -0.045em;
                max-width: 10ch;
            }}

            .hero-subtitle {{
                font-size: 1.05rem;
                line-height: 1.85;
                color: rgba(26, 26, 46, 0.78);
                max-width: 60ch;
                margin: 0;
            }}

            .section-header {{
                display: block;
                padding: 0.25rem 0 1rem;
                margin-bottom: 1rem;
            }}

            .section-title {{
                font-size: 1.35rem;
                font-weight: 800;
                color: var(--text);
                margin: 0;
                display: inline-flex;
                align-items: center;
                gap: 0.8rem;
                line-height: 1.15;
            }}

            .section-title::before {{
                content: '';
                width: 10px;
                height: 10px;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                border-radius: 999px;
                box-shadow: 0 0 0 6px rgba(124, 58, 237, 0.08);
            }}

            .section-copy {{
                font-size: 0.95rem;
                color: rgba(26, 26, 46, 0.68);
                margin-top: 0.5rem;
                max-width: 58ch;
                line-height: 1.7;
            }}

            .section-panel {{
                background: rgba(255,255,255,0.94);
                border: 1px solid rgba(124, 58, 237, 0.12);
                border-radius: var(--radius-lg);
                padding: 1.3rem;
                margin-bottom: var(--space-4);
                box-shadow: var(--shadow-sm);
            }}

            .metric-card {{
                background:
                    linear-gradient(180deg, rgba(255,255,255,0.94), rgba(246,248,255,0.9)),
                    linear-gradient(135deg, rgba(124, 58, 237, 0.06), rgba(0, 217, 255, 0.03));
                border: 1px solid var(--border);
                border-radius: var(--radius-md);
                padding: var(--space-3);
                min-height: 156px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                position: relative;
                overflow: hidden;
                box-shadow: var(--shadow-sm);
            }}

            .metric-card::before {{
                content: '';
                position: absolute;
                inset: auto -14px -14px auto;
                width: 132px;
                height: 132px;
                background: radial-gradient(circle, rgba(124, 58, 237, 0.12), transparent 68%);
                border-radius: 50%;
                pointer-events: none;
            }}

            .metric-label {{
                font-size: 0.78rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: rgba(26, 26, 46, 0.52);
                margin-bottom: 0.85rem;
            }}

            .metric-value {{
                font-size: clamp(1.8rem, 3.4vw, 2.6rem);
                font-weight: 800;
                color: var(--primary);
                line-height: 1.05;
                margin: 0.35rem 0 0.6rem;
                letter-spacing: -0.04em;
                word-break: break-word;
            }}

            .metric-description {{
                font-size: 0.92rem;
                color: rgba(26, 26, 46, 0.72);
                margin-top: auto;
                line-height: 1.65;
            }}

            .skill-pill {{
                display: inline-block;
                padding: 0.7rem 1rem;
                border-radius: 999px;
                margin: 0.35rem 0.45rem 0.35rem 0;
                font-size: 0.88rem;
                font-weight: 600;
                border: 1px solid;
                transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
            }}

            .skill-pill-primary {{
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(124, 58, 237, 0.04));
                color: var(--primary);
                border-color: rgba(124, 58, 237, 0.2);
            }}

            .skill-pill-primary:hover {{
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.18), rgba(255, 0, 110, 0.08));
                border-color: var(--primary);
                transform: translateY(-2px);
            }}

            .skill-pill-secondary {{
                background: linear-gradient(135deg, rgba(0, 217, 255, 0.16), rgba(0, 217, 255, 0.05));
                color: var(--secondary);
                border-color: rgba(0, 217, 255, 0.24);
            }}

            .skill-pill-secondary:hover {{
                background: linear-gradient(135deg, rgba(0, 217, 255, 0.22), rgba(124, 58, 237, 0.08));
                border-color: var(--secondary);
                transform: translateY(-2px);
            }}

            .status-item {{
                display: flex;
                align-items: flex-start;
                gap: var(--space-2);
                padding: 1.15rem 0;
                border-bottom: 1px solid rgba(124, 58, 237, 0.08);
            }}

            .status-item:last-child {{
                border-bottom: none;
                padding-bottom: 0;
            }}

            .status-icon {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                flex-shrink: 0;
                font-size: 1.1rem;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
            }}

            .status-icon.success {{
                background: rgba(16, 185, 129, 0.16);
                color: var(--success);
            }}

            .status-icon.danger {{
                background: rgba(239, 68, 68, 0.12);
                color: var(--danger);
            }}

            .status-content {{
                flex: 1;
            }}

            .status-title {{
                font-weight: 700;
                color: var(--text);
                font-size: 1rem;
                line-height: 1.4;
            }}

            .status-description {{
                font-size: 0.92rem;
                color: rgba(26, 26, 46, 0.72);
                margin-top: 0.35rem;
                line-height: 1.65;
            }}

            .status-badge {{
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: rgba(26, 26, 46, 0.48);
            }}

            .stTextInput input, 
            .stTextArea textarea, 
            .stSelectbox select,
            .stNumberInput input {{
                border-radius: var(--radius-xs) !important;
                border: 1.5px solid var(--border) !important;
                background: rgba(255,255,255,0.92) !important;
                color: var(--text) !important;
                font-size: 0.95rem !important;
                padding: 0.9rem 1rem !important;
                min-height: 48px !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
            }}

            .stTextInput input:focus, 
            .stTextArea textarea:focus,
            .stNumberInput input:focus {{
                border-color: var(--primary) !important;
                box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.12) !important;
            }}

            .stTextInput label,
            .stTextArea label,
            .stSelectbox label,
            .stNumberInput label {{
                font-weight: 700;
                color: var(--text) !important;
                font-size: 0.92rem !important;
                margin-bottom: 0.6rem !important;
            }}

            div[data-baseweb="input"] > div,
            div[data-baseweb="base-input"] > div,
            textarea,
            div[data-testid="stFileUploaderDropzone"] {{
                border-radius: var(--radius-xs) !important;
                border: 1.5px solid var(--border) !important;
                background: rgba(255,255,255,0.92) !important;
            }}

            div[data-testid="stFileUploaderDropzone"] {{
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.05), rgba(0, 217, 255, 0.07)) !important;
                border: 2px dashed rgba(124, 58, 237, 0.3) !important;
                padding: 1.2rem !important;
            }}

            div[data-testid="stFileUploaderDropzone"] * {{
                color: var(--text) !important;
            }}

            div[data-testid="stFileUploaderDropzone"] small {{
                color: var(--text-secondary) !important;
            }}

            .stButton > button, 
            .stDownloadButton > button {{
                border-radius: 14px;
                border: none;
                background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
                color: white !important;
                font-weight: 700;
                font-size: 0.96rem;
                min-height: 48px;
                padding: 0.85rem 1.1rem;
                box-shadow: 0 12px 28px rgba(124, 58, 237, 0.26);
                transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease;
                text-transform: none;
                letter-spacing: 0.01em;
            }}

            .stButton > button:hover, 
            .stDownloadButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 18px 34px rgba(124, 58, 237, 0.32);
                filter: saturate(1.08);
            }}

            .stButton > button:active {{
                transform: translateY(0);
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.75rem;
                margin-bottom: var(--space-3);
                border-bottom: 1px solid rgba(124, 58, 237, 0.12);
                padding-bottom: 1rem;
                flex-wrap: wrap;
            }}

            .stTabs [data-baseweb="tab"] {{
                background: rgba(255,255,255,0.66);
                border-radius: 999px;
                padding: 0.8rem 1.25rem;
                border: none;
                color: rgba(26, 26, 46, 0.56);
                font-weight: 700;
                transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
                border: 1px solid rgba(124, 58, 237, 0.08);
            }}

            .stTabs [data-baseweb="tab"]:hover {{
                color: var(--primary);
                background: rgba(124, 58, 237, 0.08);
                transform: translateY(-1px);
            }}

            .stTabs [aria-selected="true"] {{
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(0, 217, 255, 0.12)) !important;
                color: var(--primary) !important;
                border: 1px solid rgba(124, 58, 237, 0.18) !important;
                box-shadow: 0 10px 24px rgba(124, 58, 237, 0.1);
            }}

            div[data-testid="stAlert"] {{
                border-radius: var(--radius-xs);
                border: 1.5px solid !important;
                padding: 1rem 1.15rem !important;
                box-shadow: var(--shadow-sm);
            }}

            div[data-testid="stDataFrame"] {{
                border-radius: var(--radius-sm);
                overflow: hidden;
                border: 1.5px solid var(--border) !important;
                background: rgba(255,255,255,0.92) !important;
                box-shadow: var(--shadow-sm);
            }}

            .sidebar-header {{
                padding: 1.5rem 0 1.75rem;
                margin-bottom: 1.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}

            .sidebar-title {{
                font-size: 1.4rem;
                font-weight: 800;
                color: white;
                margin: 0.5rem 0 0 0;
                letter-spacing: -0.03em;
            }}

            .sidebar-subtitle {{
                font-size: 0.875rem;
                color: rgba(255, 255, 255, 0.68);
                margin-top: 0.5rem;
                line-height: 1.7;
            }}

            [data-testid="stSidebar"] label[data-baseweb="radio"] {{
                background: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 14px;
                padding: 0.85rem 1rem;
                margin-bottom: 0.75rem;
                transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
                color: #eef2ff !important;
            }}

            [data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] {{
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.28), rgba(0, 217, 255, 0.18));
                border-color: rgba(255,255,255,0.16);
                color: white !important;
                transform: translateX(2px);
            }}

            .stPlotlyChart {{
                background: var(--surface);
                border-radius: var(--radius-sm);
                padding: 1rem;
                margin-bottom: 1rem;
                border: 1px solid rgba(124, 58, 237, 0.08);
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: var(--text);
                font-weight: 800;
                letter-spacing: -0.03em;
            }}

            p, span, div {{
                color: var(--text);
            }}

            caption, label, .stCaption {{
                color: var(--text-secondary) !important;
            }}

            .modern-card {{
                padding: var(--space-3);
                margin-bottom: var(--space-3);
            }}

            .gradient-text {{
                background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .course-card {{
                display: block;
                padding: 1.05rem 1.25rem;
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.08), rgba(0, 217, 255, 0.08));
                border: 1px solid rgba(124, 58, 237, 0.14);
                border-radius: var(--radius-sm);
                color: var(--text);
                text-decoration: none;
                font-weight: 600;
                transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
                box-shadow: var(--shadow-sm);
            }}

            .course-card:hover {{
                border-color: rgba(124, 58, 237, 0.28);
                box-shadow: var(--shadow-md);
                transform: translateY(-3px);
            }}

            .info-banner {{
                padding: 1rem 1.2rem;
                border-radius: var(--radius-sm);
                border: 1px dashed rgba(124, 58, 237, 0.22);
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.06), rgba(0, 217, 255, 0.08));
                color: rgba(26, 26, 46, 0.76);
                line-height: 1.7;
            }}

            .soft-panel {{
                padding: 1rem;
                border-radius: var(--radius-sm);
                border: 1px solid rgba(124, 58, 237, 0.12);
                background: linear-gradient(180deg, rgba(255,255,255,0.84), rgba(246,248,255,0.86));
                box-shadow: var(--shadow-sm);
            }}

            .feature-list-item {{
                display: flex;
                align-items: flex-start;
                gap: 0.9rem;
                margin-bottom: 1rem;
            }}

            .feature-icon {{
                width: 36px;
                height: 36px;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 800;
                font-size: 0.8rem;
                flex-shrink: 0;
                box-shadow: 0 10px 18px rgba(124, 58, 237, 0.18);
            }}

            .spacing-sm {{ margin: 0.5rem; }}
            .spacing-md {{ margin: 1rem; }}
            .spacing-lg {{ margin: 1.5rem; }}
            .spacing-xl {{ margin: 2rem; }}

            .mb-2 {{ margin-bottom: 1rem; }}
            .mb-3 {{ margin-bottom: 1.5rem; }}
            .mb-4 {{ margin-bottom: 2rem; }}

            .text-muted {{
                color: var(--text-secondary);
            }}

            .text-primary {{
                color: var(--primary);
            }}

            .text-success {{
                color: var(--success);
            }}

            .text-danger {{
                color: var(--danger);
            }}

            @media (max-width: 991px) {{
                .block-container {{
                    padding: var(--space-4) var(--space-3) 4rem !important;
                }}

                .hero-title {{
                    max-width: none;
                }}
            }}

            @media (max-width: 640px) {{
                .block-container {{
                    padding: var(--space-3) var(--space-2) 3rem !important;
                }}

                div[data-testid="stVerticalBlockBorderWrapper"],
                .modern-card,
                .metric-card {{
                    padding: var(--space-2) !important;
                }}

                .hero-section {{
                    padding: 1.5rem;
                    border-radius: 22px;
                }}

                .hero-title {{
                    font-size: 2.2rem;
                }}

                .status-item {{
                    gap: 0.75rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.markdown(
        """
        <div class="sidebar-header">
            <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5);">AI Resume Analyzer</div>
            <div class="sidebar-title">📊 Talent OS</div>
            <div class="sidebar-subtitle">Modern resume analysis and skill mapping</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if "nav" not in st.session_state:
        st.session_state["nav"] = "User"

    if st.sidebar.button("🔐 Admin Login", use_container_width=True):
        st.session_state["nav"] = "Admin"

    nav = st.sidebar.radio(
        "Navigate",
        ["User", "Feedback", "About", "Admin"],
        index=["User", "Feedback", "About", "Admin"].index(st.session_state["nav"]),
        label_visibility="collapsed",
    )
    st.session_state["nav"] = nav
    return nav


def render_admin_entry():
    left, right = st.columns([5, 1])
    with left:
        st.caption("Admin access")
    with right:
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state["nav"] = "Admin"
            if hasattr(st, "rerun"):
                st.rerun()
            else:
                st.experimental_rerun()


def render_metric_card(label, value, description):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title, copy=None):
    html = f'<div class="section-header"><div class="section-title">{title}</div>'
    if copy:
        html += f'<div class="section-copy">{copy}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_hero():
    st.markdown(
        """
        <div class="hero-section">
            <span class="hero-badge">✨ AI-Powered Resume Intelligence</span>
            <div class="hero-title">Upload. Analyze. Improve.</div>
            <div class="hero-subtitle">
                Get instant insights on resume quality, skill alignment, role prediction, and personalized learning recommendations to accelerate your career.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    cols = st.columns(3, gap="medium")
    with cols[0]:
        render_metric_card("Analysis", "98%", "Accuracy on resume parsing")
    with cols[1]:
        render_metric_card("Speed", "1.2s", "Average processing time")
    with cols[2]:
        render_metric_card("Database", "15k+", "Candidate profiles analyzed")


def render_skill_chips(title, chips, variant):
    pill_class = "skill-pill-primary" if variant == "primary" else "skill-pill-secondary"
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if not chips:
        st.markdown('<div class="soft-panel" style="text-align: center; color: var(--text-secondary);">No data available</div>', unsafe_allow_html=True)
        return
    html = "".join([f'<span class="skill-pill {pill_class}">{chip}</span>' for chip in chips])
    st.markdown(f'<div class="section-panel">{html}</div>', unsafe_allow_html=True)


def build_score_gauge(score):
    bar_color = THEME["secondary"] if score >= 70 else THEME["accent"] if score >= 45 else THEME["danger"]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "/100", "font": {"size": 34, "color": THEME["text"]}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 0},
                "bar": {"color": bar_color, "thickness": 0.34},
                "bgcolor": "rgba(46,91,255,0.08)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(221,90,115,0.16)"},
                    {"range": [40, 70], "color": "rgba(255,181,61,0.16)"},
                    {"range": [70, 100], "color": "rgba(10,168,143,0.16)"},
                ],
            },
        )
    )
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def render_checklist(checks):
    st.markdown('<div class="section-title">Resume Quality Checklist</div>', unsafe_allow_html=True)
    rows = []
    for check in checks:
        status_class = "success" if check["passed"] else "danger"
        symbol = "✓" if check["passed"] else "⚠"
        action = f"+{check['points']} pts" if check["passed"] else check["tip"]
        rows.append(
            f'<div class="status-item"><div class="status-icon {status_class}">{symbol}</div><div class="status-content"><div class="status-title">{check["title"]}</div><div class="status-description">{action}</div></div><div class="status-badge">{"✓ Present" if check["passed"] else "✕ Missing"}</div></div>'
        )
    st.markdown(f'<div class="section-panel">{"".join(rows)}</div>', unsafe_allow_html=True)


def render_courses(courses, selected_courses=None):
    st.markdown('<div class="section-title">🎓 Recommended Learning Tracks</div>', unsafe_allow_html=True)
    if not courses:
        st.markdown(
            '<div class="soft-panel" style="text-align: center; color: var(--text-secondary);">📚 No field-specific courses found. Enhance your role keywords to get recommendations.</div>',
            unsafe_allow_html=True,
        )
        return []
    picks = selected_courses or courses
    max_count = st.slider("Show courses", 1, min(10, len(picks)), min(5, len(picks)), label_visibility="collapsed")
    
    names = []
    course_html = []
    for name, link in picks[:max_count]:
        names.append(name)
        course_html.append(
            f'<a href="{link}" target="_blank" class="course-card"><div style="display: flex; align-items: center; justify-content: space-between; gap: 0.75rem;"><div style="display: flex; align-items: center; gap: 0.75rem;"><span style="font-size: 1.25rem;">📖</span><span>{name}</span></div><span style="color: var(--secondary); font-size: 1.25rem;">↗</span></div></a>'
        )
    
    st.markdown(
        '<div class="section-panel" style="display: grid; grid-template-columns: 1fr; gap: 0.75rem;">%s</div>' % ''.join(course_html),
        unsafe_allow_html=True,
    )
    return names


def analyze_resume(act_name, act_mail, act_mob, pdf_file):
    sec_token = secrets.token_urlsafe(12)
    host_name = socket.gethostname()
    ip_add = socket.gethostbyname(host_name)
    dev_user = getpass.getuser()
    os_name_ver = platform.system() + " " + platform.release()
    latlong, city, state, country = get_client_location()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    save_image_path = os.path.join(UPLOAD_DIR, pdf_file.name)
    with open(save_image_path, "wb") as file_obj:
        file_obj.write(pdf_file.getbuffer())

    resume_data = ResumeParser(save_image_path).get_extracted_data()
    if not resume_data:
        return None

    resume_text = pdf_reader(save_image_path)
    parsed_name = resume_data.get("name") or act_name or "Candidate"
    parsed_email = resume_data.get("email") or act_mail or "Not detected"
    parsed_mobile = resume_data.get("mobile_number") or act_mob or "Not detected"
    parsed_degree = resume_data.get("degree") or []
    no_of_pages = int(resume_data.get("no_of_pages") or 0)
    skills = normalize_skills(resume_data.get("skills"))
    cand_level, level_note = infer_candidate_level(resume_text, no_of_pages)
    reco_field, recommended_skills, course_pool, field_message = infer_recommendation(skills)
    checks, resume_score = build_resume_checks(resume_text)
    preselected_courses = random.sample(course_pool, k=min(5, len(course_pool))) if course_pool else []

    result = {
        "sec_token": sec_token,
        "ip_add": ip_add,
        "host_name": host_name,
        "dev_user": dev_user,
        "os_name_ver": os_name_ver,
        "latlong": latlong,
        "city": city,
        "state": state,
        "country": country,
        "act_name": act_name,
        "act_mail": act_mail,
        "act_mob": act_mob,
        "name": parsed_name,
        "email": parsed_email,
        "mobile": parsed_mobile,
        "degree": parsed_degree,
        "pages": no_of_pages,
        "skills": skills,
        "resume_score": resume_score,
        "candidate_level": cand_level,
        "level_note": level_note,
        "predicted_field": reco_field,
        "field_message": field_message,
        "recommended_skills": recommended_skills,
        "course_pool": course_pool,
        "selected_courses": preselected_courses,
        "checks": checks,
        "resume_text": resume_text,
        "timestamp": timestamp,
        "pdf_path": save_image_path,
        "pdf_name": pdf_file.name,
    }
    return result


def render_user_page():
    render_hero()
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    
    left_col, right_col = st.columns([1.3, 0.7], gap="large")

    with left_col:
        with st.container(border=True):
            render_section_header("Upload Your Resume", "Fill in your details and upload your PDF to get started")
            
            st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
            
            form_cols = st.columns(3, gap="medium")
            with form_cols[0]:
                act_name = st.text_input("Name", placeholder="Your full name")
            with form_cols[1]:
                act_mail = st.text_input("Email", placeholder="your@email.com")
            with form_cols[2]:
                act_mob = st.text_input("Phone", placeholder="+91 XXXXX XXXXX")
            
            st.markdown('<div style="margin-top: 1.5rem; margin-bottom: 1rem;"><strong>Resume Document</strong></div>', unsafe_allow_html=True)
            pdf_file = st.file_uploader("Select PDF", type=["pdf"], label_visibility="collapsed")
            
            st.markdown(
                '<div class="info-banner" style="margin-top: 1rem; font-size: 0.9rem;">📄 Supported: PDF files up to 10MB. Text-based resumes recommended for better extraction.</div>',
                unsafe_allow_html=True,
            )
            
            st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
            analyze = st.button("🚀 Analyze Resume", use_container_width=True)

    with right_col:
        with st.container(border=True):
            render_section_header("What You'll Get", "")
            
            items = [
                ("Score", "Quality rating (0-100)"),
                ("Field", "Career direction prediction"),
                ("Skills", "Detected & recommended"),
                ("Gaps", "Areas to improve"),
                ("Courses", "Learning suggestions"),
            ]
            
            for icon_label, desc in items:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem;">
                        <div style="width: 32px; height: 32px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.75rem; flex-shrink: 0;">{icon_label[:1]}</div>
                        <div>
                            <div style="font-weight: 600; color: var(--text);">{icon_label}</div>
                            <div style="font-size: 0.875rem; color: var(--text-secondary);">{desc}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if analyze:
        if not all([act_name.strip(), act_mail.strip(), act_mob.strip(), pdf_file]):
            st.error("⚠️ Please fill in all fields and upload a resume.")
        else:
            with st.spinner("📊 Analyzing resume..."):
                time.sleep(1.2)
                result = analyze_resume(act_name, act_mail, act_mob, pdf_file)
            if not result:
                st.error("❌ Failed to parse resume. Please try again.")
            else:
                st.session_state["analysis_result"] = result
                st.session_state["course_names"] = []
                course_names = [name for name, _ in result.get("selected_courses", [])]
                insert_data(
                    result["sec_token"],
                    result["ip_add"],
                    result["host_name"],
                    result["dev_user"],
                    result["os_name_ver"],
                    result["latlong"],
                    result["city"],
                    result["state"],
                    result["country"],
                    result["act_name"],
                    result["act_mail"],
                    result["act_mob"],
                    result["name"],
                    result["email"],
                    result["resume_score"],
                    result["timestamp"],
                    result["pages"],
                    result["predicted_field"],
                    result["candidate_level"],
                    str(result["skills"]),
                    str(result["recommended_skills"]),
                    str(course_names),
                    result["pdf_name"],
                )

    result = st.session_state.get("analysis_result")
    if not result:
        return

    st.markdown(
        f"""
        <div class="soft-panel" style="margin-top: 3rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.14), rgba(124, 58, 237, 0.08)); border-color: rgba(16, 185, 129, 0.16);">
            <div style="font-size: 1rem; font-weight: 700; color: var(--success);">✓ Analysis Complete</div>
            <div style="font-size: 0.95rem; color: var(--text-secondary); margin-top: 0.35rem;">Profile for <strong>{result['name']}</strong> has been extracted and analyzed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown('<div style="margin-top: 2rem; margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    
    kpi_cols = st.columns(4, gap="medium")
    with kpi_cols[0]:
        render_metric_card("Candidate", result["name"], f"{result['email']}")
    with kpi_cols[1]:
        render_metric_card("Predicted Role", result["predicted_field"], result["field_message"])
    with kpi_cols[2]:
        render_metric_card("Experience", result["candidate_level"], result["level_note"])
    with kpi_cols[3]:
        render_metric_card("Score", f"{result['resume_score']}/100", f"{result['pages']} page(s)")

    st.markdown('<div style="margin-top: 2.5rem; margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

    tab_overview, tab_skills, tab_health, tab_pdf = st.tabs(
        ["📋 Overview", "⚡ Skills", "✓ Quality Check", "📄 PDF"]
    )

    with tab_overview:
        col_a, col_b = st.columns([1, 1.2], gap="large")
        with col_a:
            st.plotly_chart(build_score_gauge(result["resume_score"]), use_container_width=True)
            with st.container(border=True):
                render_section_header("Profile Summary")
                st.markdown(
                    f"""
                    <div style="line-height: 2.2; font-size: 0.95rem;">
                        <div><strong>👤 Name:</strong> {result['name']}</div>
                        <div><strong>📧 Email:</strong> {result['email']}</div>
                        <div><strong>📱 Phone:</strong> {result['mobile']}</div>
                        <div><strong>🎓 Degree:</strong> {result['degree'] or 'Not detected'}</div>
                        <div><strong>📍 Location:</strong> {result['city']}, {result['state']}, {result['country']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with col_b:
            render_checklist(result["checks"])

    with tab_skills:
        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            render_skill_chips("Current Skills", result["skills"], "primary")
            st_tags(
                label="",
                text="Detected from your resume",
                value=result["skills"],
                key="current-skills",
            )
        with col_b:
            render_skill_chips("Recommended Skills", result["recommended_skills"], "secondary")
            st_tags(
                label="",
                text="Skills to strengthen your profile",
                value=result["recommended_skills"],
                key="recommended-skills",
            )
        with st.container(border=True):
            course_names = render_courses(result["course_pool"], result.get("selected_courses"))
            st.session_state["course_names"] = course_names

        video_a, video_b = st.columns(2)
        with video_a:
            st.markdown('<div class="section-title">Resume tip video</div>', unsafe_allow_html=True)
            st.video(random.choice(resume_videos))
        with video_b:
            st.markdown('<div class="section-title">Interview tip video</div>', unsafe_allow_html=True)
            st.video(random.choice(interview_videos))

    with tab_health:
        passed = sum(1 for item in result["checks"] if item["passed"])
        failed = len(result["checks"]) - passed
        chart = px.bar(
            pd.DataFrame(
                [
                    {"State": "Present", "Count": passed},
                    {"State": "Missing", "Count": failed},
                ]
            ),
            x="State",
            y="Count",
            color="State",
            color_discrete_map={"Present": THEME["secondary"], "Missing": THEME["danger"]},
        )
        chart.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            height=320,
        )
        st.plotly_chart(chart, use_container_width=True)
        render_checklist(result["checks"])

    with tab_pdf:
        show_pdf(result["pdf_path"])


def render_feedback_page():
    st.markdown(
        """
        <div class="hero-section">
            <span class="hero-badge">✨ Feedback Loop</span>
            <div class="hero-title">Help Us Improve</div>
            <div class="hero-subtitle">Your feedback shapes the next version of AI Resume Analyzer</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    form_col, chart_col = st.columns([1, 1.2], gap="large")
    with form_col:
        with st.form("feedback_form"):
            with st.container(border=True):
                render_section_header("Share Your Experience", "")
                st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
                
                feed_name = st.text_input("Full Name", placeholder="Your name", label_visibility="collapsed")
                feed_email = st.text_input("Email Address", placeholder="name@example.com", label_visibility="collapsed")
                feed_score = st.slider("Rate your experience", 1, 5, 4, label_visibility="collapsed")
                comments = st.text_area("Your feedback", placeholder="What should we improve? What worked great?", height=120, label_visibility="collapsed")
                
                st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
                submitted = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
                if submitted:
                    insertf_data(feed_name, feed_email, feed_score, comments, ts)
                    st.success("✓ Thank you! Feedback recorded successfully.")

    with chart_col:
        plotfeed_data = pd.read_sql("select * from user_feedback", connection)
        with st.container(border=True):
            render_section_header("Rating Distribution", "")
            if plotfeed_data.empty:
                st.markdown(
                    '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">No feedback yet. Be the first to share your thoughts!</div>',
                    unsafe_allow_html=True,
                )
            else:
                labels = plotfeed_data.feed_score.astype(str)
                values = labels.value_counts().sort_index()
                fig = px.pie(
                    values=values.values,
                    names=values.index,
                    hole=0.55,
                    color=values.index,
                    color_discrete_sequence=[THEME["primary"], THEME["secondary"], THEME["accent"], THEME["success"], THEME["danger"]],
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=360,
                    showlegend=True,
                    font=dict(color=THEME["text"]),
                )
                st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)

    cursor.execute("select feed_name, comments, feed_score, Timestamp from user_feedback order by ID desc")
    comments_data = cursor.fetchall()
    with st.container(border=True):
        render_section_header("Recent Feedback", "")
        if comments_data:
            df = pd.DataFrame(comments_data, columns=["Name", "Comment", "Rating", "Timestamp"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown(
                '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">No feedback submitted yet.</div>',
                unsafe_allow_html=True,
            )


def render_about_page():
    st.markdown(
        """
        <div class="hero-section">
            <span class="hero-badge">✨ About the Analyzer</span>
            <div class="hero-title">Resume Intelligence Platform</div>
            <div class="hero-subtitle">AI-powered analysis that extracts insights, predicts career paths, and recommends growth opportunities</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        with st.container(border=True):
            render_section_header("How It Works", "")
            
            flows = [
                ("1", "Upload", "Submit your PDF resume"),
                ("2", "Parse", "Extract skills, experience, education"),
                ("3", "Analyze", "Score quality, predict role direction"),
                ("4", "Recommend", "Suggest skills and courses to improve"),
            ]
            
            for num, title, desc in flows:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.25rem;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, var(--primary), var(--secondary)); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; flex-shrink: 0;">{num}</div>
                        <div>
                            <div style="font-weight: 600; color: var(--text); font-size: 1rem;">{title}</div>
                            <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem;">{desc}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    
    with col_b:
        with st.container(border=True):
            render_section_header("Key Features", "")
            
            features = [
                ("🎯", "Skill Detection", "Identifies technical and soft skills from your resume"),
                ("📈", "Quality Score", "Comprehensive resume quality assessment (0-100)"),
                ("🎓", "Recommendations", "Personalized skill and course suggestions"),
                ("📊", "Analytics", "Track your profile and improvement over time"),
            ]
            
            for icon, title, desc in features:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1.25rem;">
                        <div style="font-size: 1.5rem; flex-shrink: 0;">{icon}</div>
                        <div>
                            <div style="font-weight: 600; color: var(--text); font-size: 1rem;">{title}</div>
                            <div style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem;">{desc}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    
    st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        render_section_header("Technology Stack", "")
        
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
                <div class="soft-panel" style="border-left: 3px solid var(--primary);">
                    <div style="font-weight: 600; color: var(--primary); margin-bottom: 0.5rem;">AI & NLP</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary);">Advanced parsing and entity extraction</div>
                </div>
                <div class="soft-panel" style="border-left: 3px solid var(--secondary);">
                    <div style="font-weight: 600; color: var(--secondary); margin-bottom: 0.5rem;">Database</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary);">SQLite with secure data storage</div>
                </div>
                <div class="soft-panel" style="border-left: 3px solid var(--accent);">
                    <div style="font-weight: 600; color: var(--accent); margin-bottom: 0.5rem;">Analytics</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary);">Comprehensive dashboards and reporting</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def admin_kpi_card(title, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_admin_page():
    admin_username = os.getenv("RESUME_ANALYZER_ADMIN_USERNAME", "")
    admin_password = os.getenv("RESUME_ANALYZER_ADMIN_PASSWORD", "")

    st.markdown(
        """
        <div class="hero-section">
            <span class="hero-badge">🔐 Admin Dashboard</span>
            <div class="hero-title">Analytics & Operations</div>
            <div class="hero-subtitle">Secure access to resume analytics, user data, and system metrics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    if "admin_ok" not in st.session_state:
        st.session_state["admin_ok"] = False

    with st.form("admin_login"):
        with st.container(border=True):
            render_section_header("Authentication Required", "Enter your admin credentials")
            st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                ad_user = st.text_input("Username", placeholder="Admin username", label_visibility="collapsed")
            with col2:
                ad_password = st.text_input("Password", type="password", placeholder="Admin password", label_visibility="collapsed")
            
            st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("🔓 Unlock Dashboard", use_container_width=True)
            if submitted:
                st.session_state["admin_ok"] = bool(admin_username and admin_password) and ad_user == admin_username and ad_password == admin_password
                if not st.session_state["admin_ok"]:
                    st.error("❌ Invalid credentials. Please try again.")

    if not st.session_state["admin_ok"]:
        return

    st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)

    cursor.execute(
        f"SELECT ID, ip_add, resume_score, {db_text('Predicted_Field')}, {db_text('User_level')}, city, state, country, Timestamp from user_data"
    )
    datanalys = cursor.fetchall()
    plot_data = pd.DataFrame(
        datanalys,
        columns=["Idt", "IP_add", "resume_score", "Predicted_Field", "User_Level", "City", "State", "Country", "Timestamp"],
    )

    cursor.execute(
        f"""SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob, {db_text('Predicted_Field')}, Timestamp,
            Name, Email_ID, resume_score, Page_no, pdf_name, {db_text('User_level')}, {db_text('Actual_skills')},
            {db_text('Recommended_skills')}, {db_text('Recommended_courses')}, city, state, country, latlong,
            os_name_ver, host_name, dev_user from user_data"""
    )
    raw_user_data = cursor.fetchall()
    user_df = pd.DataFrame(
        raw_user_data,
        columns=[
            "ID",
            "Token",
            "IP Address",
            "Name",
            "Mail",
            "Mobile Number",
            "Predicted Field",
            "Timestamp",
            "Predicted Name",
            "Predicted Mail",
            "Resume Score",
            "Total Page",
            "File Name",
            "User Level",
            "Actual Skills",
            "Recommended Skills",
            "Recommended Course",
            "City",
            "State",
            "Country",
            "Lat Long",
            "Server OS",
            "Server Name",
            "Server User",
        ],
    )

    feedback_df = pd.read_sql("select * from user_feedback", connection)
    total_users = int(plot_data["Idt"].count()) if not plot_data.empty else 0
    avg_score = round(pd.to_numeric(plot_data["resume_score"], errors="coerce").fillna(0).mean(), 1) if not plot_data.empty else 0
    total_feedback = int(feedback_df.shape[0])
    system_health = "Stable ✓" if total_users or total_feedback else "Idle"

    kpi_cols = st.columns(4, gap="medium")
    with kpi_cols[0]:
        admin_kpi_card("Total Resumes", total_users, "Candidate profiles analyzed")
    with kpi_cols[1]:
        admin_kpi_card("Avg Score", f"{avg_score}/100", "Mean resume quality")
    with kpi_cols[2]:
        admin_kpi_card("Feedback", total_feedback, "User sentiment entries")
    with kpi_cols[3]:
        admin_kpi_card("Status", system_health, "System operational")

    st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)

    chart_left, chart_right = st.columns([1.15, 0.85], gap="large")
    with chart_left:
        with st.container(border=True):
            render_section_header("Processing Volume", "Resumes analyzed over time")
            if plot_data.empty:
                st.markdown(
                    '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">No data available</div>',
                    unsafe_allow_html=True,
                )
            else:
                trend = (
                    plot_data.assign(Date=plot_data["Timestamp"].astype(str).str.slice(0, 10))
                    .groupby("Date", dropna=False)
                    .size()
                    .reset_index(name="Count")
                )
                fig = px.area(trend, x="Date", y="Count", line_shape="spline")
                fig.update_traces(line_color=THEME["primary"], fillcolor="rgba(124, 58, 237, 0.16)")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=320,
                    font=dict(color=THEME["text"]),
                    hovermode='x unified',
                )
                st.plotly_chart(fig, use_container_width=True)

    with chart_right:
        with st.container(border=True):
            render_section_header("Role Distribution", "")
            if plot_data.empty:
                st.markdown(
                    '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">No data available</div>',
                    unsafe_allow_html=True,
                )
            else:
                mix = plot_data["Predicted_Field"].fillna("Unknown").astype(str).value_counts()
                fig = px.pie(
                    values=mix.values,
                    names=mix.index,
                    hole=0.55,
                    color_discrete_sequence=[THEME["primary"], THEME["secondary"], THEME["accent"], THEME["success"], THEME["danger"]],
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=320,
                    font=dict(color=THEME["text"]),
                )
                st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)

    lower_left, lower_right = st.columns([1.1, 0.9], gap="large")
    with lower_left:
        with st.container(border=True):
            render_section_header("Candidate Records", f"Total: {len(user_df)} profiles")
            if user_df.empty:
                st.markdown(
                    '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">No user records available</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.dataframe(user_df, use_container_width=True, hide_index=True)
                st.markdown(get_csv_download_link(user_df, "User_Data.csv", "📥 Download Report"), unsafe_allow_html=True)

    with lower_right:
        with st.container(border=True):
            render_section_header("Feedback Summary", f"Total: {len(feedback_df)} entries")
            if feedback_df.empty:
                st.markdown(
                    '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">No feedback records available</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.dataframe(feedback_df, use_container_width=True, hide_index=True)
                if "feed_score" in feedback_df:
                    score_mix = feedback_df["feed_score"].astype(str).value_counts().sort_index()
                    fig = px.bar(
                        x=score_mix.index,
                        y=score_mix.values,
                        color=score_mix.index,
                        color_discrete_sequence=[THEME["primary"], THEME["secondary"], THEME["accent"], THEME["success"], THEME["danger"]],
                    )
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0, r=0, t=10, b=0),
                        height=280,
                        xaxis_title="Rating",
                        yaxis_title="Count",
                        showlegend=False,
                        font=dict(color=THEME["text"]),
                    )
                    st.plotly_chart(fig, use_container_width=True)


def run():
    init_database()
    inject_theme()
    nav = render_sidebar()
    render_admin_entry()

    if nav == "User":
        render_user_page()
    elif nav == "Feedback":
        render_feedback_page()
    elif nav == "About":
        render_about_page()
    else:
        render_admin_page()


run()
