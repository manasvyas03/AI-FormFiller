# app/annotation.py
from typing import List, Dict
from .models import AnnotatedField

def generate_annotations(form_id: str, answers: Dict[str, str], questions_map: Dict[str, str]) -> List[AnnotatedField]:
    """
    For v1: hard-code coordinates for fields on one specific form.
    questions_map: question_id -> field_name
    """
    layout = {
        "Full Name": (100, 150),
        "Date of Birth": (100, 200),
        "Address": (100, 250),
        "Mobile Number": (100, 300),
        "Email": (100, 350),
    }

    annotated = []
    for q_id, value in answers.items():
        field_name = questions_map.get(q_id)
        if not field_name:
            continue
        if field_name in layout:
            x, y = layout[field_name]
            annotated.append(
                AnnotatedField(
                    field_name=field_name,
                    value=value,
                    x=x,
                    y=y
                )
            )
    return annotated
