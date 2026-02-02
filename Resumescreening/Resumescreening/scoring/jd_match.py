from sklearn.metrics.pairwise import cosine_similarity

def jd_match_score(resume_vector, jd_vector):
    similarity = cosine_similarity(resume_vector, jd_vector)
    return round(similarity[0][0] * 100, 2)
