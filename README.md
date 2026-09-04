# AI Resume Analyzer - Student / Staff Viva Explanation

> Source checked: `README.md`, `package.json`, `App/App.py`, `App/resume_parser_local.py`, `App/data/cv.sqlite3`, `src/App.tsx`, `src/lib/analyseResume.ts`, `src/hooks/useResumeParser.ts`, `start.bat`, `start.sh`, and `PORTABLE_RUN.md`.
> Unknown college/student details are marked as `Not available / Not implemented`.

---

## 1. Basic Project Details

| Field | Answer |
|---|---|
| Project Name | AI Resume Analyzer |
| Student Name(s) | Not available / Not implemented |
| Class / Semester | Not available / Not implemented |
| Department | Not available / Not implemented |
| College / Institute | Not available / Not implemented |
| Guide / Staff Name | Not available / Not implemented |
| Project Type | Hybrid web project: React resume analyzer plus Streamlit analytics/admin app |
| Domain | HR Tech, Resume Screening, Career Guidance |
| Main Programming Language(s) | TypeScript, Python |
| Frontend Technology | React 18, Vite, TypeScript, Tailwind CSS, Streamlit UI |
| Backend Technology | Python Streamlit app with local parsing and SQLite storage; React uses client-side TypeScript logic |
| Database Used | SQLite database file: `App/data/cv.sqlite3` |
| IDE / Editor Used | Not available / Not implemented |
| Operating System Used | Project supports Windows and Linux/macOS style startup scripts; current code also records OS using Python `platform` |

### Staff-style questions

**What is the name of your project?**  
AI Resume Analyzer.

**Which domain does your project belong to?**  
HR Tech and career guidance.

**Is this project web-based, desktop-based, mobile-based, or hybrid?**  
Hybrid web-based project. It has a React web dashboard and a Streamlit web admin/analytics app.

**Which technologies did you use and why?**  
React and Vite for fast browser UI, TypeScript for safer client-side logic, Python and Streamlit for resume parsing/admin dashboard, and SQLite for local portable data storage.

**Which part did you personally understand and work on?**  
Not available / Not implemented.

---

## 2. Short Project Summary

### 2.1 One-line Explanation

AI Resume Analyzer checks a resume, extracts useful details, scores resume quality, shows missing skills, and stores analysis data for admin review.

### 2.2 Simple Explanation in Student Language

This project helps a student or job seeker improve their resume. The user uploads a resume, the system reads it, finds skills and details, gives a score, shows improvement points, and recommends skills/courses.

### 2.3 Technical Explanation

The React app parses PDF/DOCX files in the browser using `pdfjs-dist` and `mammoth`, then scores the resume using rule-based TypeScript logic in `src/lib/analyseResume.ts`. The Streamlit app in `App/App.py` accepts PDF resumes, extracts text using `pdfminer.six`, extracts profile details using `App/resume_parser_local.py`, computes a rule-based score, recommends fields/skills/courses, and stores records in SQLite.

### Staff-style questions

**Explain your project in one sentence.**  
It is a resume analysis system that gives ATS-style score, skills, gaps, and recommendations.

**Explain your project as if you are explaining it to a non-technical person.**  
It reads a resume and tells what is good, what is missing, and how the candidate can improve it.

**Explain your project technically.**  
It uses PDF/DOCX parsing, keyword matching, section detection, scoring rules, charts, and SQLite storage.

**What is the main purpose of this project?**  
To reduce manual resume checking and give fast resume improvement guidance.

---

## 3. Problem Statement

### 3.1 What problem existed before this project?

Manual resume screening takes time. Candidates do not know which sections, skills, keywords, or proof points are missing. Placement teams also need structured resume data and feedback records.

### 3.2 Why is this problem important?

Resume quality affects shortlisting. A weak or badly formatted resume can fail ATS screening even if the candidate has skills.

### 3.3 Who faces this problem?

Students, job seekers, placement cells, recruiters, and admins who manage candidate resume data.

### 3.4 How does your project solve this problem?

It automates resume parsing, gives a resume score, predicts a career field, detects skills, recommends missing skills/courses, and stores analysis records locally.

### Staff-style questions

**What is the problem statement of your project?**  
Manual resume review is slow and inconsistent, so this system automates resume checking and improvement guidance.

**Why did you select this topic?**  
Because students and job seekers need fast resume feedback before applying.

**What problem does your system solve?**  
It solves slow screening and unclear resume improvement feedback.

**What happens if this system is not used?**  
Resume checking remains manual, slower, and less structured.

**Who are the real users of this system?**  
Candidates, students, placement teams, and recruiters.

---

## 4. Aim and Objectives

### 4.1 Aim of the Project

To build a local resume analyzer that parses resumes, scores quality, recommends improvements, and provides admin analytics.

### 4.2 Objectives

- Upload and parse resumes.
- Extract name, email, phone, degree, skills, and page count.
- Calculate ATS-style resume score.
- Detect resume sections and missing sections.
- Predict career field using detected skills.
- Recommend skills and learning courses.
- Store analysis and feedback in SQLite.
- Provide admin dashboard with records, charts, and CSV download.

### Staff-style questions

**What is the aim of your project?**  
To analyze resumes and give improvement suggestions automatically.

**List the main objectives of your project.**  
Parsing, scoring, skill detection, recommendations, storage, feedback, and analytics.

**Which objective is the most important and why?**  
Resume analysis and scoring, because it gives the main output to the user.

**Are all objectives completed in the final project?**  
Most core objectives are implemented. Advanced AI/ML model-based scoring is not implemented.

---

## 5. Existing System and Proposed System

### 5.1 Existing System

In the existing/manual system, staff or recruiters read resumes manually and decide quality based on personal review.

### 5.2 Problems in Existing System

- Time-consuming resume checking.
- No automatic scoring.
- Candidate does not get instant improvement suggestions.
- Manual review may be inconsistent.
- Data is difficult to track without a system.

### 5.3 Proposed System

The proposed system accepts resumes, extracts text/details, checks sections and skills, calculates score, recommends improvements, and stores results in a local SQLite database.

### 5.4 Advantages of Proposed System

- Fast resume analysis.
- Structured ATS-style result.
- Skill gap detection.
- Admin records and charts.
- Portable local database.

### Staff-style questions

**What is the existing/manual system?**  
Manual resume reading and shortlisting.

**What are the drawbacks of the existing system?**  
It is slow, inconsistent, and does not give instant feedback.

**What is your proposed system?**  
An automated resume analyzer with scoring, suggestions, and admin analytics.

**How is your system better than the existing system?**  
It gives faster, structured, and reusable analysis.

---

## 6. Scope of the Project

### 6.1 Where can this project be used?

It can be used in college placement cells, resume improvement sessions, job preparation, and initial screening workflows.

### 6.2 Who can use this project?

Candidates, students, admins, placement staff, and recruiters.

### 6.3 Current Scope

- React PDF/DOCX resume analysis dashboard.
- Streamlit PDF resume analyzer.
- Local SQLite storage.
- Admin dashboard.
- Feedback collection.
- CSV export for admin records.

### 6.4 Out of Scope / Not Included

- Cloud login system.
- Enterprise security.
- Real ML model training.
- Multi-user role-based backend auth.
- Online API deployment.

### Staff-style questions

