"""
TravelPlannerAgent — genera itinerarios de viaje inteligentes usando la Claude API.
Soporta generación inicial y edición mediante prompts en lenguaje natural.
"""
import json
import anthropic
from pathlib import Path

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()

SYSTEM_PROMPT = f"""Eres TravelPlannerAgent, un experto en planificación de viajes con amplio conocimiento
de destinos turísticos, cultura, gastronomía y logística de viajes.

Tu misión es generar itinerarios de viaje detallados en formato JSON estructurado.

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

El formato de itinerario que debes producir es:
{{
  "destination": "nombre del destino",
  "type": "cultural|aventura|relax|gastronómico|familiar",
  "days": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "activities": [
        {{
          "time": "09:00",
          "name": "nombre de la actividad",
          "type": "visita|comida|transporte|alojamiento|ocio",
          "description": "descripción detallada",
          "duration_minutes": 90,
          "cost_estimate_eur": 15,
          "location": "dirección o área",
          "tips": "consejo útil"
        }}
      ]
    }}
  ],
  "budget_estimate_eur": 1200,
  "best_season": "primavera",
  "tips": ["consejo general 1", "consejo general 2"]
}}

Responde ÚNICAMENTE con el JSON del itinerario, sin texto adicional.
"""


class TravelPlannerAgent:
    def __init__(self):
        self.conversation_history = []

    def generate_itinerary(
        self,
        destination: str,
        days: int,
        trip_type: str = "cultural",
        budget: str = "medio",
        travelers: int = 2,
    ) -> dict:
        """Genera un itinerario inicial para el destino dado."""
        prompt = (
            f"Genera un itinerario de {days} días para {destination}.\n"
            f"Tipo de viaje: {trip_type}\n"
            f"Presupuesto: {budget}\n"
            f"Número de viajeros: {travelers}\n"
            "Incluye actividades variadas para cada día, con tiempos realistas y costes estimados."
        )

        self.conversation_history = [{"role": "user", "content": prompt}]

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=8192,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=self.conversation_history,
        ) as stream:
            final = stream.get_final_message()

        # Guardar respuesta en historial para ediciones posteriores
        assistant_text = next(b.text for b in final.content if b.type == "text")
        self.conversation_history.append({"role": "assistant", "content": assistant_text})

        return json.loads(assistant_text)

    def edit_itinerary(self, edit_prompt: str) -> dict:
        """Edita el itinerario actual usando un prompt en lenguaje natural."""
        if not self.conversation_history:
            raise ValueError("No hay itinerario generado. Llama primero a generate_itinerary().")

        self.conversation_history.append({"role": "user", "content": edit_prompt})

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=8192,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=self.conversation_history,
        ) as stream:
            final = stream.get_final_message()

        assistant_text = next(b.text for b in final.content if b.type == "text")
        self.conversation_history.append({"role": "assistant", "content": assistant_text})

        return json.loads(assistant_text)

    def save_itinerary(self, itinerary: dict, output_path: str) -> None:
        """Guarda el itinerario en un fichero JSON."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(itinerary, f, indent=2, ensure_ascii=False)
        print(f"[OK] Itinerario guardado en: {output_path}")


if __name__ == "__main__":
    agent = TravelPlannerAgent()

    print("Generando itinerario para París...")
    itinerary = agent.generate_itinerary(destination="París", days=5, trip_type="cultural")
    agent.save_itinerary(itinerary, "travel-ai-app/itinerary_paris.json")

    print("\nEditando itinerario: añadir más gastronomía...")
    updated = agent.edit_itinerary(
        "Añade más restaurantes y experiencias gastronómicas locales en cada día."
    )
    agent.save_itinerary(updated, "travel-ai-app/itinerary_paris_v2.json")
    print("Listo.")
