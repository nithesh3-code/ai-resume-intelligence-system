from fastapi import FastAPI
from pydantic import BaseModel

from backend.ats_engine import analyze
from backend.jd_matcher import match
from backend.database import Session, ResumeHistory

app = FastAPI()


class ResumeInput(BaseModel):
    text: str
    jd: str = ""


@app.post("/analyze")
def analyze_resume(data: ResumeInput):

    score, roles, found, missing = analyze(data.text)

    jd_score = 0
    if data.jd:
        jd_score = match(data.text, data.jd)

    db = Session()
    record = ResumeHistory(
        score=score,
        jd_score=jd_score,
        roles=",".join(roles)
    )
    db.add(record)
    db.commit()

    return {
        "ats_score": score,
        "jd_score": jd_score,
        "roles": roles,
        "skills": found,
        "missing": missing
    }


@app.get("/history")
def history():
    db = Session()
    data = db.query(ResumeHistory).all()

    return [
        {
            "score": d.score,
            "jd_score": d.jd_score,
            "roles": d.roles
        }
        for d in data
    ]