**What is the scope of your project?**  
Resume analysis, scoring, suggestions, and admin analytics.

**Where can this project be implemented?**  
Colleges, placement cells, and job-preparation environments.

**What is not included in your current project?**  
Enterprise authentication, cloud deployment, and trained ML model inference.

**Can this project be used in real life?**  
Yes, for basic resume checking and improvement guidance.

---

## 7. Technology Stack

### 7.1 Frontend

| Technology | Version / Details | Why Used? | Where Used? |
|---|---|---|---|
| React | `^18.3.1` | Build interactive dashboard UI | `src/App.tsx`, `src/components/*` |
| Vite | `^6.0.7` | Fast local dev server and build tool | `package.json`, `vite.config.ts` |
| TypeScript | `^5.7.2` | Safer frontend logic | `src/**/*.ts`, `src/**/*.tsx` |
| Tailwind CSS | `^3.4.17` | Styling utility classes | `src/index.css`, `tailwind.config.ts` |
| Streamlit | Listed in `App/requirements.txt` | Python UI/admin pages | `App/App.py` |

### 7.2 Backend

| Technology | Version / Details | Why Used? | Where Used? |
|---|---|---|---|
| Python | Version not pinned in repo | Resume parsing, database, Streamlit app | `App/App.py`, `App/resume_parser_local.py` |
| Streamlit | From requirements | Runs Python web app | `App/App.py` |
| TypeScript client logic | Local browser logic | React analyzer runs without API key | `src/lib/analyseResume.ts` |

### 7.3 Database

| Database | File / Server Name | Why Used? | Main Use |
|---|---|---|---|
| SQLite | `App/data/cv.sqlite3` | Local, portable, no server needed | Store resume records and feedback |
| MySQL | Optional through `RESUME_ANALYZER_DB=mysql` | Legacy/optional database mode | Code exists in `App/App.py`, not default |

### 7.4 Libraries / Packages / Tools

| Library / Tool | Purpose | File / Section Where Used |
|---|---|---|
| `pdfjs-dist` | Parse PDF in browser | `src/hooks/useResumeParser.ts` |
| `mammoth` | Extract DOCX text | `src/hooks/useResumeParser.ts` |
| `pdfminer.six` | Extract PDF text in Python | `App/App.py`, `App/resume_parser_local.py` |
| `pypdf` | Count PDF pages | `App/resume_parser_local.py` |
| `pandas` | Tables and dataframes | `App/App.py` |
| `plotly` | Charts/gauge/pie/bar/area | `App/App.py` |
| `streamlit-tags` | Skill tag display | `App/App.py` |
| `Pillow` | Image dependency | `App/App.py` imports `Image` |
| `geocoder`, `geopy` | Location lookup | `get_client_location()` in `App/App.py` |
| `PyMySQL` | Optional MySQL connection | `App/App.py` |
| `lucide-react` | React icons | `src/App.tsx`, components |

### Staff-style questions

**Which frontend technology did you use?**  
React with Vite/TypeScript and Streamlit for Python UI.

**Which backend technology did you use?**  
Python Streamlit and local TypeScript analysis logic.

**Which database did you use?**  
SQLite.

**Why did you choose this database?**  
It is local, portable, and needs no database server.

**Which libraries are important in your project?**  
PDF.js, Mammoth, PDFMiner, PyPDF, Pandas, Plotly, Streamlit, SQLite.

**What is the role of each library?**  
They parse resumes, analyze data, show UI/charts, and store records.

---

## 8. Folder Structure and Important Files

### 8.1 Main Folder Structure

```text
AI-Resume-Analyzer/
├── App/
│   ├── App.py
│   ├── Courses.py
│   ├── Logo/
│   ├── Uploaded_Resumes/
│   ├── data/
│   │   └── cv.sqlite3
│   ├── requirements.txt
│   └── resume_parser_local.py
├── src/
│   ├── App.tsx
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   │   ├── analyseResume.ts
│   │   └── exportPDF.ts
│   ├── styles/
│   ├── types/
│   ├── index.css
│   └── main.tsx
├── tools/
│   ├── check_portable.py
│   ├── portable_start.ps1
│   └── smart_deps.py
├── package.json
├── package-lock.json
├── start.bat
├── start.sh
├── PORTABLE_RUN.md
├── vite.config.ts
└── README.md
```

### 8.2 Important Files Explanation

| File / Folder Name | Purpose | Why Important? |
|---|---|---|
| `src/App.tsx` | Main React app shell | Controls upload, JD input, admin login modal, and results dashboard |
| `src/hooks/useResumeParser.ts` | Browser PDF/DOCX parser | Validates files and extracts resume text |
| `src/lib/analyseResume.ts` | React scoring logic | Calculates ATS score, sections, skills, keywords, suggestions |
| `App/App.py` | Main Streamlit app | Handles Python UI, PDF upload, DB insert, admin dashboard, feedback |
| `App/resume_parser_local.py` | Local parser | Extracts name, email, phone, skills, degree, page count |
| `App/Courses.py` | Course/video lists | Supplies recommended course and video links |
| `App/data/cv.sqlite3` | SQLite database | Stores resume analysis and feedback |
| `start.bat` | Windows launcher | Starts React app through portable PowerShell script |
| `start.sh` | Linux/macOS launcher | Installs dependencies and starts Vite app |
| `tools/portable_start.ps1` | Portable Windows bootstrap | Downloads Node, installs deps, finds port, opens app |

### Staff-style questions

**Show your project folder structure.**  
See folder structure above.

**Which is the main file of your project?**  
React: `src/App.tsx`. Streamlit: `App/App.py`.

**Which file starts the application?**  
React starts from `src/main.tsx`; Streamlit starts from `App/App.py`.

**Which file contains main logic?**  
React logic: `src/lib/analyseResume.ts`; Streamlit logic: `App/App.py` and `App/resume_parser_local.py`.

**Which file contains database logic?**  
`App/App.py` contains SQLite connection, table creation, insert, select, and CSV export.

**Which file contains UI/design?**  
React UI: `src/App.tsx`, `src/components/*`, `src/index.css`, `src/styles/themes.css`. Streamlit UI: `inject_theme()` in `App/App.py`.

---

## 9. Installation and Setup

### 9.1 Software Requirements

| Software | Required Version | Purpose |
|---|---|---|
| Node.js | Windows launcher downloads Node `22.11.0`; manual install can use Node LTS | Run React/Vite app |
| npm | Comes with Node | Install React dependencies |
| Python | Not pinned in repo | Run Streamlit app |
| PowerShell | Windows PowerShell | Run `start.bat` portable bootstrap |
| Browser | Any modern browser | Open local web app |

### 9.2 Hardware Requirements

| Component | Minimum Requirement |
|---|---|
| Processor | Dual-core processor or better |
| RAM | 4 GB minimum, 8 GB recommended |
| Storage | Around 1 GB free for dependencies and uploads |
| Internet Required? | Required on first run for dependency download; not required after dependencies are installed for local analysis |

### 9.3 Setup Steps

```bash
# Step 1: Go to project folder
cd AI-Resume-Analyzer

# Step 2: Install React dependencies
npm install

# Step 3: Start React frontend
npm run client -- --host 127.0.0.1 --port 5173

# Optional Step 4: Install Python dependencies for Streamlit app
python -m pip install -r App/requirements.txt

# Optional Step 5: Start Streamlit app
cd App
python -m streamlit run App.py
```

