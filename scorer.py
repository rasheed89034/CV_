from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


print("Loading all-MiniLM-L6-v2 model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_ats_score(cv_text: str, jd_text: str) -> float:
    """
    CV aur JD ko mathematical vectors mein convert kar ke unka Match Score nikalta hai.
    """
    # Agar dono mein se koi text khali hai to 0% return karo
    if not cv_text.strip() or not jd_text.strip():
        return 0.0
        
    # AI Model CV aur JD ko "Embeddings" (numbers) mein convert karta hai
    embeddings = model.encode([cv_text, jd_text])
    
    cv_vector = embeddings[0].reshape(1, -1)
    jd_vector = embeddings[1].reshape(1, -1)
    
    
    similarity = cosine_similarity(cv_vector, jd_vector)[0][0]
    
    match_percentage = round(similarity * 100, 2)
    

    return float(max(0.0, match_percentage))