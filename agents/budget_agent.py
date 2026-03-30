"""
BudgetAgent — estima y gestiona presupuestos de viaje usando la Claude API.
Calcula costes por categoría, compara opciones y sugiere cómo optimizar el presupuesto.
"""
import json
import anthropic
from pathlib import Path

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()

SYSTEM_PROMPT = f"""Eres BudgetAgent, experto en finanzas de viaje y optimización de presupuestos turísticos.

Tu misión es ayudar a los viajeros a planificar y controlar el presupuesto de sus viajes.

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Cuando generes un desglose de presupuesto, responde en JSON con este formato:
{{
  "destination": "nombre",
  "travelers": 2,
  "days": 5,
  "budget_tier": "económico|medio|premium",
  "total_estimate_eur": 1500,
  "breakdown": {{
    "accommodation": {{"total": 400, "per_night": 80, "options": ["hostal", "hotel 3*"]}},
    "transport": {{"flights": 300, "local": 100, "total": 400}},
    "food": {{"total": 250, "per_day_per_person": 25}},
    "activities": {{"total": 200, "highlights": ["museo", "tour"]}},
    "misc": {{"total": 100, "includes": ["seguros", "souvenirs"]}}
  }},
  "saving_tips": ["consejo 1", "consejo 2"],
  "best_booking_time": "con 2 meses de antelación"
}}

Responde ÚNICAMENTE con el JSON, sin texto adicional.
"""


class BudgetAgent:
    def __init__(self):
        self.conversation_history = []

    def estimate_budget(
        self,
        destination: str,
        days: int,
        travelers: int = 2,
        budget_tier: str = "medio",
    ) -> dict:
        """Genera un desglose de presupuesto detallado para el viaje."""
        prompt = (
            f"Calcula el presupuesto detallado para un viaje a {destination}.\n"
            f"Duración: {days} días\n"
            f"Viajeros: {travelers}\n"
            f"Nivel de presupuesto: {budget_tier}\n"
            "Incluye vuelos, alojamiento, comida, actividades y extras."
        )
        self.conversation_history = [{"role": "user", "content": prompt}]

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=self.conversation_history,
        ) as stream:
            final = stream.get_final_message()

        text = next(b.text for b in final.content if b.type == "text")
        self.conversation_history.append({"role": "assistant", "content": text})
        return json.loads(text)

    def optimize_budget(self, current_budget: dict, max_budget_eur: float) -> dict:
        """Optimiza un presupuesto existente para ajustarlo a un máximo."""
        prompt = (
            f"Tengo este presupuesto:\n{json.dumps(current_budget, ensure_ascii=False)}\n\n"
            f"Necesito ajustarlo a un máximo de {max_budget_eur}€. "
            "¿Cómo puedo reducir costes manteniendo la mejor experiencia posible?"
        )
        self.conversation_history.append({"role": "user", "content": prompt})

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=self.conversation_history,
        ) as stream:
            final = stream.get_final_message()

        text = next(b.text for b in final.content if b.type == "text")
        self.conversation_history.append({"role": "assistant", "content": text})
        return json.loads(text)

    def compare_destinations(self, destinations: list[str], days: int, travelers: int = 2) -> dict:
        """Compara el coste entre varios destinos."""
        prompt = (
            f"Compara el coste de viaje a estos destinos para {travelers} viajeros durante {days} días:\n"
            + "\n".join(f"- {d}" for d in destinations)
            + "\nOrdénalos de más económico a más caro con un resumen de cada uno."
        )
        self.conversation_history = [{"role": "user", "content": prompt}]

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=self.conversation_history,
        ) as stream:
            final = stream.get_final_message()

        text = next(b.text for b in final.content if b.type == "text")
        self.conversation_history.append({"role": "assistant", "content": text})
        return json.loads(text)


if __name__ == "__main__":
    agent = BudgetAgent()
    budget = agent.estimate_budget(destination="Tokio", days=7, travelers=2, budget_tier="medio")
    print(json.dumps(budget, indent=2, ensure_ascii=False))
