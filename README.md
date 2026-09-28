#  AI Resume Analyzer

A lightweight resume analysis web app built with **Python and Streamlit**.

It compares a PDF resume with a job description and provides:

- Resume text extraction
- Technical skill detection
- Matched skills
- Missing skills
- Keyword-based match score
- Actionable resume suggestions

##  Features

### Resume Upload
Upload a PDF resume and extract its text automatically.

### Skill Matching
The app detects common technologies and compares them with the skills mentioned in the job description.

### Match Score
A simple estimated score is calculated from:

- 70% recognized skill overlap
- 30% keyword overlap

### Resume Suggestions
The app checks for useful resume sections and suggests improvements.

##  Tech Stack

- Python
- Streamlit
- PyPDF2
- Regular Expressions

##  Project Structure

```text
ai-resume-analyzer/
├── app.py
├── requirements.txt
├── README.md
└── sample_data/
```

##  Run Locally

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

## Disclaimer

This project provides an estimated resume-to-job-description similarity score. It is not an ATS replica and should not be used as a hiring decision system.

## Future Improvements

- LLM-powered resume feedback
- More skill categories
- Experience-level detection
- Job-specific resume suggestions
- Resume section quality scoring
- Cloud deployment
