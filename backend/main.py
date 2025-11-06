from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class QuoteDB(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    customer = Column(String)
    contract_type = Column(String)
    amount = Column(Float)

Base.metadata.create_all(bind=engine)

class Quote(BaseModel):
    customer: str
    contract_type: str
    amount: float

@app.post("/quotes")
def create(quote: Quote):
    db = SessionLocal()
    db_quote = QuoteDB(**quote.dict())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    db.close()
    return db_quote

@app.get("/quotes")
def read():
    db = SessionLocal()
    quotes = db.query(QuoteDB).all()
    db.close()
    return [{"id": q.id, "customer": q.customer, "contract_type": q.contract_type, "amount": q.amount} for q in quotes]

@app.get("/")
def health():
    return {"status": "ERP LIVE - Clermont, FL"}