### Staff-style questions

**How do you install this project?**  
Run `npm install` for React and `python -m pip install -r App/requirements.txt` for Streamlit.

**Which software is required before running it?**  
Node.js/npm for React. Python/pip for Streamlit.

**Are there any dependencies?**  
Yes. They are listed in `package.json` and `App/requirements.txt`.

**How do you install dependencies?**  
Use `npm install` and `python -m pip install -r App/requirements.txt`.

**Does this project require internet?**  
First dependency install needs internet. Local analysis works after setup.

---

## 10. How to Start / Run the Project

### 10.1 Command to Start Frontend

```bash
npm run client -- --host 127.0.0.1 --port 5173
```

Windows one-click:

```bat
start.bat
```

Linux/macOS:

```bash
./start.sh
```

### 10.2 Command to Start Backend

```bash
cd App
python -m streamlit run App.py
```

### 10.3 Command to Start Database / Server

```bash
# No separate database server required.
# SQLite database file is used automatically:
# App/data/cv.sqlite3
```

### 10.4 URL / Port After Running

| Part | URL / Port |
|---|---|
| Frontend | `http://127.0.0.1:5173` by default; launcher finds free port from `5173` to `8999` |
| Backend | Streamlit default: `http://localhost:8501` |
| Admin Panel | React: Admin Login button in header. Streamlit: `Admin` navigation page |
| API Base URL | Not available / Not implemented |

### 10.5 Login Details, If Any

| Role | Username / Email | Password | Notes |
|---|---|---|---|
| React Admin | Configure locally | Configure locally | Optional demo values use `VITE_DEMO_ADMIN_USERNAME` and `VITE_DEMO_ADMIN_PASSWORD`; this browser-only gate does not protect server data |
| Streamlit Admin | Configure locally | Configure locally | Required env vars: `RESUME_ANALYZER_ADMIN_USERNAME` and `RESUME_ANALYZER_ADMIN_PASSWORD` |

### Staff-style questions

**How do you run your project?**  
Use `start.bat` on Windows or run `npm run client -- --host 127.0.0.1 --port 5173` manually.

**Which command starts the project?**  
React: `npm run client`. Streamlit: `python -m streamlit run App.py`.

**Which port is used?**  
React uses `5173` by default. Streamlit uses `8501` by default.

**How do you open it in browser?**  
Open `http://127.0.0.1:5173` for React or `http://localhost:8501` for Streamlit.

**Is login required?**  
Normal resume analysis does not require login. Admin dashboard requires login.

**What are the admin credentials?**  
Values configured through environment variables.

---

## 11. How to Stop / Turn Off the Project

### 11.1 Stop Frontend

Press `Ctrl + C` in the terminal running Vite.

### 11.2 Stop Backend

Press `Ctrl + C` in the terminal running Streamlit.

### 11.3 Stop Database / Server

No separate database server is running. SQLite is a local file, so stopping the app is enough.

### Staff-style questions

**How do you stop the running project?**  
Press `Ctrl + C` in the terminal.

**What happens if you close the terminal?**  
The local server stops.

**Is data lost when the project is stopped?**  
No. SQLite data remains in `App/data/cv.sqlite3`.

**How do you restart it again?**  
Run the same start command or double-click `start.bat` again.

---

## 12. User Roles and Access

### 12.1 Roles in Project

| Role | Permissions / Work | Pages Accessible |
|---|---|---|
| Candidate / User | Upload resume, see score, skills, recommendations | React main page, Streamlit `User` page |
| Admin | View records, charts, feedback, download CSV | React admin unlock message, Streamlit `Admin` page |
| Placement Cell / Recruiter | Review structured results and analytics | Streamlit `Admin` dashboard after login |

### 12.2 Role-wise Explanation

**Role 1: Candidate / User**  
What this user can do: upload resume, enter details, view score, predicted field, current skills, recommended skills, courses, checklist, and PDF preview.

**Role 2: Admin**  
What this user can do: log in, view total resumes, average score, feedback count, role distribution, candidate records, feedback records, and download CSV.

**Role 3: Placement Cell / Recruiter**  
What this user can do: use admin analytics to review candidate readiness and resume quality trends.

### Staff-style questions

**How many user roles are there?**  
Three practical roles: Candidate/User, Admin, Placement Cell/Recruiter.

**What can a normal user do?**  
Upload resume and view analysis.

**What can an admin do?**  
View analytics, records, feedback, and download report.

**Is there role-based access?**  
Basic admin gate exists. Full enterprise role-based access is not implemented.

**Which pages are protected?**  
Streamlit `Admin` page is protected by username/password.

---

## 13. Main Features

### 13.1 Feature List

| No. | Feature Name | What It Does | User Role |
|---|---|---|---|
| 1 | Resume Upload | Accepts PDF in Streamlit and PDF/DOCX in React | Candidate |
| 2 | Resume Parsing | Extracts text and profile data | Candidate |
| 3 | Resume Scoring | Calculates ATS-style score | Candidate |
| 4 | Skill Detection | Finds current skills and missing/recommended skills | Candidate |
| 5 | Job Description Match | React compares resume with pasted job description | Candidate |
| 6 | Admin Analytics | Shows records, charts, feedback, CSV download | Admin |

### 13.2 Feature-wise Explanation

**Feature 1: Resume Upload**  
Purpose: take resume input from user.  
How it works: file uploader accepts resume file.  
Input: PDF in Streamlit; PDF or DOCX in React.  
Processing: validates file type and extracts text.  
Output: parsed resume text/details.

**Feature 2: Resume Analysis and Scoring**  
Purpose: judge resume quality.  
How it works: checks contact, summary, experience, skills, education, formatting, sections, and keywords.  
Input: extracted resume text.  
Processing: rule-based scoring in `src/lib/analyseResume.ts` and `build_resume_checks()` in `App/App.py`.  
Output: score, verdict, section result, suggestions.

**Feature 3: Admin Dashboard**  
Purpose: monitor stored records and feedback.  
How it works: reads SQLite tables and displays KPIs/charts/dataframes.  
Input: database records.  
Processing: Pandas and Plotly charts.  
Output: dashboard, tables, CSV download.

### Staff-style questions

**What are the main features of your project?**  
Upload, parse, score, skill detection, recommendations, job match, admin analytics, feedback.

**Which feature is most important?**  
Resume analysis and scoring.

**Explain one feature with input, process, and output.**  
Input: PDF resume. Process: text extraction and rule checks. Output: score, skills, and suggestions.

**Which feature was difficult to implement?**  
Resume parsing and scoring, because resume formats are different.

**What happens when the user clicks this button?**  
For `Analyze Resume`, the system validates inputs, parses the resume, calculates score, stores data, and shows results.

---

## 14. Complete System Workflow

### 14.1 Step-by-step Workflow

1. User opens React or Streamlit app.
2. User uploads resume.
3. React accepts PDF/DOCX; Streamlit accepts PDF.
4. System validates file type and basic text length.
5. System extracts resume text.
6. System extracts profile details like name, email, phone, degree, skills, and pages.
7. System checks sections, skills, keywords, and formatting.
8. System calculates resume score.
9. System predicts career field and candidate level in Streamlit.
10. System recommends missing skills, courses, and actions.
11. Streamlit stores data in SQLite.
12. User/admin views results, charts, feedback, and records.

