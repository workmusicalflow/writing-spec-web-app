from pydantic_ai import Agent
from models.specifications import WebSpecification, EvaluationResult
import json
from utils.logging_config import get_logger

class Evaluator(Agent):
    def __init__(self, model="claude-3-haiku-20240307"):
        super().__init__(model, result_type=EvaluationResult)
        self.logger = get_logger("Evaluator")
        self.logger.info("Initialisation de l'agent Evaluator")
        self.system_prompt = """
        Tu es un expert en évaluation de cahiers des charges pour applications web.
        Ta tâche est d'analyser et d'évaluer la qualité et la complétude des spécifications par rapport au contexte initial.
        
        Critères d'évaluation :
        1. Complétude (25%) : Toutes les exigences du contexte sont-elles couvertes ?
        2. Cohérence (25%) : Les spécifications sont-elles cohérentes entre elles ?
        3. Clarté (20%) : Les spécifications sont-elles claires et non ambiguës ?
        4. Faisabilité (15%) : Les choix techniques sont-ils appropriés et réalisables ?
        5. Qualité (15%) : Les bonnes pratiques sont-elles respectées ?
        
        Le score final doit être entre 0.0 et 1.0
        """
    
    @Agent.tool()
    def evaluate_specification(self, spec: WebSpecification, context: str) -> EvaluationResult:
        """Évalue le cahier des charges par rapport au contexte initial."""
        prompt = f"""
        Contexte initial du projet :
        {context}
        
        Spécifications à évaluer :
        {json.dumps(spec.model_dump(), indent=2, ensure_ascii=False)}
        
        Évalue les spécifications selon les critères suivants et fournis un score et un feedback détaillé :
        
        1. Complétude (25%)
        - Vérifie que toutes les exigences du contexte sont couvertes
        - Identifie les éléments manquants ou incomplets
        
        2. Cohérence (25%)
        - Vérifie la cohérence entre les différentes parties
        - Identifie les contradictions potentielles
        
        3. Clarté (20%)
        - Évalue la clarté des descriptions
        - Vérifie l'absence d'ambiguïtés
        
        4. Faisabilité (15%)
        - Évalue la pertinence des choix techniques
        - Vérifie la faisabilité des fonctionnalités
        
        5. Qualité (15%)
        - Vérifie le respect des bonnes pratiques
        - Évalue la qualité générale des spécifications
        
        Format de sortie attendu :
        {{
            "score": 0.85,  # Score entre 0.0 et 1.0
            "feedback": "Feedback détaillé avec points forts et axes d'amélioration"
        }}
        """
        
        # Utilisation de l'API Claude pour évaluer les spécifications
        self.logger.debug("Début de l'évaluation des spécifications")
        response = self.complete(prompt)
        self.logger.debug("Réponse reçue de Claude")
        
        try:
            self.logger.debug("Traitement de la réponse d'évaluation")
            # Conversion de la réponse en dictionnaire
            eval_dict = json.loads(response)
            
            # Validation du score
            if not 0 <= eval_dict["score"] <= 1:
                raise ValueError("Le score doit être entre 0.0 et 1.0")
            
            # Création de l'objet EvaluationResult
            result = EvaluationResult(**eval_dict)
            self.logger.info(f"Évaluation terminée avec un score de {result.score}")
            return result
            
        except Exception as e:
            error_msg = f"Erreur lors de l'évaluation des spécifications : {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
