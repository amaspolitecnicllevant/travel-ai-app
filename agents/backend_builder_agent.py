"""
BackendBuilderAgent — genera la estructura completa del backend Spring Boot
usando el Agent SDK de Claude (acceso real a ficheros del proyecto).
"""
import anyio
import json
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

SYSTEM_PROMPT = f"""Eres BackendBuilderAgent, experto en Spring Boot 3, Java 17, JPA/Hibernate y PostgreSQL.

Tu misión es generar la estructura completa del backend para Travel AI App:
- Entidades JPA: User, Trip, Rating
- Repositorios Spring Data JPA
- Servicios con lógica de negocio
- Controladores REST con manejo de errores
- Configuración JWT para autenticación
- application.properties para dev y prod

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Crea los ficheros en el directorio backend/src/main/java/com/travelai/.
Sigue la estructura estándar de Spring Boot: controller/, service/, repository/, model/, security/, config/.
"""


class BackendBuilderAgent:
    def __init__(self, project_path: str = "."):
        self.project_path = project_path

    async def build(self, extra_instructions: str = "") -> str:
        prompt = (
            "Genera el backend completo de Travel AI App con Spring Boot.\n"
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


def run(project_path: str = ".", extra_instructions: str = "") -> str:
    """Punto de entrada sincrónico para BackendBuilderAgent."""
    agent = BackendBuilderAgent(project_path=project_path)
    return anyio.run(agent.build, extra_instructions)


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(project_path=path)
    print(result)