### 14.2 Input-Process-Output Flow

| Step | Input | Process | Output |
|---|---|---|---|
| 1 | Resume file | File validation | Accepted or error message |
| 2 | Resume text | Parsing and keyword extraction | Name, email, phone, skills, sections |
| 3 | Parsed text/details | Rule-based scoring | Resume score and verdict |
| 4 | Analysis result | UI rendering and DB insert | Dashboard, charts, saved records |

### 14.3 Workflow Diagram Text

```text
User -> Upload Resume -> Validate File -> Extract Text -> Parse Details -> Score Resume -> Recommend Skills/Courses -> Store in SQLite -> Show Dashboard/Admin Reports
```

### Staff-style questions

**Explain the complete workflow of your project.**  
The user uploads a resume, the system extracts text, checks details and sections, calculates score, recommends improvements, stores data, and displays output.

**What happens first when the project starts?**  
The UI loads and the user sees upload/input options.

**What happens after user enters data?**  
The app validates the inputs and processes the resume.

**Where is the data processed?**  
React processing is in `src/lib/analyseResume.ts`; Streamlit processing is in `App/App.py` and `App/resume_parser_local.py`.

**Where is the result displayed?**  
React result dashboard or Streamlit User page tabs.

**Is data stored in database? At which step?**  
Yes. Streamlit inserts data after successful resume analysis.

---

## 15. Page / Screen / Section Explanation

### 15.1 Pages List

| Page / Screen Name | URL / Route / File | Purpose | Main Components |
|---|---|---|---|
| React Home Upload | `src/App.tsx` at `/` | Upload PDF/DOCX and analyze | `UploadZone`, `JDInput`, `AnalyseButton` |
| React Results Dashboard | Same page, `#results-dashboard` | Show ATS score and insights | `ATSScoreMeter`, `SectionScorecard`, `SkillsAnalysis`, `KeywordHeatmap` |
| React Admin Login | Header admin panel in `src/App.tsx` | Basic admin unlock | Email/password form |
| Streamlit User Page | `App/App.py`, `render_user_page()` | PDF analysis flow | Upload form, score, tabs, PDF preview |
| Streamlit Feedback Page | `render_feedback_page()` | Collect and show feedback | Form, pie chart, recent feedback table |
| Streamlit About Page | `render_about_page()` | Explain project | Workflow, features, stack |
| Streamlit Admin Page | `render_admin_page()` | Admin analytics | Login, KPIs, charts, tables, CSV download |

### 15.2 Detailed Page Explanation

**Page 1: React Home Upload**  
Where is it located? `src/App.tsx`.  
What does this page show? Resume upload area, job description input, analyze button, theme/header controls.  
Which buttons / inputs are available? Upload file, clear resume, job description text input, Analyze button, Admin button.  
What happens after clicking each button? Upload parses file, clear removes file/result, Analyze runs `analyseResume()`, Admin opens login panel.  
Which code file controls this page? `src/App.tsx`, `src/hooks/useResumeParser.ts`, `src/lib/analyseResume.ts`.

**Page 2: Streamlit User Page**  
Where is it located? `render_user_page()` in `App/App.py`.  
What does this page show? Hero, name/email/phone fields, PDF upload, analysis output, skills, courses, videos, PDF preview.  
Which buttons / inputs are available? Name, email, phone, PDF uploader, `Analyze Resume`, course slider.  
What happens after clicking each button? `Analyze Resume` calls `analyze_resume()`, inserts data using `insert_data()`, and displays tabs.  
Which code file controls this page? `App/App.py`.

**Page 3: Streamlit Admin Page**  
Where is it located? `render_admin_page()` in `App/App.py`.  
What does this page show? Admin login, KPIs, charts, candidate records, feedback records.  
Which buttons / inputs are available? Username, password, `Unlock Dashboard`, `Download Report`.  
What happens after clicking each button? Login checks credentials; download creates CSV link.  
Which code file controls this page? `App/App.py`.

### Staff-style questions

**Explain the home page.**  
The home page lets users upload a resume and start analysis.

**Explain the dashboard page.**  
It shows ATS score, section scores, matched/missing skills, keywords, job match, suggestions, and summary.

**What is the use of this section?**  
Each section gives one part of resume feedback.

**Which page is opened after login?**  
Streamlit stays on Admin page and unlocks dashboard content.

**Which page shows final output?**  
React Results Dashboard or Streamlit User result tabs.

**Which page is for admin?**  
Streamlit `Admin` page.

---

## 16. Module-wise Explanation

### 16.1 Modules List

| Module No. | Module Name | Purpose | Important Files |
|---|---|---|---|
| 1 | Upload and Parsing Module | Accept resume and extract text/details | `src/hooks/useResumeParser.ts`, `App/resume_parser_local.py` |
| 2 | Scoring Module | Calculate resume score | `src/lib/analyseResume.ts`, `App/App.py` |
| 3 | Recommendation Module | Recommend field, skills, courses | `App/App.py`, `App/Courses.py` |
| 4 | Database Module | Store and read analysis/feedback | `App/App.py`, `App/data/cv.sqlite3` |
| 5 | Admin Analytics Module | Show KPIs/charts/reports | `App/App.py` |

### 16.2 Module Details

**Module 1: Upload and Parsing**  
Purpose: collect resume and extract text/profile data.  
Input: PDF/DOCX in React; PDF in Streamlit.  
Processing / Logic: `pdfjs-dist`, `mammoth`, `pdfminer.six`, `pypdf`, regex extraction.  
Output: resume text, name, email, phone, degree, skills, pages.  
Important functions / files: `parseFile()`, `ResumeParser.get_extracted_data()`.

**Module 2: Scoring**  
Purpose: score resume quality.  
Input: extracted text and optional job description.  
Processing / Logic: section detection, skill matching, keyword counting, weak phrase detection, weighted score.  
Output: ATS score, section scores, verdict, checklist.  
Important functions / files: `analyseResume()`, `scoreResume()`, `build_resume_checks()`.

**Module 3: Recommendation**  
Purpose: suggest field, skills, and courses.  
Input: detected skills.  
Processing / Logic: compare skills with `FIELD_CATALOG` keyword sets.  
Output: predicted field, recommended skills, course list.  
Important functions / files: `infer_recommendation()`, `App/Courses.py`.

### Staff-style questions

**How many modules are in your project?**  
Five main modules.

**Explain each module.**  
Upload/parsing, scoring, recommendation, database, admin analytics.

**Which module handles input?**  
Upload and parsing module.

**Which module handles processing?**  
Scoring and recommendation modules.

**Which module handles output?**  
React dashboard and Streamlit result tabs.

**Which module connects with the database?**  
Database module in `App/App.py`.

---

## 17. Working of Important Buttons / Actions

