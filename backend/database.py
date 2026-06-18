from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///database/ats.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class ResumeHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    score = Column(Float)
    jd_score = Column(Float)
    roles = Column(String)


Base.metadata.create_all(engine)