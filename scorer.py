from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_ats_score(cv_text: str, jd_text: str) -> float:
    
    if not cv_text.strip() or not jd_text.strip():
        return 0.0

    embeddings = model.encode([cv_text, jd_text])
    
    cv_vector = embeddings[0].reshape(1, -1)
    jd_vector = embeddings[1].reshape(1, -1)
    
    
    similarity = cosine_similarity(cv_vector, jd_vector)[0][0]
    
    match_percentage = round(similarity * 100, 2)
    

    return float(max(0.0, match_percentage))
