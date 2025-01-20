from __future__ import annotations
from pydantic_ai import Agent, RunContext
from models.specifications import (
    VersionedWebSpecification,
    WebSpecification,
    EvaluationResult,
    OptimizationResult,
    OptimizationChange,
    PageSection,
    TechStackCategory,
    VersionMetadata,
    ModificationType
)
from utils.context_manager import ContextManager
from typing import Optional, Dict, Any
from datetime import datetime
import json
from utils.logging_config import get_logger

class Optimizer(Agent):
    def __init__(self, model="claude-3-haiku-20240307", context_manager: Optional[ContextManager] = None):
        super().__init__(model, result_type=OptimizationResult)
        self.context_manager = context_manager or ContextManager()
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
        
        # Enregistrement de l'outil optimize_specification
        self.tool(self.optimize_specification)
    
    def optimize_specification(self, spec: VersionedWebSpecification, evaluation: EvaluationResult, context: RunContext[str]) -> OptimizationResult:
        """Optimise le cahier des charges en fonction de l'évaluation et du contexte."""
        prompt = f"""
        Contexte initial du projet :
        {context.value}
        
        Spécifications actuelles :
        {json.dumps(spec.model_dump(), indent=2, ensure_ascii=False)}
        
        Évaluation reçue :
        Score total : {evaluation.total_score}
        Scores détaillés :
        - Complétude : {evaluation.criteria.completeness}
        - Cohérence : {evaluation.criteria.coherence}
        - Faisabilité : {evaluation.criteria.feasibility}
        - Clarté : {evaluation.criteria.clarity}
        
        Feedback :
        Points forts : {json.dumps(evaluation.feedback["strengths"], indent=2, ensure_ascii=False)}
        Points faibles : {json.dumps(evaluation.feedback["weaknesses"], indent=2, ensure_ascii=False)}
        Aspects techniques : {json.dumps(evaluation.feedback["technical"], indent=2, ensure_ascii=False)}
        Aspects fonctionnels : {json.dumps(evaluation.feedback["functional"], indent=2, ensure_ascii=False)}
        
        Suggestions d'amélioration :
        {json.dumps(evaluation.improvement_suggestions, indent=2, ensure_ascii=False)}
        
        Optimise les spécifications en tenant compte du feedback et génère une réponse au format JSON suivant :
        {{
            "improved_specification": {{
                // Structure complète WebSpecification avec les améliorations
            }},
            "changes": [
                {{
                    "field_path": "chemin.vers.le.champ",
                    "previous_value": "ancienne valeur",
                    "new_value": "nouvelle valeur",
                    "reason": "Justification du changement"
                }}
            ],
            "optimization_score": 0.95  // Score estimé après optimisation
        }}
        
        Assure-toi que :
        1. Les modifications répondent directement aux points soulevés dans l'évaluation
        2. Les améliorations sont concrètes et mesurables
        3. La cohérence globale est maintenue
        4. Les changements sont clairement documentés
        """
        
        # Utilisation de l'API Claude pour optimiser les spécifications
        self.logger.debug(f"Début de l'optimisation des spécifications (score actuel: {evaluation.total_score})")
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
            
            # Stockage de la nouvelle version dans le ContextManager
            new_version_id = self.context_manager.store_specification_version(
                specification_data=improved_spec,
                agent_name="Optimizer",
                action_type="optimization",
                parent_id=spec.metadata.version_id
            )
            
            # Création des métadonnées de version
            metadata = VersionMetadata(
                version_id=new_version_id,
                parent_version_id=spec.metadata.version_id,
                agent_name="Optimizer",
                modification_type=ModificationType.OPTIMIZATION,
                timestamp=datetime.utcnow(),
                comment=f"Optimisation basée sur l'évaluation (score initial: {evaluation.total_score})"
            )
            
            # Création de la spécification versionnée améliorée
            improved_spec_obj = VersionedWebSpecification(
                **WebSpecification(**improved_spec).dict(),
                metadata=metadata
            )
            
            # Création de l'objet OptimizationResult
            result = OptimizationResult(
                original_version_id=spec.metadata.version_id,
                new_version_id=new_version_id,
                improved_specification=improved_spec_obj,
                changes_made=[OptimizationChange(**change) for change in opt_dict["changes"]],
                optimization_score=opt_dict["optimization_score"],
                optimizer_name="Optimizer",
                timestamp=datetime.utcnow()
            )
            
            self.logger.info(
                f"Optimisation terminée : version {new_version_id}, "
                f"{len(result.changes_made)} modifications, "
                f"score estimé: {result.optimization_score}"
            )
            return result
            
        except Exception as e:
            error_msg = f"Erreur lors de l'optimisation des spécifications : {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