| Button / Action | Page | What It Does | Code File / Function | Output |
|---|---|---|---|---|
| Upload resume | React Home | Parses PDF/DOCX text | `useResumeParser.parseFile()` | Resume text or parse error |
| Analyze | React Home | Runs client analysis | `handleAnalyse()`, `analyseResume()` | Results Dashboard |
| Admin Login | React Header | Opens admin form and checks credentials | `handleAdminSubmit()` | Admin unlocked or invalid credentials |
| Analyze Resume | Streamlit User | Parses PDF, scores, stores data | `render_user_page()`, `analyze_resume()`, `insert_data()` | Tabs with analysis result |
| Submit Feedback | Streamlit Feedback | Saves feedback | `insertf_data()` | Success message and chart update |
| Unlock Dashboard | Streamlit Admin | Verifies admin credentials | `render_admin_page()` | Admin analytics view |
| Download Report | Streamlit Admin | Creates CSV download | `get_csv_download_link()` | `User_Data.csv` download |

### Staff-style questions

**What happens after clicking the submit button?**  
Feedback is inserted into `user_feedback` table.

**What happens after clicking upload?**  
The app validates file type and extracts text.

**What happens after login?**  
Admin dashboard content is shown if credentials are correct.

**What happens after logout?**  
Logout is not implemented.

**What happens if wrong input is given?**  
The app shows validation or error message.

**Which function runs after this action?**  
Depends on action: `parseFile()`, `handleAnalyse()`, `analyze_resume()`, `insertf_data()`, or `render_admin_page()`.

---

## 18. Input Details

### 18.1 Inputs Taken from User

| Input Name | Type | Required? | Validation | Example |
|---|---|---|---|---|
| Resume file | PDF/DOCX in React; PDF in Streamlit | Yes | File type and text length | `resume.pdf` |
| Job description | Text | No | Trimmed text | React developer job description |
| Name | Text | Yes in Streamlit | Non-empty check | Rahul Patil |
| Email | Text | Yes in Streamlit | Non-empty check only | user@example.com |
| Phone | Text | Yes in Streamlit | Non-empty check only | +91 9876543210 |
| Feedback name/email/comments/rating | Text/slider | Form fields | Stored directly | Rating 4 |
| Admin credentials | Text/password | Yes for admin | Exact match | Values configured through environment variables |

### 18.2 Input Validation

React checks file type, parses PDF/DOCX, and rejects resume text shorter than 100 characters. Streamlit checks that name, email, phone, and PDF file are present before analysis. Streamlit uploader accepts only PDF.

### Staff-style questions

**What input does your project take?**  
Resume file, job description, user details, feedback, and admin credentials.

**Is validation applied?**  
Yes, basic file and required-field validation is applied.

**What happens if the user enters wrong data?**  
The app shows an error message or rejects the input.

**What happens if the user leaves fields empty?**  
Streamlit shows `Please fill in all fields and upload a resume.`

**What type of file/data is accepted?**  
React accepts PDF/DOCX. Streamlit accepts PDF.

---

## 19. Output Details

### 19.1 Outputs Generated by System

| Output Name | Where Displayed? | Based On Which Input? | Purpose |
|---|---|---|---|
| ATS Score | React dashboard | Resume text and optional JD | Show resume quality |
| Section Scores | React dashboard | Resume sections | Show strengths/weaknesses |
| Matched/Missing Skills | React and Streamlit | Resume keywords | Show skill gaps |
| Predicted Field | Streamlit User/Admin | Detected skills | Suggest career direction |
| Recommended Courses | Streamlit User | Predicted field | Learning guidance |
| Admin KPIs/Charts | Streamlit Admin | SQLite records | Operational analytics |
| CSV Report | Streamlit Admin | SQLite user data | Export records |

### 19.2 Final Output Explanation

The final output is a resume analysis result with score, parsed details, predicted field, current skills, recommended skills, checklist, course suggestions, and admin analytics records.

### Staff-style questions

**What output does your system generate?**  
Resume score, skills, suggestions, charts, and saved records.

**Where is the output shown?**  
React dashboard and Streamlit pages.

**Is output stored in database?**  
Streamlit output is stored in SQLite `user_data`; feedback is stored in `user_feedback`.

**Can output be downloaded/exported?**  
Admin can download `User_Data.csv`. React export creates a text report through `src/lib/exportPDF.ts`.

**How do you verify the output is correct?**  
Check parsed details, score rules, database rows, and UI result against uploaded resume content.

---

## 20. Database Explanation

### 20.1 Database Name

`App/data/cv.sqlite3`

### 20.2 Why this database was used?

SQLite is simple, local, portable, and does not require a separate server.

### 20.3 Tables / Collections

| Table / Collection Name | Purpose | Important Fields |
|---|---|---|
| `user_data` | Stores resume analysis records | `ID`, `act_name`, `act_mail`, `Name`, `Email_ID`, `resume_score`, `Predicted_Field`, `User_level`, `Actual_skills`, `Recommended_skills`, `pdf_name` |
| `user_feedback` | Stores user feedback | `ID`, `feed_name`, `feed_email`, `feed_score`, `comments`, `Timestamp` |
| `sqlite_sequence` | SQLite auto-increment tracking | `name`, `seq` |

### 20.4 Field-wise Explanation

**Table 1: `user_data`**

| Field Name | Data Type | Purpose |
|---|---|---|
| `ID` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique record id |
| `sec_token` | varchar(20) | Session/security token |
| `ip_add` | varchar(50) | Host IP address |
| `host_name` | varchar(50) | System host name |
| `dev_user` | varchar(50) | System user name |
| `os_name_ver` | varchar(50) | OS name/version |
| `latlong`, `city`, `state`, `country` | varchar | Location metadata |
| `act_name`, `act_mail`, `act_mob` | varchar | User-entered details |
| `Name`, `Email_ID` | varchar | Parser-detected candidate name/email |
| `resume_score` | VARCHAR(8) | Resume score |
| `Timestamp` | VARCHAR(50) | Analysis time |
| `Page_no` | VARCHAR(5) | Resume page count |
| `Predicted_Field` | BLOB | Predicted career field |
| `User_level` | BLOB | Fresher/intermediate/experienced |
| `Actual_skills` | BLOB | Detected skills |
| `Recommended_skills` | BLOB | Suggested skills |
| `Recommended_courses` | BLOB | Suggested courses |
| `pdf_name` | varchar(50) | Uploaded file name |

**Table 2: `user_feedback`**

| Field Name | Data Type | Purpose |
|---|---|---|
| `ID` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique feedback id |
| `feed_name` | varchar(50) | Feedback user name |
| `feed_email` | VARCHAR(50) | Feedback email |
| `feed_score` | VARCHAR(5) | Rating score |
| `comments` | VARCHAR(100) | User comment |
| `Timestamp` | VARCHAR(50) | Feedback time |

### 20.5 Database Operations

| Operation | Where Used? | Purpose |
|---|---|---|
| Insert | `insert_data()` | Save resume analysis |
| Insert | `insertf_data()` | Save feedback |
| Select / Read | `render_admin_page()` | Read user records and charts |
| Select / Read | `render_feedback_page()` | Read feedback chart/table |
| Update | Not implemented | Not available / Not implemented |
| Delete | Not implemented | Not available / Not implemented |

### Staff-style questions

**Which database did you use?**  
SQLite.

**How many tables are there?**  
Three tables in file: `user_data`, `user_feedback`, and `sqlite_sequence`.

**Explain each table.**  
`user_data` stores resume analysis. `user_feedback` stores feedback. `sqlite_sequence` tracks auto-increment IDs.

**What is the primary key?**  
`ID` is primary key in `user_data` and `user_feedback`.

