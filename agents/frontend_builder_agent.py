"""
FrontendBuilderAgent — genera la estructura completa del frontend Vue 3
usando el Agent SDK de Claude (acceso real a ficheros del proyecto).
"""
import anyio
import json
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

SYSTEM_PROMPT = f"""Eres FrontendBuilderAgent, experto en Vue 3, TypeScript, Pinia, Vue Router y Tailwind CSS.

Tu misión es generar la estructura completa del frontend para Travel AI App:
- Vistas: LoginView, RegisterView, DashboardView, TripDetailView, CreateTripView
- Stores Pinia: authStore, tripsStore, itineraryStore
- Componentes reutilizables: TripCard, ItineraryDay, PromptEditor, RatingStars
- Configuración de Axios con interceptores JWT
- Rutas con Vue Router (con guards de autenticación)
- Layout principal con navbar

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Crea los ficheros en el directorio frontend/src/.
Estructura: views/, components/, stores/, router/, services/, composables/.
Usa <script setup lang="ts"> en todos los componentes.
"""


class FrontendBuilderAgent:
    def __init__(self, project_path: str = ".", api_url: str = "http://localhost:8080/api"):
        self.project_path = project_path
        self.api_url = api_url

    async def build(self, extra_instructions: str = "") -> str:
        prompt = (
            f"Genera el frontend completo de Travel AI App con Vue 3.\n"
            f"La API REST está en: {self.api_url}\n"
            "Crea todos los ficheros necesarios directamente en el sistema de archivos.\n"
        )
        if extra_instructions:
            prompt += f"\nInstrucciones adicionales: {extra_instructions}"

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=40,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text


def run(project_path: str = ".", api_url: str = "http://localhost:8080/api", extra_instructions: str = "") -> str:
    """Punto de entrada sincrónico para FrontendBuilderAgent."""
    agent = FrontendBuilderAgent(project_path=project_path, api_url=api_url)
    return anyio.run(agent.build, extra_instructions)


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(project_path=path)
    print(result)
