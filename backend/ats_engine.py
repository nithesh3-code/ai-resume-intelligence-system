import re

def clean(text):
    return re.sub(r"[^a-zA-Z0-9+.# ]", " ", text.lower())


def analyze(text):
    text = clean(text)

    skills = {
        "python": 20,
        "machine learning": 25,
        "deep learning": 25,
        "ai": 15,
        "data science": 25,
        "sql": 15,
        "nlp": 20,
        "tensorflow": 25,
        "pandas": 10,
        "numpy": 10
    }

    found = []
    score = 0

    for s, w in skills.items():
        if s in text:
            found.append(s)
            score += w

    score = min(score, 100)

    roles = (
        ["Senior AI Engineer", "ML Engineer"] if score > 80 else
        ["AI Developer", "Data Analyst"] if score > 50 else
        ["Junior Dev"] if score > 30 else
        ["Intern"]
    )

    missing = list(set(skills.keys()) - set(found))

    return score, roles, found, missing