**Where is data inserted?**  
`insert_data()` and `insertf_data()` in `App/App.py`.

**How do you fetch data from database?**  
Using SQL `SELECT` queries and `pandas.read_sql()` in `App/App.py`.

**Is database local or online?**  
Local.

---

## 21. Algorithm / Logic Used

### 21.1 Main Algorithm / Logic

The project uses rule-based resume analysis. It detects sections, keywords, skills, action verbs, weak phrases, contact details, education, experience, and formatting quality. It then calculates score and recommendations.

### 21.2 Step-by-step Logic

1. Extract text from resume.
2. Normalize text into lowercase for matching.
3. Detect email, phone, name, degree, skills, and page count.
4. Check resume sections like summary, education, experience, skills, certifications, projects.
5. Calculate score from section presence and quality signals.
6. Detect matched skills and missing skills.
7. If job description is provided, compare JD terms with resume terms.
8. Generate suggestions and warnings.
9. Store result in SQLite in Streamlit.
10. Display score, charts, and recommendations.

### 21.3 Conditions / Rules Used

| Condition / Rule | Meaning | Where Used? |
|---|---|---|
| Resume text length `< 100` | Resume too short | `useResumeParser.ts`, `src/App.tsx` |
| File is not PDF/DOCX | Invalid upload | `useResumeParser.ts` |
| Missing Streamlit fields | Required fields empty | `render_user_page()` |
| Email/phone regex found | Contact score signal | `analyseResume.ts`, `resume_parser_local.py` |
| Section keyword found | Section is present | `analyseResume.ts`, `build_resume_checks()` |
| Skill keyword match | Skill detected | `analyseResume.ts`, `resume_parser_local.py` |
| Admin credentials exact match | Admin login success | `src/App.tsx`, `App/App.py` |

### Staff-style questions

**What is the main logic of your project?**  
Rule-based resume parsing, scoring, and recommendation.

**Which algorithm is used?**  
Keyword matching, regex extraction, weighted scoring, and rule-based classification.

**Is it rule-based or model-based?**  
Rule-based.

**How is score/result calculated?**  
By checking contact, summary, experience, skills, education, formatting, sections, bullets, and keywords.

**Which conditions are checked?**  
File type, text length, required fields, section presence, skill match, weak phrases, admin credentials.

**Explain the logic line by line at a high level.**  
Upload resume, extract text, find details, check rules, calculate score, create suggestions, show and store result.

---

## 22. API / Routes / Functions Explanation

### 22.1 API Routes, If Any

| Method | Route / Endpoint | Input | Output | Purpose |
|---|---|---|---|---|
| GET | Not implemented | Not implemented | Not implemented | No backend REST API exists |
| POST | Not implemented | Not implemented | Not implemented | No backend REST API exists |
| PUT | Not implemented | Not implemented | Not implemented | No backend REST API exists |
| DELETE | Not implemented | Not implemented | Not implemented | No backend REST API exists |

### 22.2 Important Functions

| Function Name | File Name | Input Parameters | Output / Return | Purpose |
|---|---|---|---|---|
| `parseFile` | `src/hooks/useResumeParser.ts` | `File` | Resume state with text | Parse PDF/DOCX in browser |
| `analyseResume` | `src/lib/analyseResume.ts` | `resumeText`, `jobDescription` | `AnalysisResult` | Produce React analysis result |
| `scoreResume` | `src/lib/analyseResume.ts` | Resume text, JD | Internal score object | Calculate ATS/section scores |
| `exportReport` | `src/lib/exportPDF.ts` | Element id | Text file download | Export React dashboard text |
| `ResumeParser.get_extracted_data` | `App/resume_parser_local.py` | PDF path | Dict | Extract name/email/phone/skills/degree/pages |
| `analyze_resume` | `App/App.py` | Name, email, mobile, PDF file | Result dict | Main Streamlit analysis function |
| `insert_data` | `App/App.py` | Analysis fields | DB insert | Save resume analysis |
| `insertf_data` | `App/App.py` | Feedback fields | DB insert | Save feedback |
| `render_admin_page` | `App/App.py` | None | UI | Show admin login/dashboard |

### Staff-style questions

**Does your project have APIs?**  
No REST API is implemented.

**Which route handles form submission?**  
No route. React uses event handlers; Streamlit uses form/button handlers.

**Which function processes data?**  
React: `analyseResume()`. Streamlit: `analyze_resume()`.

**Which function connects database?**  
SQLite connection and cursor are created in `App/App.py`; inserts use `insert_data()` and `insertf_data()`.

**Which function gives final output?**  
React: `analyseResume()`. Streamlit: `analyze_resume()` result displayed by `render_user_page()`.

**Explain this function in simple words.**  
`analyze_resume()` saves uploaded PDF, extracts resume data, calculates score/recommendations, and returns a result dictionary.

---

## 23. Authentication / Login System

### 23.1 Is Login Available?

Yes, basic admin login is available. Normal user login is not implemented.

### 23.2 Login Flow

1. Admin opens Admin page/panel.
2. Admin enters email and password.
3. System compares with configured credentials.
4. If correct, admin dashboard is unlocked.
5. If wrong, error message is shown.

### 23.3 Security Details

Admin authentication is simple. React can use optional build-time demo values, while Streamlit requires environment variables. Password hashing, database users, and role-based auth are not implemented.

### Staff-style questions

**Is login implemented?**  
Yes, only basic admin login.

**How is user verified?**  
By exact username/password comparison.

**Is password stored securely?**  
No. It is simple demo-level authentication.

**What happens after successful login?**  
Admin dashboard is shown.

**What happens after wrong login?**  
Error message appears.

**Can multiple roles login?**  
No. Only admin login is implemented.

---

## 24. Error Handling and Validation

### 24.1 Possible Errors

| Error Case | Reason | System Response / Message |
|---|---|---|
| No resume uploaded | User clicked analyze without file | React: `Upload a resume before analysis.` |
| Resume too short | Extracted text below 100 chars | React: `Resume seems too short.` |
| Wrong file type | File not PDF/DOCX in React | `Only PDF and DOCX files are supported.` |
| Missing Streamlit fields | Name/email/phone/PDF missing | `Please fill in all fields and upload a resume.` |
| PDF parsing fails | Bad/scanned/unsupported PDF | `Failed to parse resume. Please try again.` |
| Wrong admin credentials | Username/password mismatch | `Invalid admin credentials.` or `Invalid credentials. Please try again.` |
| Empty database | No records yet | Admin/feedback pages show no data messages |

### 24.2 How Errors Are Handled

The app uses basic validation checks, try/catch in React parser/analysis flow, Streamlit error messages, and empty-state messages for missing data.

### Staff-style questions

**What errors can occur in your project?**  
Invalid file, missing fields, parsing failure, short resume text, wrong login, empty database.

**How does your system handle invalid input?**  
It shows an error message and stops processing.

**What happens if database connection fails?**  
No custom DB failure screen is implemented; Streamlit would show runtime error.

**What happens if file format is wrong?**  
React rejects it; Streamlit uploader only allows PDF.

**Are error messages shown to user?**  
Yes.

---

## 25. Testing Performed

### 25.1 Test Cases

