import os
import shutil
import tempfile
import streamlit as st

from extractor import generate_feedback_report
from parser import parse_pdf_cv
from scorer import calculate_ats_score

# Page Configuration
st.set_page_config(
    page_title="AI ATS CV Analyzer", page_icon="📄", layout="wide"
)

st.title("📄 AI-Powered ATS CV Analyzer")
st.write(
    "Upload your resume and match it against a Job Description to get an ATS score and detailed feedback."
)

# Sidebar for Job Details Inputs
st.sidebar.header("📝 Job Details")
jd_text = st.sidebar.text_area(
    "Paste Job Description (JD):",
    height=250,
    placeholder="Paste the full job description here...",
)
jd_skills = st.sidebar.text_input(
    "Required Skills (comma-separated):",
    placeholder="Python, FastAPI, Streamlit, SQL, Git",
)

with st.sidebar:
  st.markdown("---")
  st.markdown("### 👨‍💻 Developed By")
  st.markdown("**Rasheed Ahmad**")
  st.markdown("🤖 AI Student @ COMSATS University Islamabad")
  st.markdown("💻 Machine Learning Engineer & Backend Developer(FastAPI)")
  st.markdown("---")

# Main Section for CV Upload
st.header("📤 Upload Resume")
cv_file = st.file_uploader(
    "Upload your CV (PDF format only):", type=["pdf"]
)

# Analysis Trigger Button
if st.button("Analyze CV", type="primary"):
  if not cv_file:
    st.error("Please upload a PDF CV file first!")
  elif not jd_text:
    st.error("Please provide the Job Description!")
  elif not jd_skills:
    st.error("Please provide the required skills!")
  else:
    with st.spinner("Analyzing your CV... Please wait ⏳"):
      # 1. Save uploaded file to a temporary file
      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        shutil.copyfileobj(cv_file, temp_file)
        temp_file_path = temp_file.name

      try:
        # 2. Module 1: Extract Text from PDF
        cv_text = parse_pdf_cv(temp_file_path)

        # Check if PDF parsing failed
        if "Error" in cv_text or "Warning" in cv_text:
          st.error(cv_text)
        else:
          # 3. Convert JD skills string to list
          skills_list = [
              skill.strip() for skill in jd_skills.split(",") if skill.strip()
          ]

          # 4. Module 2: Extractor Report
          feedback_report = generate_feedback_report(cv_text, skills_list)

          # 5. Module 3: Scorer Percentage
          ats_score = calculate_ats_score(cv_text, jd_text)

          # 6. Display Results
          st.success("Analysis Complete!")
          st.markdown("---")

          # Metrics Dashboard Layout
          col1, col2 = st.columns(2)
          with col1:
            st.metric(label="🎯 ATS Match Score", value=f"{ats_score}%")
          with col2:
            st.metric(label="📁 Analyzed File", value=cv_file.name)

          st.markdown("### 📊 Detailed Feedback Report")

          if isinstance(feedback_report, dict):
            matched_skills = feedback_report.get("skills_matched", [])
            missing_skills = feedback_report.get("skills_missing", [])

            with st.container(border=True):
              st.markdown("### 🎯 Skills Breakdown")
              sub_col1, sub_col2 = st.columns(2)

              with sub_col1:
                st.markdown("#### ✅ Matched Skills")
                if matched_skills:
                  for skill in matched_skills:
                    st.markdown(f"- {skill}")
                else:
                  st.markdown("*No matching skills found.*")

              with sub_col2:
                st.markdown("#### ❌ Missing Skills")
                if missing_skills:
                  for skill in missing_skills:
                    st.markdown(f"- {skill}")
                else:
                  st.markdown("*No missing skills! Great job.*")
          else:
            st.markdown(feedback_report)

      except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

      finally:
        # 7. Cleanup temporary file from memory
        if os.path.exists(temp_file_path):
          os.remove(temp_file_path)
