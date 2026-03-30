"""
PromptEngineerAgent — mejora los prompts del usuario para obtener mejores
itinerarios y experiencias. Transforma instrucciones vagas en prompts efectivos.
"""
import json
import anthropic
from pathlib import Path

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()

SYSTEM_PROMPT = f"""Eres PromptEngineerAgent, experto en prompt engineering aplicado a planificación de viajes.

Tu misión es:
1. Mejorar prompts vagos del usuario en instrucciones claras y detalladas
2. Extraer intención real detrás de peticiones ambiguas
3. Sugerir prompts alternativos para explorar opciones
4. Validar que los prompts producirán resultados útiles para la app

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Cuando mejores un prompt, responde en JSON con este formato:
{{
  "original_prompt": "...",
  "analysis": "qué intenta conseguir el usuario",
  "improved_prompt": "prompt mejorado y detallado",
  "alternatives": [
    "alternativa más específica",
    "alternativa más creativa",
    "alternativa más práctica"
  ],
  "parameters_extracted": {{
    "destination": "si se menciona",
    "days": null,
    "budget": "si se menciona",
    "trip_type": "cultural|aventura|relax|etc",
    "special_requirements": []
  }},
  "tips_for_user": "consejo para que el usuario haga mejores prompts en el futuro"
}}

Responde ÚNICAMENTE con el JSON, sin texto adicional.
"""


class PromptEngineerAgent:
    def improve_prompt(self, user_prompt: str, context: str = "") -> dict:
        """Mejora un prompt del usuario para generar mejores itinerarios."""
        prompt = (
            f"Mejora este prompt de usuario para Travel AI App:\n\n"
            f"'{user_prompt}'\n\n"
            + (f"Contexto adicional: {context}\n\n" if context else "")
            + "Analiza la intención y genera una versión mejorada con alternativas."
        )

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=2048,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            final = stream.get_final_message()

        return json.loads(next(b.text for b in final.content if b.type == "text"))

    def validate_edit_prompt(self, edit_prompt: str, current_itinerary: dict) -> dict:
        """Valida y mejora un prompt de edición de itinerario."""
        prompt = (
            f"El usuario quiere editar su itinerario con esta instrucción:\n"
            f"'{edit_prompt}'\n\n"
            f"Itinerario actual (resumen):\n"
            f"Destino: {current_itinerary.get('destination')}, "
            f"Días: {len(current_itinerary.get('days', []))}, "
            f"Tipo: {current_itinerary.get('type')}\n\n"
            "¿Es el prompt claro y ejecutable? Mejóralo si es necesario."
        )

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=2048,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            final = stream.get_final_message()

        return json.loads(next(b.text for b in final.content if b.type == "text"))

    def suggest_prompts_for_destination(self, destination: str, trip_type: str = "cultural") -> list[str]:
        """Sugiere prompts populares para un destino específico."""
        prompt = (
            f"Sugiere 5 prompts creativos y útiles que los usuarios podrían usar "
            f"para personalizar su itinerario de viaje {trip_type} a {destination}.\n"
            "Que sean variados: gastronomía, cultura, aventura, ocio nocturno, descanso."
        )

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=1024,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            final = stream.get_final_message()

        result = json.loads(next(b.text for b in final.content if b.type == "text"))
        return result.get("alternatives", [])


if __name__ == "__main__":
    agent = PromptEngineerAgent()
    result = agent.improve_prompt("quiero algo chulo en madrid unos días")
    print(json.dumps(result, indent=2, ensure_ascii=False))
