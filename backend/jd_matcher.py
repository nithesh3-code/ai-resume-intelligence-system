from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match(resume, jd):
    tfidf = TfidfVectorizer()
    mat = tfidf.fit_transform([resume, jd])

    score = cosine_similarity(mat[0:1], mat[1:2])[0][0]

    return round(score * 100, 2)