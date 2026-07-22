import spacy
import re

# Load NLP Model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model... please wait.")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Weak verbs jo ATS pasand nahi karta
WEAK_VERBS = {"worked", "helped", "assisted", "did", "was", "responsible", "handled"}

def analyze_action_verbs(text: str) -> list:
    """
    spaCy use kar ke CV ke sentences check karta hai.
    Agar sentence weak verb se start ho, to usay flag karta hai.
    """
    doc = nlp(text)
    weak_sentences = []
    
    # Text ko sentences mein break karein
    for sent in doc.sents:
        # Punctuation aur extra spaces hata kar pehla word nikalna
        words = [token.text.lower() for token in sent if not token.is_space and not token.is_punct]
        
        if words:
            first_word = words[0]
            if first_word in WEAK_VERBS:
                weak_sentences.append(sent.text.strip())
                
    return weak_sentences

def check_quantifiable_metrics(text: str) -> list:
    """
    Regex use kar ke numbers, percentages (%) aur currency ($) nikalta hai.
    """
    # Regex pattern: 15%, $500, 100+
    metrics_pattern = r'(\d+%)|(\$\d+[kKmM]?)|(\d+\+?)'
    matches = re.findall(metrics_pattern, text)
    
    # Findall tuples return karta hai, usko clean list mein convert karna
    found_metrics = [item for sublist in matches for item in sublist if item]
    
    return found_metrics

def extract_skills_from_jd(cv_text: str, jd_skills: list) -> dict:
    """
    Job description (JD) ki skills ko CV mein dhoondta hai.
    """
    cv_text_lower = cv_text.lower()
    found_skills = []
    missing_skills = []
    
    for skill in jd_skills:
        if skill.lower() in cv_text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    return {"found": found_skills, "missing": missing_skills}

def generate_feedback_report(cv_text: str, jd_skills: list) -> dict:
    """
    Sab functions ko combine kar ke final feedback dictionary banata hai.
    """
    weak_verbs = analyze_action_verbs(cv_text)
    metrics = check_quantifiable_metrics(cv_text)
    skills_match = extract_skills_from_jd(cv_text, jd_skills)
    
    report = {
        "metrics_found": len(metrics) > 0,
        "total_metrics_detected": metrics,
        "weak_bullet_points": weak_verbs,
        "skills_matched": skills_match["found"],
        "skills_missing": skills_match["missing"]
    }
    return report


    