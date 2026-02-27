# app/main.py
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from .models import (
    UploadResponse,
    GenerateQuestionsRequest,
    GenerateQuestionsResponse,
    Question,
    SubmitAnswersRequest,
    AnnotatedFormResponse
)
from .ocr import extract_text, infer_fields_from_text
from .llm import generate_questions_from_fields
from .annotation import generate_annotations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# simple in-memory store for demo
FORMS: Dict[str, Dict] = {}  # form_id -> {"path": ..., "fields": [...], "questions": [...]}

@app.post("/upload_form", response_model=UploadResponse)
async def upload_form(file: UploadFile = File(...)):
    form_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    save_path = os.path.join(UPLOAD_DIR, f"{form_id}{file_ext}")

    with open(save_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(save_path)
    fields = infer_fields_from_text(text)

    FORMS[form_id] = {
        "path": save_path,
        "fields": fields,
        "questions": []
    }

    return UploadResponse(form_id=form_id, fields=fields)

@app.post("/generate_questions", response_model=GenerateQuestionsResponse)
async def generate_questions(req: GenerateQuestionsRequest):
    if req.form_id not in FORMS:
        raise HTTPException(status_code=404, detail="Form not found")

    questions_raw = generate_questions_from_fields(req.fields, req.language)

    questions = []
    for item in questions_raw:
        q_id = item.get("id") or str(uuid.uuid4())
        q = Question(
            id=q_id,
            field_name=item.get("field_name", ""),
            question_text=item.get("question_text", "")
        )
        questions.append(q)

    FORMS[req.form_id]["questions"] = [q.dict() for q in questions]
    return GenerateQuestionsResponse(questions=questions)

@app.post("/submit_answers", response_model=AnnotatedFormResponse)
async def submit_answers(req: SubmitAnswersRequest):
    if req.form_id not in FORMS:
        raise HTTPException(status_code=404, detail="Form not found")

    form_data = FORMS[req.form_id]
    questions = form_data.get("questions", [])

    questions_map = {q["id"]: q["field_name"] for q in questions}
    annotated_fields = generate_annotations(req.form_id, req.answers, questions_map)

    return AnnotatedFormResponse(
        form_id=req.form_id,
        annotated_fields=annotated_fields
    )
