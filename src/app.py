import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .assistants.classifier import classify_lead_with_llm
from .assistants.extractor import extract_info_with_llm
from .assistants.editor import edit_note_with_llm
from .assistants.risk_assessor import assess_risk_with_llm

from .assistants.extractor import ExtractedInfo
from .assistants.risk_assessor import RiskAssessment
from .assistants.classifier import LeadText as ClassifierLeadText
from .assistants.extractor import LeadText as ExtractorLeadText
from .assistants.editor import LeadText as EditorLeadText
from .assistants.risk_assessor import NoteText as RiskAssessorNoteText

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(
    title="AI CRM Assistant Service",
    description="API для AI-ассистента, который автоматизирует рутинные задачи в CRM.",
    version="0.1.0"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify")
async def classify_lead(lead: ClassifierLeadText):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")
    return classify_lead_with_llm(lead.text, API_KEY)

@app.post("/extract-info", response_model=ExtractedInfo)
async def extract_info(lead: ExtractorLeadText):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")
    return extract_info_with_llm(lead.text, API_KEY)

@app.post("/edit-note")
async def edit_note(note: EditorLeadText):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")
    return edit_note_with_llm(note.text, API_KEY)

@app.post("/risk-assessment", response_model=RiskAssessment)
async def assess_risk(note: RiskAssessorNoteText):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")
    return assess_risk_with_llm(note.text, API_KEY)
