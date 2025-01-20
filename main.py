import gradio as gr
import json
from agents.specification_writer import SpecificationWriter
from agents.evaluator import Evaluator
from agents.optimizer import Optimizer
from utils.context_manager import ContextManager
from pydantic_ai import RunContext
from typing import Dict, Any, Tuple

# Initialisation du ContextManager partagé
context_manager = ContextManager()

# Initialisation des agents avec le même ContextManager
writer = SpecificationWriter(context_manager=context_manager)
evaluator = Evaluator(context_manager=context_manager)
optimizer = Optimizer(context_manager=context_manager)

def format_evaluation_result(evaluation) -> str:
    """Formate le résultat de l'évaluation pour l'affichage."""
    return f"""
### Scores d'évaluation

- Score total : {evaluation.total_score:.2f}
- Complétude : {evaluation.criteria.completeness:.1f}/100
- Cohérence : {evaluation.criteria.coherence:.1f}/100
- Faisabilité : {evaluation.criteria.feasibility:.1f}/100
- Clarté : {evaluation.criteria.clarity:.1f}/100

### Points forts
{chr(10).join(f"- {point}" for point in evaluation.feedback["strengths"])}

### Points à améliorer
{chr(10).join(f"- {point}" for point in evaluation.feedback["weaknesses"])}

### Aspects techniques
{chr(10).join(f"- {point}" for point in evaluation.feedback["technical"])}

### Aspects fonctionnels
{chr(10).join(f"- {point}" for point in evaluation.feedback["functional"])}
"""

def format_optimization_changes(optimization) -> str:
    """Formate les changements d'optimisation pour l'affichage."""
    if not optimization:
        return "Aucune optimisation nécessaire"
    
    changes = [
        f"### Modification {i+1}\n"
        f"- Champ : {change.field_path}\n"
        f"- Avant : {change.previous_value}\n"
        f"- Après : {change.new_value}\n"
        f"- Raison : {change.reason}\n"
        for i, change in enumerate(optimization.changes_made)
    ]
    return f"""
## Optimisations effectuées

Score après optimisation : {optimization.optimization_score:.2f}

{"".join(changes)}
"""

def generate_specification(user_input: str) -> Tuple[str, str, str]:
    """Génère et optimise les spécifications avec retour détaillé."""
    # Stockage du contexte utilisateur
    context_manager.set_user_input(user_input)
    context = context_manager.get_user_input()
    
    # Génération des spécifications initiales
    run_context = RunContext(value=context)
    spec = writer.write_specification(run_context)
    
    # Évaluation des spécifications
    evaluation = evaluator.evaluate_specification(spec, run_context)
    eval_text = format_evaluation_result(evaluation)
    
    # Optimisation si nécessaire
    optimization = None
    if evaluation.total_score < 0.9:
        optimization = optimizer.optimize_specification(spec, evaluation, run_context)
        opt_text = format_optimization_changes(optimization)
        final_spec = optimization.improved_specification
    else:
        opt_text = "Aucune optimisation nécessaire (score > 0.9)"
        final_spec = spec
    
    # Formatage du résultat final
    spec_json = json.dumps(
        final_spec.model_dump(exclude={"metadata"}),
        indent=2,
        ensure_ascii=False
    )
    
    return spec_json, eval_text, opt_text

# Interface Gradio
iface = gr.Interface(
    fn=generate_specification,
    inputs=[
        gr.Textbox(
            lines=10,
            label="Description du projet",
            placeholder="Décrivez votre projet web en détail..."
        )
    ],
    outputs=[
        gr.JSON(label="Cahier des charges"),
        gr.Markdown(label="Évaluation"),
        gr.Markdown(label="Optimisations")
    ],
    title="Générateur de cahier des charges pour applications web",
    description="""
    Entrez les détails de votre projet web pour obtenir un cahier des charges optimisé.
    Le système analysera votre demande, générera des spécifications détaillées,
    les évaluera selon plusieurs critères et les optimisera si nécessaire.
    """,
    allow_flagging="never",
    theme="default"
)

if __name__ == "__main__":
    iface.launch()