| Test Case ID | Test Scenario | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC01 | React invalid file validation | Non-PDF/DOCX file | Error message | Code shows error: only PDF/DOCX supported | Pass by code review |
| TC02 | React short resume validation | Resume text under 100 chars | Error message | Code throws short resume error | Pass by code review |
| TC03 | Streamlit missing input validation | Empty name/email/phone/file | Error message | Code shows required fields error | Pass by code review |
| TC04 | Admin login valid credentials | Configured environment values | Dashboard unlock | Code checks exact credentials | Pass by code review |
| TC05 | Database schema check | `App/data/cv.sqlite3` | Tables present | `user_data`, `user_feedback`, `sqlite_sequence` found | Pass by local schema read |

### 25.2 Types of Testing Done

- [ ] Unit Testing
- [ ] Integration Testing
- [x] System Testing
- [x] UI Testing
- [x] Database Testing
- [x] Validation Testing
- [x] Smoke Testing

### Staff-style questions

**What testing did you perform?**  
Validation checks, database schema check, code review smoke test, and UI workflow review from source.

**Give one test case.**  
If user uploads wrong file type in React, the system shows only PDF/DOCX supported.

**What was the expected output?**  
Error message and no analysis.

**Did you test invalid input?**  
Invalid input handling is confirmed from code paths.

**Did you test database insertion?**  
Database insert functions exist; current database has 6 `user_data` rows and 0 `user_feedback` rows.

**Did you test login?**  
Login logic is confirmed from source code.

---

## 26. Screenshots Required

| Screenshot No. | Screenshot Name | Purpose | File Name / Location |
|---|---|---|---|
| 1 | React Home Upload Screen | Show upload and JD input | Not available / Not implemented |
| 2 | React Results Dashboard | Show ATS score and suggestions | Not available / Not implemented |
| 3 | Streamlit User Upload Page | Show PDF upload form | Not available / Not implemented |
| 4 | Streamlit Analysis Tabs | Show overview/skills/quality/PDF tabs | Not available / Not implemented |
| 5 | Streamlit Feedback Page | Show feedback form and chart | Not available / Not implemented |
| 6 | Streamlit Admin Dashboard | Show KPIs, charts, records | Not available / Not implemented |

Available image assets in project: `App/Logo/RESUM.png`, `App/Logo/recommend.png`. Actual screenshot files were not found.

### Staff-style questions

**Show the home page screenshot.**  
Not available / Not implemented.

**Show the output/result page.**  
Not available / Not implemented.

**Show the admin/dashboard page.**  
Not available / Not implemented.

**Explain what is visible in this screenshot.**  
Not available / Not implemented.

**Which feature is shown in this screenshot?**  
Not available / Not implemented.

---

## 27. Diagrams Required

### 27.1 System Architecture Diagram

Text description: User interacts with React or Streamlit UI. React handles local browser parsing/scoring. Streamlit handles PDF parsing, recommendations, SQLite storage, feedback, and admin analytics.

```text
User
 ├─> React UI (Vite)
 │    ├─> PDF.js / Mammoth Parser
 │    ├─> TypeScript Resume Scoring
 │    └─> Results Dashboard
 └─> Streamlit UI (Python)
      ├─> PDFMiner / PyPDF Parser
      ├─> ResumeParser + Rule Engine
      ├─> SQLite Database (cv.sqlite3)
      └─> Admin Dashboard / Feedback / CSV Export
```

### 27.2 Data Flow Diagram

Text description: Resume data flows from upload to parser, scoring, database, and dashboard output.

```text
Candidate -> Upload Resume -> Parser -> Resume Details + Text -> Scoring Rules -> Result Output
                                                   -> SQLite user_data -> Admin Dashboard
User Feedback -> Feedback Form -> SQLite user_feedback -> Feedback Chart/Admin View
```

### 27.3 Use Case Diagram

Actors: Candidate/User, Admin, Placement Cell/Recruiter.

Use cases: Upload resume, view analysis, submit feedback, login admin, view analytics, download CSV report.

```text
Candidate/User -> Upload Resume
Candidate/User -> View Score and Suggestions
Candidate/User -> Submit Feedback
Admin -> Login
Admin -> View Candidate Records
Admin -> View Feedback
Admin -> Download CSV Report
Placement Cell/Recruiter -> Review Analytics
```

### 27.4 ER Diagram

Entities: `user_data`, `user_feedback`.

Relationships: No direct foreign key relationship implemented.

```text
user_data
- ID (PK)
- act_name
- act_mail
- resume_score
- Predicted_Field
- User_level
- Actual_skills
- Recommended_skills
- pdf_name

user_feedback
- ID (PK)
- feed_name
- feed_email
- feed_score
- comments
- Timestamp

Relationship: No foreign key implemented between user_data and user_feedback.
```

### 27.5 Flowchart

```text
Start
  |
Open App
  |
Upload Resume
  |
Validate File and Required Fields
  |
Valid? ---- No ----> Show Error -> End
  |
 Yes
  |
Extract Resume Text and Details
  |
Calculate Score and Recommendations
  |
Store Data in SQLite (Streamlit)
  |
Display Dashboard / Charts / Suggestions
  |
End
```

### Staff-style questions

**Explain your architecture diagram.**  
It shows two app parts: React client analysis and Streamlit Python analysis/admin with SQLite.

**Explain your data flow diagram.**  
Resume goes from upload to parser to scoring to UI output and database storage.

**Who are the actors in use case diagram?**  
Candidate/User, Admin, and Placement Cell/Recruiter.

**What are the entities in ER diagram?**  
`user_data` and `user_feedback`.

**Explain the flowchart step by step.**  
Start app, upload resume, validate, parse, analyze, store, display result, end.

---

## 28. Advantages

- Reduces manual resume screening effort.
- Gives fast resume feedback.
- Shows ATS-style score and section issues.
- Detects skills and missing skills.
- Provides admin analytics and CSV export.
- Uses local SQLite, so it is portable.
- React version works without API key.

### Staff-style questions

**What are the advantages of your project?**  
Fast analysis, skill gap detection, admin analytics, and local storage.

**How does it save time?**  
It automatically reads and scores the resume.

**How does it help users?**  
It tells users what to improve before applying.

**What makes your project useful?**  
It gives structured feedback and stores analysis records.

---

## 29. Limitations

- Resume parsing accuracy depends on resume format and text quality.
- Scanned/image-only PDFs may not parse well.
- Scoring is rule-based, not trained ML model-based.
- Admin login is simple demo-level security.
- Full REST API is not implemented.
- Update/delete database operations are not implemented.
- Screenshot files are not available in the project.

### Staff-style questions

**What are the limitations of your project?**  
Parsing may fail on poor PDFs, scoring is rule-based, and security is basic.

**What features are missing?**  
Advanced AI model, cloud deployment, enterprise auth, REST API, role management.

**What are the weaknesses of your system?**  
It depends on keyword/rule matching and extracted text quality.

**Where can your project fail?**  
It can fail on scanned resumes, very short resumes, or unusual resume formats.

---

## 30. Future Scope

- Add advanced NLP or AI model for deeper resume understanding.
- Add OCR support for scanned resumes.
- Add recruiter filters and candidate comparison.
- Add secure multi-user login and role-based access.
- Add cloud database and online deployment.
- Add REST API for integration.
- Add better report export such as PDF report.
- Add more job domains and skill catalogs.

### Staff-style questions

