import re
import io
import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

SKILLS = {
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "HTML", "CSS",
    "React", "Next.js", "Node.js", "Express", "Flutter", "Dart",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Git", "GitHub",
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Generative AI", "LLM", "Data Analysis", "Data Science",
    "AWS", "Azure", "Docker", "Kubernetes", "REST API", "FastAPI",
    "Django", "Flask", "Streamlit", "Power BI", "Tableau"
}

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def normalize(text):
    return re.sub(r"[^a-z0-9+#.\s]", " ", text.lower())

def extract_skills(text):
    normalized = normalize(text)
    found = []
    for skill in sorted(SKILLS, key=len, reverse=True):
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))

def keyword_tokens(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", text.lower())
    stop = {
        "the","and","for","with","that","this","from","have","has","are",
        "you","your","our","will","job","role","work","using","years",
        "experience","required","requirements","responsibilities"
    }
    return {w for w in words if w not in stop}

def analyze(resume, jd):
    resume_skills = set(extract_skills(resume))
    jd_skills = set(extract_skills(jd))
    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    jd_words = keyword_tokens(jd)
    resume_words = keyword_tokens(resume)
    keyword_match = len(jd_words & resume_words) / max(len(jd_words), 1)

    skill_match = len(matched) / max(len(jd_skills), 1)
    score = round((skill_match * 70) + (keyword_match * 30), 1)

    return matched, missing, score

def suggestions(missing, resume):
    tips = []
    if missing:
        tips.append("Consider adding relevant missing skills only if you genuinely have experience with them.")
    if len(resume.split()) < 150:
        tips.append("Your resume appears short. Add measurable project outcomes, responsibilities, and technical details.")
    if not re.search(r"\b(project|projects)\b", resume, re.I):
        tips.append("Add a Projects section with your contribution and measurable results.")
    if not re.search(r"\b(github|linkedin)\b", resume, re.I):
        tips.append("Add relevant professional links such as GitHub or LinkedIn.")
    tips.append("Use numbers where possible: reduced time by 30%, processed 10K records, built 5 features, etc.")
    return tips

st.title(" AI Resume Analyzer")
st.caption("Compare a resume with a job description using skill and keyword matching.")

with st.sidebar:
    st.header("About")
    st.write("A lightweight NLP-style resume screening tool built with Python and Streamlit.")
    st.info("This score is an estimate, not a hiring decision.")

uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

resume_text = ""
if uploaded:
    try:
        resume_text = extract_pdf_text(uploaded)
        st.success("Resume loaded successfully.")
    except Exception as e:
        st.error(f"Could not read the PDF: {e}")

jd = st.text_area(
    "Paste the Job Description",
    height=260,
    placeholder="Paste the complete job description here..."
)

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if not resume_text:
        st.warning("Please upload a readable PDF resume.")
    elif not jd.strip():
        st.warning("Please paste a job description.")
    else:
        matched, missing, score = analyze(resume_text, jd)

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Match Score", f"{score}%")
        c2.metric("Matched Skills", len(matched))
        c3.metric("Missing Skills", len(missing))

        st.subheader(" Matched Skills")
        st.write(", ".join(matched) if matched else "No recognized matching skills found.")

        st.subheader("Skills Mentioned in JD but Not Found")
        st.write(", ".join(missing) if missing else "No recognized missing skills.")

        st.subheader("Suggestions")
        for tip in suggestions(missing, resume_text):
            st.write(f"- {tip}")

        with st.expander("View Extracted Resume Text"):
            st.text(resume_text[:12000])

st.divider()
st.caption("Built with Python • Streamlit • PyPDF2 • Regex")
