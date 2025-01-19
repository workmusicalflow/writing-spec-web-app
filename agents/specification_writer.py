from pydantic_ai import Agent
from models.specifications import WebSpecification

class SpecificationWriter(Agent):
    def __init__(self, model="claude-3-haiku-20240307"):
        super().__init__(model, result_type=WebSpecification)
    
    @Agent.tool()
    def write_specification(self, context: str) -> WebSpecification:
        """Écrit un cahier des charges basé sur le contexte fourni."""
        # Implémentation de la logique de rédaction
