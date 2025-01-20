from pydantic_ai import Agent
from models.specifications import WebSpecification, EvaluationResult, OptimizationResult, PageSection, TechStackCategory
import json
from utils.logging_config import get_logger

class Optimizer(Agent):
    def __init__(self, model="claude-3-haiku-20240307"):
        super().__init__(model, result_type=OptimizationResult)
        self.logger = get_logger("Optimizer")
        self.logger.info("Initialisation de l'agent Optimizer")
        self.system_prompt = """
        Tu es un expert en optimisation de cahiers des charges pour applications web.
        Ta tâche est d'améliorer les spécifications en fonction de l'évaluation reçue et du contexte initial.
        
        Directives d'optimisation :
        1. Analyse le feedback de l'évaluation pour identifier les points faibles
        2. Propose des améliorations concrètes et justifiées
        3. Maintiens la cohérence avec le contexte initial
        4. Assure-toi que les modifications apportent une réelle valeur ajoutée
        5. Documente clairement les changements effectués
        
        Format de sortie : JSON structuré selon le modèle OptimizationResult
        """
    
    @Agent.tool()
    def optimize_specification(self, spec: WebSpecification, evaluation: EvaluationResult, context: str) -> OptimizationResult:
        """Optimise le cahier des charges en fonction de l'évaluation et du contexte."""
        prompt = f"""
        Contexte initial du projet :
        {context}
        
        Spécifications actuelles :
        {json.dumps(spec.model_dump(), indent=2, ensure_ascii=False)}
        
        Évaluation reçue :
        Score : {evaluation.score}
        Feedback : {evaluation.feedback}
        
        Optimise les spécifications en tenant compte du feedback et génère une réponse au format JSON suivant :
        {{
            "improved_specification": {{
                // Structure complète WebSpecification avec les améliorations
            }},
            "changes_made": [
                "Liste détaillée des modifications apportées"
            ]
        }}
        
        Assure-toi que :
        1. Les modifications répondent directement aux points soulevés dans l'évaluation
        2. Les améliorations sont concrètes et mesurables
        3. La cohérence globale est maintenue
        4. Les changements sont clairement documentés
        """
        
        # Utilisation de l'API Claude pour optimiser les spécifications
        self.logger.debug(f"Début de l'optimisation des spécifications (score actuel: {evaluation.score})")
        response = self.complete(prompt)
        self.logger.debug("Réponse reçue de Claude")
        
        try:
            self.logger.debug("Traitement de la réponse d'optimisation")
            # Conversion de la réponse en dictionnaire
            opt_dict = json.loads(response)
            
            # Conversion des pages en objets PageSection dans la spécification améliorée
            improved_spec = opt_dict["improved_specification"]
            pages_dict = {}
            for page_name, page_data in improved_spec["pages"].items():
                pages_dict[page_name] = PageSection(**page_data)
            improved_spec["pages"] = pages_dict
            
            # Conversion du tech_stack en utilisant l'énumération
            tech_stack_dict = {}
            for category, technologies in improved_spec["tech_stack"].items():
                tech_stack_dict[TechStackCategory(category)] = technologies
            improved_spec["tech_stack"] = tech_stack_dict
            
            # Création de l'objet WebSpecification amélioré
            improved_spec_obj = WebSpecification(**improved_spec)
            
            # Création de l'objet OptimizationResult
            result = OptimizationResult(
                improved_specification=improved_spec_obj,
                changes_made=opt_dict["changes_made"]
            )
            self.logger.info(f"Optimisation terminée avec {len(result.changes_made)} modifications")
            return result
            
        except Exception as e:
            error_msg = f"Erreur lors de l'optimisation des spécifications : {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
