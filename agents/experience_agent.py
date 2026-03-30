"""
ExperienceAgent — recomienda experiencias, actividades y puntos de interés
usando la Claude API. Personaliza recomendaciones según el perfil del viajero.
"""
import json
import anthropic
from pathlib import Path

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()

SYSTEM_PROMPT = f"""Eres ExperienceAgent, experto en experiencias de viaje únicas y actividades turísticas.

Tu misión es recomendar experiencias auténticas y memorables adaptadas al perfil del viajero.

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Cuando generes recomendaciones, responde en JSON con este formato:
{{
  "destination": "nombre",
  "traveler_profile": "aventurero|cultural|gastronómico|familiar|romántico",
  "experiences": [
    {{
      "name": "nombre de la experiencia",
      "type": "aventura|cultural|gastronómica|naturaleza|ocio_nocturno|bienestar",
      "description": "descripción detallada y atractiva",
      "duration_hours": 3,
      "cost_eur": 45,
      "booking_required": true,
      "best_time": "mañana|tarde|noche|todo_el_día",
      "difficulty": "fácil|moderado|difícil",
      "highlights": ["punto 1", "punto 2"],
      "insider_tip": "consejo de local",
      "rating_estimate": 4.8
    }}
  ],
  "hidden_gems": ["experiencia oculta 1", "experiencia oculta 2"],
  "avoid": ["trampa turística 1", "trampa turística 2"]
}}

Responde ÚNICAMENTE con el JSON, sin texto adicional.
"""


class ExperienceAgent:
    def __init__(self):
        self.conversation_history = []

    def recommend_experiences(
        self,
        destination: str,
        traveler_profile: str = "cultural",
        days: int = 5,
        interests: list[str] | None = None,
    ) -> dict:
        """Genera recomendaciones de experiencias personalizadas."""
        interests_str = ", ".join(interests) if interests else "variados"
        prompt = (
            f"Recomienda las mejores experiencias en {destination} para un viajero {traveler_profile}.\n"
            f"Duración del viaje: {days} días\n"
            f"Intereses específicos: {interests_str}\n"
            "Incluye experiencias auténticas y evita las trampas turísticas."
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

    def get_day_experiences(self, destination: str, day_theme: str, budget_eur: float = 100) -> dict:
        """Genera actividades para un día específico con un tema y presupuesto."""
        prompt = (
            f"Diseña un día completo de experiencias en {destination} con temática '{day_theme}'.\n"
            f"Presupuesto máximo: {budget_eur}€ por persona\n"
            "Organiza las actividades por horario para que fluyan naturalmente."
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

    def filter_by_rating(self, experiences: dict, min_rating: float = 4.5) -> list:
        """Filtra experiencias por valoración mínima."""
        return [
            exp for exp in experiences.get("experiences", [])
            if exp.get("rating_estimate", 0) >= min_rating
        ]


if __name__ == "__main__":
    agent = ExperienceAgent()
    result = agent.recommend_experiences(
        destination="Kioto",
        traveler_profile="cultural",
        days=4,
        interests=["templos", "gastronomía", "tradiciones japonesas"],
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
