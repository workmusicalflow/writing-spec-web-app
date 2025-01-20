from pydantic_ai import Agent
from models.specifications import WebSpecification, PageSection, TechStackCategory
from typing import Dict, List
import json
from utils.logging_config import get_logger

class SpecificationWriter(Agent):
    def __init__(self, model="claude-3-haiku-20240307"):
        super().__init__(model, result_type=WebSpecification)
        self.logger = get_logger("SpecificationWriter")
        self.logger.info("Initialisation de l'agent SpecificationWriter")
        self.system_prompt = """
        Tu es un expert en rédaction de cahiers des charges pour applications web.
        Ta tâche est d'analyser le contexte fourni et de générer des spécifications détaillées et structurées.
        
        Directives importantes :
        1. Analyse en profondeur le contexte pour identifier tous les éléments clés
        2. Structure les spécifications de manière claire et exhaustive
        3. Assure-toi que chaque page et fonctionnalité est bien détaillée
        4. Propose une stack technique adaptée aux besoins
        5. Inclus les aspects de performance, sécurité et accessibilité si pertinents
        
        Format de sortie : JSON structuré selon le modèle WebSpecification
        """
    
    @Agent.tool()
    def write_specification(self, context: str) -> WebSpecification:
        """Écrit un cahier des charges détaillé basé sur le contexte fourni."""
        prompt = f"""
        Contexte du projet :
        {context}
        
        Génère un cahier des charges complet au format JSON avec la structure suivante :
        {{
            "project_name": "Nom du projet",
            "description": "Description détaillée",
            "target_audience": "Public cible",
            "pages": {{
                "page_name": {{
                    "name": "Nom de la page",
                    "description": "Description de la page",
                    "components": ["Liste des composants"],
                    "dynamic_elements": ["Éléments dynamiques"],
                    "interactions": ["Interactions utilisateur"]
                }}
            }},
            "features": ["Liste des fonctionnalités"],
            "tech_stack": {{
                "frontend": ["Technologies frontend"],
                "backend": ["Technologies backend"],
                "database": ["Technologies base de données"],
                "testing": ["Outils de test"],
                "deployment": ["Outils de déploiement"]
            }},
            "responsive_design": true,
            "performance_requirements": {{"critère": "valeur"}},
            "security_requirements": ["Exigences de sécurité"],
            "seo_requirements": ["Exigences SEO"],
            "accessibility_requirements": ["Exigences d'accessibilité"]
        }}
        
        Assure-toi que la sortie est un JSON valide et respecte exactement cette structure.
        """
        
        # Utilisation de l'API Claude pour générer les spécifications
        self.logger.debug(f"Génération des spécifications pour le contexte : {context[:100]}...")
        response = self.complete(prompt)
        self.logger.debug("Réponse reçue de Claude")
        
        try:
            self.logger.debug("Traitement de la réponse")
            # Conversion de la réponse en dictionnaire
            spec_dict = json.loads(response)
            
            # Conversion des pages en objets PageSection
            pages_dict = {}
            for page_name, page_data in spec_dict["pages"].items():
                pages_dict[page_name] = PageSection(**page_data)
            
            # Mise à jour du dictionnaire avec les pages converties
            spec_dict["pages"] = pages_dict
            
            # Conversion du tech_stack en utilisant l'énumération
            tech_stack_dict = {}
            for category, technologies in spec_dict["tech_stack"].items():
                tech_stack_dict[TechStackCategory(category)] = technologies
            spec_dict["tech_stack"] = tech_stack_dict
            
            # Création de l'objet WebSpecification
            spec = WebSpecification(**spec_dict)
            self.logger.info("Spécifications générées avec succès")
            return spec
            
        except Exception as e:
            error_msg = f"Erreur lors de la génération des spécifications : {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
