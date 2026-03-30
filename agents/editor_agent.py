"""
EditorAgent — edita itinerarios de viaje existentes usando prompts en lenguaje natural.
Permite modificaciones precisas sin regenerar todo el itinerario.
"""
import json
import anthropic
from pathlib import Path

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()

SYSTEM_PROMPT = f"""Eres EditorAgent, especialista en editar y mejorar itinerarios de viaje existentes.

Tu misión es aplicar modificaciones precisas a itinerarios JSON usando instrucciones en lenguaje natural.
Preserva la estructura y el resto del contenido. Solo modifica lo que se te pide.

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

El formato del itinerario es:
{{
  "destination": "...",
  "type": "...",
  "days": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "activities": [
        {{
          "time": "09:00",
          "name": "...",
          "type": "visita|comida|transporte|alojamiento|ocio",
          "description": "...",
          "duration_minutes": 90,
          "cost_estimate_eur": 15,
          "location": "...",
          "tips": "..."
        }}
      ]
    }}
  ],
  "budget_estimate_eur": 1200,
  "tips": []
}}

Responde ÚNICAMENTE con el JSON completo y actualizado, sin texto adicional.
"""


class EditorAgent:
    def __init__(self):
        self.current_itinerary: dict | None = None
        self.edit_history: list[str] = []

    def load_itinerary(self, itinerary: dict) -> None:
        """Carga un itinerario para editarlo."""
        self.current_itinerary = itinerary
        self.edit_history = []

    def load_from_file(self, file_path: str) -> dict:
        """Carga un itinerario desde un fichero JSON."""
        with open(file_path, encoding="utf-8") as f:
            self.current_itinerary = json.load(f)
        self.edit_history = []
        return self.current_itinerary

    def edit(self, instruction: str) -> dict:
        """Aplica una modificación al itinerario usando lenguaje natural."""
        if not self.current_itinerary:
            raise ValueError("No hay itinerario cargado. Llama primero a load_itinerary().")

        prompt = (
            f"Aquí está el itinerario actual:\n\n"
            f"```json\n{json.dumps(self.current_itinerary, indent=2, ensure_ascii=False)}\n```\n\n"
            f"Instrucción de edición: {instruction}\n\n"
            "Devuelve el itinerario completo y actualizado en JSON."
        )

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=8192,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            final = stream.get_final_message()

        text = next(b.text for b in final.content if b.type == "text")
        self.current_itinerary = json.loads(text)
        self.edit_history.append(instruction)
        return self.current_itinerary

    def add_activity(self, day: int, activity: dict) -> dict:
        """Añade una actividad a un día específico."""
        return self.edit(
            f"Añade esta actividad al día {day}: {json.dumps(activity, ensure_ascii=False)}. "
            "Insértala en el horario de forma coherente."
        )

    def remove_activity(self, day: int, activity_name: str) -> dict:
        """Elimina una actividad por nombre."""
        return self.edit(f"Elimina la actividad '{activity_name}' del día {day}.")

    def change_day_theme(self, day: int, new_theme: str) -> dict:
        """Cambia el tema/enfoque de un día completo."""
        return self.edit(
            f"Reorganiza completamente el día {day} con el tema: '{new_theme}'. "
            "Sustituye las actividades actuales por otras que encajen con este nuevo tema."
        )

    def save(self, output_path: str) -> None:
        """Guarda el itinerario editado."""
        if not self.current_itinerary:
            raise ValueError("No hay itinerario para guardar.")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.current_itinerary, f, indent=2, ensure_ascii=False)
        print(f"[OK] Itinerario guardado en: {output_path}")

    def get_edit_history(self) -> list[str]:
        return self.edit_history


if __name__ == "__main__":
    # Ejemplo de uso
    sample_itinerary = {
        "destination": "Roma",
        "type": "cultural",
        "days": [
            {
                "day": 1,
                "date": "2025-06-01",
                "activities": [
                    {
                        "time": "09:00",
                        "name": "Coliseo",
                        "type": "visita",
                        "description": "Visita al anfiteatro romano",
                        "duration_minutes": 120,
                        "cost_estimate_eur": 16,
                        "location": "Piazza del Colosseo",
                        "tips": "Compra entradas online"
                    }
                ]
            }
        ],
        "budget_estimate_eur": 800,
        "tips": []
    }

    editor = EditorAgent()
    editor.load_itinerary(sample_itinerary)
    updated = editor.edit("Añade una cena en restaurante de cocina italiana tradicional al final del día 1.")
    print(json.dumps(updated, indent=2, ensure_ascii=False))
