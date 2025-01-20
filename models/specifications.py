from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class PageSection(BaseModel):
    name: str
    description: str
    components: List[str]
    dynamic_elements: Optional[List[str]] = None
    interactions: Optional[List[str]] = None

class TechStackCategory(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    TESTING = "testing"
    DEPLOYMENT = "deployment"

class WebSpecification(BaseModel):
    project_name: str = Field(..., description="Nom du projet web")
    description: str = Field(..., description="Description détaillée du projet")
    target_audience: str = Field(..., description="Public cible du site web")
    pages: Dict[str, PageSection] = Field(..., description="Structure détaillée des pages")
    features: List[str] = Field(..., description="Fonctionnalités principales")
    tech_stack: Dict[TechStackCategory, List[str]] = Field(..., description="Stack technique par catégorie")
    responsive_design: bool = Field(True, description="Support du design responsive")
    performance_requirements: Optional[Dict[str, str]] = Field(None, description="Exigences de performance")
    security_requirements: Optional[List[str]] = Field(None, description="Exigences de sécurité")
    seo_requirements: Optional[List[str]] = Field(None, description="Exigences SEO")
    accessibility_requirements: Optional[List[str]] = Field(None, description="Exigences d'accessibilité")

class EvaluationResult(BaseModel):
    score: float
    feedback: str

class OptimizationResult(BaseModel):
    improved_specification: WebSpecification
    changes_made: List[str]
