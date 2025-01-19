from pydantic_ai import Agent
from models.specifications import WebSpecification, EvaluationResult

class Evaluator(Agent):
    def __init__(self, model="claude-3-haiku-20240307"):
        super().__init__(model, result_type=EvaluationResult)
    
    @Agent.tool()
    def evaluate_specification(self, spec: WebSpecification, context: str) -> EvaluationResult:
        """Évalue le cahier des charges par rapport au contexte initial."""
        # Implémentation de la logique d'évaluation
