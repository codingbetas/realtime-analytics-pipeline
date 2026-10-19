import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Notice the +psycopg2 at the end of postgresql
DATABASE_URL = "postgresql+psycopg2://metrics_user:metrics_password@localhost:5433/metrics_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class MetricLog(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    total_events = Column(Integer, default=0)
    total_amount = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()