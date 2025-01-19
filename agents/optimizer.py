from pydantic_ai import Agent
from models.specifications import WebSpecification, OptimizationResult

class Optimizer(Agent):
    def __init__(self, model="claude-3-haiku-20240307"):
        super().__init__(model, result_type=OptimizationResult)
    
    @Agent.tool()
    def optimize_specification(self, spec: WebSpecification, evaluation: EvaluationResult, context: str) -> OptimizationResult:
        """Optimise le cahier des charges en fonction de l'évaluation et du contexte."""
        # Implémentation de la logique d'optimisation
