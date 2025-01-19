from pydantic import BaseModel
from typing import List

class WebSpecification(BaseModel):
    project_name: str
    description: str
    pages: List[str]
    features: List[str]
    tech_stack: dict

class EvaluationResult(BaseModel):
    score: float
    feedback: str

class OptimizationResult(BaseModel):
    improved_specification: WebSpecification
    changes_made: List[str]
