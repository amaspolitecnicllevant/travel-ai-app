"""
SocialAgent — gestiona el contenido social de los viajes: genera descripciones
para compartir, responde a valoraciones y crea contenido para redes sociales.
"""
import json
import anthropic
from pathlib import Path

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()

SYSTEM_PROMPT = f"""Eres SocialAgent, experto en comunicación digital, redes sociales y narrativa de viajes.

Tu misión es generar contenido atractivo y auténtico para compartir experiencias de viaje:
- Descripciones de viajes para la plataforma
- Posts para Instagram, Twitter/X y Facebook
- Respuestas a valoraciones de otros usuarios
- Hashtags relevantes y trending

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Cuando generes contenido social, responde en JSON con este formato:
{{
  "platform_content": {{
    "app_description": "descripción completa para la plataforma (200-400 chars)",
    "instagram": {{
      "caption": "texto del post con emojis",
      "hashtags": ["#viaje", "#travel", "#destino"],
      "story_text": "texto corto para story"
    }},
    "twitter": {{
      "tweet": "tweet de máximo 280 chars",
      "thread": ["tweet 1", "tweet 2", "tweet 3"]
    }},
    "facebook": {{
      "post": "post largo y descriptivo"
    }}
  }},
  "rating_response": "respuesta a valoración si aplica",
  "seo_keywords": ["keyword1", "keyword2"]
}}

Responde ÚNICAMENTE con el JSON, sin texto adicional.
"""


class SocialAgent:
    def generate_trip_content(self, trip: dict, itinerary: dict | None = None) -> dict:
        """Genera contenido social completo para un viaje."""
        context = f"Información del viaje:\n{json.dumps(trip, ensure_ascii=False)}"
        if itinerary:
            context += f"\n\nItinerario:\n{json.dumps(itinerary, ensure_ascii=False)}"

        prompt = (
            f"{context}\n\n"
            "Genera contenido atractivo para compartir este viaje en todas las plataformas."
        )

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            final = stream.get_final_message()

        return json.loads(next(b.text for b in final.content if b.type == "text"))

    def respond_to_rating(self, trip: dict, rating: dict) -> str:
        """Genera una respuesta personalizada a una valoración recibida."""
        prompt = (
            f"Viaje: {json.dumps(trip, ensure_ascii=False)}\n"
            f"Valoración recibida (score: {rating.get('score')}/5): "
            f"{rating.get('comment', 'sin comentario')}\n\n"
            "Genera una respuesta agradecida y personalizada para esta valoración."
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
        return result.get("rating_response", "")

    def generate_hashtags(self, destination: str, trip_type: str, activities: list[str]) -> list[str]:
        """Genera hashtags optimizados para un viaje."""
        prompt = (
            f"Genera los mejores hashtags para un viaje {trip_type} a {destination}.\n"
            f"Actividades principales: {', '.join(activities)}\n"
            "Mezcla hashtags populares, de nicho y en español e inglés."
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
        return result.get("platform_content", {}).get("instagram", {}).get("hashtags", [])


if __name__ == "__main__":
    agent = SocialAgent()
    trip = {"title": "Aventura en Bali", "destination": "Bali", "type": "aventura", "days": 7}
    content = agent.generate_trip_content(trip)
    print(json.dumps(content, indent=2, ensure_ascii=False))
