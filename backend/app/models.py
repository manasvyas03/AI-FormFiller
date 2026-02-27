# app/models.py
from pydantic import BaseModel
from typing import List, Dict, Any

class UploadResponse(BaseModel):
    form_id: str
    fields: List[str]

class GenerateQuestionsRequest(BaseModel):
    form_id: str
    language: str
    fields: List[str]

class Question(BaseModel):
    id: str
    field_name: str
    question_text: str

class GenerateQuestionsResponse(BaseModel):
    questions: List[Question]

class SubmitAnswersRequest(BaseModel):
    form_id: str
    answers: Dict[str, str]  # key = question.id

class AnnotatedField(BaseModel):
    field_name: str
    value: str
    x: int
    y: int

class AnnotatedFormResponse(BaseModel):
    form_id: str
    annotated_fields: List[AnnotatedField]
