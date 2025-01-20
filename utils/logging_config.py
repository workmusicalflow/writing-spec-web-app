import logging
import os
from datetime import datetime
from pathlib import Path

class AgentLogger:
    def __init__(self):
        # Création du dossier logs s'il n'existe pas
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configuration du logger principal
        self.logger = logging.getLogger("agent_workflow")
        self.logger.setLevel(logging.DEBUG)
        
        # Formatter pour les logs
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Handler pour les fichiers de log quotidiens
        daily_file = log_dir / f"agent_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(daily_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler pour la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Ajout des handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_agent_logger(self, agent_name: str) -> logging.Logger:
        """Crée un logger spécifique pour un agent."""
        logger = self.logger.getChild(agent_name)
        return logger

# Instance globale du logger
agent_logger = AgentLogger()

def get_logger(agent_name: str) -> logging.Logger:
    """Fonction utilitaire pour obtenir un logger pour un agent."""
    return agent_logger.get_agent_logger(agent_name)
