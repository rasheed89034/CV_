# from fastapi import FastAPI, UploadFile, File, Form
# import shutil
# import os

# # Apne banaye hue custom modules import kar rahe hain
# from parser import parse_pdf_cv
# from extractor import generate_feedback_report
# from scorer import calculate_ats_score

# app = FastAPI(title="ATS CV Analyzer API", version="1.0")

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware # Yeh line add karein
# from parser import parse_pdf_cv
# from extractor import generate_feedback_report
# from scorer import calculate_ats_score

# app = FastAPI()

# # Yeh CORS configuration add karein taa ke HTML frontend API ko call kar sake
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], # For development
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     return {"message": "ATS API is running perfectly!"}

# @app.post("/analyze-cv/")
# async def analyze_cv(
#     cv_file: UploadFile = File(...),
#     jd_text: str = Form(...),
#     jd_skills: str = Form(...)  # Comma separated skills e.g., "Python, FastAPI, Machine Learning"
# ):
#     # 1. PDF file ko temporarily save karna (Kyunke pdfplumber ko file path chahiye hota hai)
#     temp_file_path = f"temp_{cv_file.filename}"
#     with open(temp_file_path, "wb") as buffer:
#         shutil.copyfileobj(cv_file.file, buffer)
        
#     try:
#         # 2. Module 1: Extract Text
#         cv_text = parse_pdf_cv(temp_file_path)
        
#         # Agar PDF format kharab hai ya scan image hai
#         if "Error" in cv_text or "Warning" in cv_text:
#             return {"status": "error", "message": cv_text}
            
#         # 3. JD skills string ko list mein convert karna (e.g., "Python, Java" -> ["Python", "Java"])
#         skills_list = [skill.strip() for skill in jd_skills.split(",") if skill.strip()]
        
#         # 4. Module 2: Extractor (Weak verbs, metrics, skills mapping)
#         feedback_report = generate_feedback_report(cv_text, skills_list)
        
#         # 5. Module 3: Scorer (AI Similarity Percentage)
#         ats_score = calculate_ats_score(cv_text, jd_text)
        
#         # 6. Final JSON Response jo aapki app ko milega
#         final_result = {
#             "status": "success",
#             "file_name": cv_file.filename,
#             "ats_match_percentage": ats_score,
#             "feedback": feedback_report
#         }
#         return final_result
        
#     finally:
#         # 7. Cleanup: Processing ke baad system ki memory free karne ke liye file delete kar dein
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)



# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import shutil  # <-- Yeh zaroori hai file save karne ke liye
# import os      # <-- Yeh zaroori hai temp file delete karne ke liye

# from parser import parse_pdf_cv
# from extractor import generate_feedback_report
# from scorer import calculate_ats_score

# app = FastAPI()

# # CORS configuration taa ke HTML frontend API ko call kar sake
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     return {"message": "ATS API is running perfectly!"}

# @app.post("/analyze-cv/")
# async def analyze_cv(
#     cv_file: UploadFile = File(...),
#     jd_text: str = Form(...),
#     jd_skills: str = Form(...)  
# ):
#     # 1. PDF file ko temporarily save karna
#     temp_file_path = f"temp_{cv_file.filename}"
#     with open(temp_file_path, "wb") as buffer:
#         shutil.copyfileobj(cv_file.file, buffer)
        
#     try:
#         # 2. Module 1: Extract Text
#         cv_text = parse_pdf_cv(temp_file_path)
        
#         # Agar PDF format kharab hai ya scan image hai
#         if "Error" in cv_text or "Warning" in cv_text:
#             return {"status": "error", "message": cv_text}
            
#         # 3. JD skills string ko list mein convert karna
#         skills_list = [skill.strip() for skill in jd_skills.split(",") if skill.strip()]
        
#         # 4. Module 2: Extractor (Weak verbs, metrics, skills mapping)
#         feedback_report = generate_feedback_report(cv_text, skills_list)
        
#         # 5. Module 3: Scorer (AI Similarity Percentage)
#         ats_score = calculate_ats_score(cv_text, jd_text)
        
#         # 6. Final JSON Response
#         final_result = {
#             "status": "success",
#             "file_name": cv_file.filename,
#             "ats_match_percentage": ats_score,
#             "feedback": feedback_report
#         }
#         return final_result
        
#     finally:
#         # 7. Cleanup: Memory free karne ke liye file delete kar dein
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)


from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import tempfile  # <-- Yeh library add karni hai

from parser import parse_pdf_cv
from extractor import generate_feedback_report
from scorer import calculate_ats_score

app = FastAPI()

# CORS configuration taa ke HTML frontend API ko call kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ATS API is running perfectly!"}

@app.post("/analyze-cv/")
async def analyze_cv(
    cv_file: UploadFile = File(...),
    jd_text: str = Form(...),
    jd_skills: str = Form(...)  
):
    # 1. File ko system ke hidden temp folder mein save karna (Taake live server reload na ho)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        shutil.copyfileobj(cv_file.file, temp_file)
        temp_file_path = temp_file.name
        
    try:
        # 2. Module 1: Extract Text
        cv_text = parse_pdf_cv(temp_file_path)
        
        # Agar PDF format kharab hai ya scan image hai
        if "Error" in cv_text or "Warning" in cv_text:
            return {"status": "error", "message": cv_text}
            
        # 3. JD skills string ko list mein convert karna
        skills_list = [skill.strip() for skill in jd_skills.split(",") if skill.strip()]
        
        # 4. Module 2: Extractor (Weak verbs, metrics, skills mapping)
        feedback_report = generate_feedback_report(cv_text, skills_list)
        
        # 5. Module 3: Scorer (AI Similarity Percentage)
        ats_score = calculate_ats_score(cv_text, jd_text)
        
        # 6. Final JSON Response
        final_result = {
            "status": "success",
            "file_name": cv_file.filename,
            "ats_match_percentage": ats_score,
            "feedback": feedback_report
        }
        return final_result
        
    finally:
        # 7. Cleanup: Memory free karne ke liye temporary file delete kar dein
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)