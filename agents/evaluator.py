from __future__ import annotations
from pydantic_ai import Agent, RunContext
from models.specifications import (
    VersionedWebSpecification,
    EvaluationResult,
    EvaluationCriteria,
    DependencyContext,
    ModificationType
)
from utils.context_manager import ContextManager
from typing import Optional
import json
from utils.logging_config import get_logger

class Evaluator(Agent):
    def __init__(self, model="claude-3-haiku-20240307", context_manager: Optional[ContextManager] = None):
        super().__init__(
            model,
            result_type=EvaluationResult,
            deps_type=str
        )
        self.context_manager = context_manager or ContextManager()
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
        
        # Enregistrement de l'outil evaluate_specification
        self.tool(self.evaluate_specification)
    
    def evaluate_specification(self, context: RunContext[str], spec: VersionedWebSpecification) -> EvaluationResult:
        """Évalue le cahier des charges par rapport au contexte initial."""
        prompt = f"""
        Contexte initial du projet :
        {context.value}
        
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
            "criteria": {{
                "completeness": 85.0,  # Score entre 0 et 100
                "coherence": 90.0,
                "feasibility": 75.0,
                "clarity": 80.0
            }},
            "total_score": 0.85,  # Moyenne pondérée des critères
            "feedback": {{
                "strengths": ["Point fort 1", "Point fort 2"],
                "weaknesses": ["Point faible 1", "Point faible 2"],
                "technical": ["Commentaire technique 1", "Commentaire technique 2"],
                "functional": ["Commentaire fonctionnel 1", "Commentaire fonctionnel 2"]
            }},
            "improvement_suggestions": [
                "Suggestion d'amélioration 1",
                "Suggestion d'amélioration 2"
            ]
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
            
            # Validation des scores
            if not all(0 <= score <= 100 for score in eval_dict["criteria"].values()):
                raise ValueError("Les scores des critères doivent être entre 0 et 100")
            if not 0 <= eval_dict["total_score"] <= 1:
                raise ValueError("Le score total doit être entre 0.0 et 1.0")
            
            # Création de l'objet EvaluationResult
            result = EvaluationResult(
                specification_version=spec.metadata.version_id,
                criteria=EvaluationCriteria(**eval_dict["criteria"]),
                total_score=eval_dict["total_score"],
                feedback=eval_dict["feedback"],
                evaluator_name="Evaluator",
                improvement_suggestions=eval_dict["improvement_suggestions"]
            )
            
            # Enregistrement du résultat dans le ContextManager
            self.context_manager.store_specification_version(
                specification_data=result.dict(),
                agent_name="Evaluator",
                action_type="evaluation",
                parent_id=spec.metadata.version_id
            )
            
            # Enregistrement de la dépendance avec l'Optimizer si le score est inférieur à 0.9
            if result.total_score < 0.9:
                self.context_manager.register_agent_dependency(
                    source_agent="Evaluator",
                    target_agent="Optimizer",
                    context_data=DependencyContext(
                        source_version_id=spec.metadata.version_id,
                        target_agent="Optimizer",
                        context_type="optimization_request",
                        data={
                            "specification_id": spec.metadata.version_id,
                            "evaluation_feedback": result.dict()
                        },
                        priority=2
                    ).dict()
                )
            
            self.logger.info(f"Évaluation terminée avec un score de {result.total_score}")
            return result
            
        except Exception as e:
            error_msg = f"Erreur lors de l'évaluation des spécifications : {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
