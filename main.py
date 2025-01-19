import gradio as gr
from agents.specification_writer import SpecificationWriter
from agents.evaluator import Evaluator
from agents.optimizer import Optimizer
from utils.context_manager import ContextManager

context_manager = ContextManager()
writer = SpecificationWriter()
evaluator = Evaluator()
optimizer = Optimizer()

def generate_specification(user_input):
    context_manager.set_user_input(user_input)
    spec = writer.write_specification(context_manager.get_user_input())
    evaluation = evaluator.evaluate_specification(spec, context_manager.get_user_input())
    
    if evaluation.score < 0.8:  # Seuil arbitraire pour l'optimisation
        optimization = optimizer.optimize_specification(spec, evaluation, context_manager.get_user_input())
        return optimization.improved_specification.model_dump_json(indent=2)
    
    return spec.model_dump_json(indent=2)

iface = gr.Interface(
    fn=generate_specification,
    inputs=gr.Textbox(lines=10, label="Description du projet"),
    outputs=gr.JSON(label="Cahier des charges"),
    title="Générateur de cahier des charges pour applications web",
    description="Entrez les détails de votre projet web pour obtenir un cahier des charges optimisé."
)

if __name__ == "__main__":
    iface.launch()
