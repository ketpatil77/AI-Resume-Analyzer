import os
import re

from pdfminer.high_level import extract_text
from pypdf import PdfReader


COMMON_SKILLS = [
    'python', 'java', 'javascript', 'typescript', 'react', 'node js', 'node',
    'django', 'flask', 'streamlit', 'sql', 'mysql', 'postgresql', 'mongodb',
    'html', 'css', 'tailwind', 'bootstrap', 'aws', 'azure', 'gcp', 'docker',
    'kubernetes', 'git', 'github', 'linux', 'machine learning', 'deep learning',
    'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
    'data analysis', 'data visualization', 'power bi', 'tableau', 'excel',
    'android', 'kotlin', 'flutter', 'ios', 'swift', 'figma', 'adobe xd',
    'photoshop', 'illustrator', 'ui', 'ux', 'communication', 'leadership',
]

DEGREE_PATTERNS = [
    r'\bB\.?\s?Tech\b',
    r'\bM\.?\s?Tech\b',
    r'\bB\.?\s?E\.?\b',
    r'\bM\.?\s?E\.?\b',
    r'\bB\.?\s?Sc\b',
    r'\bM\.?\s?Sc\b',
    r'\bBCA\b',
    r'\bMCA\b',
    r'\bMBA\b',
    r'\bPh\.?\s?D\b',
    r'\bBachelor(?:s)?(?: of [A-Za-z ]+)?\b',
    r'\bMaster(?:s)?(?: of [A-Za-z ]+)?\b',
]


class ResumeParser:
    def __init__(self, resume):
        self.resume = resume

    def get_extracted_data(self):
        text = extract_text(self.resume) or ''
        clean = ' '.join(text.split())
        return {
            'name': self._extract_name(text),
            'email': self._extract_email(clean),
            'mobile_number': self._extract_mobile(clean),
            'skills': self._extract_skills(clean),
            'degree': self._extract_degrees(clean),
            'no_of_pages': self._page_count(),
        }

    def _extract_name(self, text):
        for line in text.splitlines():
            line = line.strip()
            if not line or '@' in line or any(char.isdigit() for char in line):
                continue
            words = line.split()
            if 1 < len(words) <= 4 and all(word[:1].isalpha() for word in words):
                return line
        return os.path.splitext(os.path.basename(self.resume))[0]

    def _extract_email(self, text):
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
        return match.group(0) if match else ''

    def _extract_mobile(self, text):
        match = re.search(r'(?:\+?\d[\s().-]*){10,15}', text)
        return match.group(0).strip() if match else ''

    def _extract_skills(self, text):
        lowered = text.lower()
        found = []
        for skill in COMMON_SKILLS:
            pattern = r'(?<![a-z0-9])' + re.escape(skill.lower()) + r'(?![a-z0-9])'
            if re.search(pattern, lowered):
                found.append(skill.title() if skill not in {'ui', 'ux'} else skill.upper())
        return sorted(set(found))

    def _extract_degrees(self, text):
        degrees = []
        for pattern in DEGREE_PATTERNS:
            degrees.extend(match.group(0) for match in re.finditer(pattern, text, flags=re.IGNORECASE))
        return sorted(set(degrees))

    def _page_count(self):
        try:
            return len(PdfReader(self.resume).pages)
        except Exception:
            return 1