**What is the future scope of your project?**  
AI-based scoring, OCR, better auth, deployment, APIs, and recruiter tools.

**What can be added later?**  
Cloud deployment, real ML model, OCR, multi-role login, and PDF export.

**Can this project be deployed online?**  
Yes, after adding proper hosting and security setup.

**Can AI/ML/API/cloud be added later?**  
Yes.

---

## 31. Demo Explanation Script

### 31.1 Opening Line

Good morning. My project is AI Resume Analyzer. It helps users check resume quality, find missing skills, and view improvement suggestions.

### 31.2 Step-by-step Demo Script

First, I will open the project using: `start.bat` on Windows or `npm run client -- --host 127.0.0.1 --port 5173` manually.  
This is the home page. Here: user can upload resume and optionally paste a job description.  
Now I will enter/upload/select: a PDF or DOCX resume in React, or a PDF resume in Streamlit.  
After clicking this button: the system validates the file and extracts text.  
The system processes data by: checking sections, contact details, skills, keywords, weak phrases, and scoring rules.  
The output shown here is: ATS score, section scores, matched skills, missing skills, suggestions, keyword heatmap, and action plan.  
The database stores: Streamlit resume analysis in `user_data` and feedback in `user_feedback`.  
The admin/user can see: admin dashboard with KPIs, charts, records, feedback, and CSV download.  
Finally, the conclusion is: this project helps candidates improve resumes and helps admins review structured resume data.

### Staff-style questions

**Give a live demo of your project.**  
Open app, upload resume, click analyze, explain score and suggestions, then open admin dashboard.

**Start the project in front of me.**  
Use `start.bat` or `npm run client -- --host 127.0.0.1 --port 5173`.

**Explain every step while running it.**  
Explain upload, validation, parsing, scoring, output, and storage.

**Show where input is given.**  
Input is given in upload form and text fields.

**Show where output is generated.**  
Output appears in dashboard/result tabs.

**Show where data is stored.**  
Data is stored in `App/data/cv.sqlite3`.

---

## 32. Common Viva Questions and Blank Answers

**Q1. What is your project about?**  
It is about automatic resume analysis and improvement suggestions.

**Q2. Why did you choose this project?**  
Because students and job seekers need quick resume feedback before applying.

**Q3. What technologies did you use?**  
React, Vite, TypeScript, Tailwind CSS, Python, Streamlit, SQLite, PDF.js, Mammoth, PDFMiner, PyPDF, Pandas, and Plotly.

**Q4. Explain the workflow of your project.**  
Upload resume, validate file, extract text, parse details, score resume, recommend improvements, store data, show dashboard.

**Q5. Which database did you use and why?**  
SQLite, because it is local and portable.

**Q6. What are the main modules?**  
Upload/parsing, scoring, recommendation, database, and admin analytics.

**Q7. What are the main features?**  
Resume upload, parsing, ATS score, skill gap, job match, recommendations, feedback, admin dashboard.

**Q8. Which file is the main file?**  
React: `src/App.tsx`. Streamlit: `App/App.py`.

**Q9. How do you run the project?**  
Use `start.bat` or `npm run client -- --host 127.0.0.1 --port 5173`. For Streamlit use `python -m streamlit run App.py` inside `App`.

**Q10. How do you stop the project?**  
Press `Ctrl + C` in the terminal.

**Q11. What happens after user submits input?**  
The resume is validated, parsed, analyzed, and results are shown.

**Q12. How is the output generated?**  
By rule-based scoring and keyword/section matching.

**Q13. What validations are used?**  
File type validation, text length validation, required field validation, and admin credential validation.

**Q14. What errors can occur?**  
Wrong file type, missing fields, short resume, parsing failure, wrong login, database/runtime errors.

**Q15. What testing did you perform?**  
Code-based validation review, database schema check, and workflow smoke review.

**Q16. What are the advantages?**  
Fast feedback, local storage, structured analytics, and resume improvement guidance.

**Q17. What are the limitations?**  
Rule-based scoring, simple admin login, no OCR, no full REST API, no enterprise auth.

**Q18. What is the future scope?**  
AI model, OCR, cloud deployment, secure login, APIs, recruiter tools.

**Q19. What is your contribution in the project?**  
Not available / Not implemented.

**Q20. If staff asks to change one feature, where will you modify the code?**  
For React UI change `src/App.tsx` or `src/components/*`; for React scoring change `src/lib/analyseResume.ts`; for Streamlit UI/database change `App/App.py`; for parser change `App/resume_parser_local.py`.

---

## 33. Code Explanation Checklist

- [x] I know the main entry file.
- [x] I know how the project starts.
- [x] I know which file handles UI.
- [x] I know which file handles logic.
- [x] I know which file handles database.
- [x] I know which function runs after button click.
- [x] I know how input is validated.
- [x] I know how output is generated.
- [x] I know how errors are handled.
- [x] I know how to run and stop the project.
- [x] I can explain every page/screen.
- [x] I can explain every module.
- [x] I can explain advantages, limitations, and future scope.

---

## 34. Fill Status

| Section | Filled? | Notes |
|---|---|---|
| Basic details | Yes | Student/college details not available |
| Problem statement | Yes | Based on project purpose |
| Technology stack | Yes | Based on package and requirements files |
| Setup/run commands | Yes | Based on launchers and scripts |
| Workflow | Yes | Based on React and Streamlit code |
| Modules | Yes | Based on source files |
| Features | Yes | Based on implemented UI/functions |
| Database | Yes | Based on `cv.sqlite3` schema |
| Pages/screens | Yes | Screenshot files not available |
| Testing | Yes | Source/database review; live browser run not included in this fill |
| Viva Q&A | Yes | Filled with project-backed answers |

---

## 35. Final Student Confidence Check

Before going to staff, student should be able to answer:

- What is the project? AI Resume Analyzer.
- Why was it made? To automate resume checking and improvement guidance.
- Who uses it? Candidates, students, admins, placement cells, recruiters.
- What technologies are used? React, Vite, TypeScript, Python, Streamlit, SQLite, PDF/DOCX parsing libraries.
- How does it start? `start.bat`, `start.sh`, `npm run client`, or `python -m streamlit run App.py`.
- How does it stop? `Ctrl + C`.
- What is the complete workflow? Upload, validate, parse, score, recommend, store, display.
- What is each page doing? User upload/result, feedback, about, admin analytics.
- What is each module doing? Parsing, scoring, recommendation, database, analytics.
- Which file contains which logic? `src/App.tsx`, `src/lib/analyseResume.ts`, `App/App.py`, `App/resume_parser_local.py`.
- Which database/table/field is used? SQLite `cv.sqlite3`, tables `user_data`, `user_feedback`.
- What happens after every important button click? Upload parses, analyze scores, feedback saves, admin login unlocks, download exports CSV.
- What output is generated? Score, skills, suggestions, charts, CSV.
- What testing was done? Validation/database/workflow checks.
- What are limitations and future scope? Rule-based limits now; AI/OCR/cloud/auth/API later.

---

## 36. Notes for Codex While Filling

```text
Read the complete project source code, README, database files, package files, and screenshots if available. Fill this Markdown template accurately. Keep the language simple so a student can explain it to staff. Do not remove any section. If something is not implemented, write "Not implemented". Include exact run commands, file names, function names, database table names, workflow, and staff viva answers.
```
