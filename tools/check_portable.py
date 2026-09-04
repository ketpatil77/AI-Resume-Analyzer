import importlib
import os
import sqlite3
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT, "App")
DATA_DIR = os.path.join(APP_DIR, "data")
UPLOAD_DIR = os.path.join(APP_DIR, "Uploaded_Resumes")
DB_PATH = os.path.join(DATA_DIR, "cv.sqlite3")


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    require(sys.version_info[:2] == (3, 14), "Python 3.14 is required by the launcher.")

    sys.path.insert(0, APP_DIR)

    for folder in (DATA_DIR, UPLOAD_DIR):
        os.makedirs(folder, exist_ok=True)
        require(os.path.isdir(folder), f"Missing folder: {folder}")

    modules = [
        "streamlit",
        "pandas",
        "plotly",
        "pdfminer",
        "pypdf",
        "streamlit_tags",
        "geocoder",
        "geopy",
        "PIL",
        "resume_parser_local",
    ]
    for module in modules:
        importlib.import_module(module)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("select 1")
    conn.close()

    print("Portable check passed.")


if __name__ == "__main__":
    main()
