"""
DevOpsAgent — gestiona la infraestructura de Travel AI App:
Dockerfiles, docker-compose, CI/CD workflows, scripts de despliegue
y configuración de entornos usando el Agent SDK.
"""
import anyio
import json
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

SYSTEM_PROMPT = f"""Eres DevOpsAgent, experto en Docker, CI/CD con GitHub Actions, y despliegue de aplicaciones Spring Boot + Vue 3.

Tu misión es crear y mantener la infraestructura de Travel AI App:
- Dockerfiles multi-stage optimizados para producción
- docker-compose para dev y prod con PostgreSQL
- Workflows de GitHub Actions para CI/CD completo
- Scripts de inicialización de base de datos
- Configuraciones de entorno (dev/staging/prod)
- Nginx para servir el frontend en producción

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Principios:
- Imágenes Docker lo más ligeras posible (multi-stage builds)
- Secrets nunca hardcodeados (usar variables de entorno)
- Healthchecks en todos los servicios de docker-compose
- CI/CD: lint → test → build → push → deploy
"""


class DevOpsAgent:
    def __init__(self, project_path: str = "."):
        self.project_path = project_path

    async def setup_docker(self, environment: str = "dev") -> str:
        """Genera toda la infraestructura Docker para el entorno indicado."""
        prompt = (
            f"Genera la infraestructura Docker completa para entorno '{environment}':\n\n"
            "1. backend/Dockerfile — multi-stage: Maven build + JRE slim runtime\n"
            "2. frontend/Dockerfile — multi-stage: Node build + Nginx serve\n"
            "3. frontend/nginx.conf — configuración Nginx con proxy a API y SPA routing\n"
            f"4. docker-compose.yml — con backend, frontend, PostgreSQL 15"
            + (" y pgAdmin" if environment == "dev" else " sin pgAdmin")
            + "\n5. .env.example — todas las variables de entorno necesarias\n\n"
            "Incluye healthchecks, restart policies y redes Docker correctamente configuradas."
        )

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=25,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text

    async def setup_cicd(self) -> str:
        """Genera el pipeline completo de CI/CD con GitHub Actions."""
        prompt = (
            "Genera el pipeline CI/CD completo en .github/workflows/:\n\n"
            "1. ci.yml — se ejecuta en cada PR:\n"
            "   - Lint y tests del backend (Maven + JUnit)\n"
            "   - Lint y tests del frontend (ESLint + Vitest)\n"
            "   - Build de imágenes Docker\n\n"
            "2. cd.yml — se ejecuta en push a main:\n"
            "   - Build y push de imágenes a Docker Hub o GitHub Container Registry\n"
            "   - Deploy automático (docker-compose pull && docker-compose up -d)\n\n"
            "3. db-migrate.yml — ejecución manual para migraciones de BD con Flyway\n\n"
            "Usa secrets de GitHub para credenciales. Incluye caché de dependencias Maven y npm."
        )

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=20,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text

    async def setup_db_scripts(self) -> str:
        """Genera scripts de inicialización y migración de la base de datos."""
        prompt = (
            "Genera los scripts SQL de inicialización de la base de datos en scripts/db/:\n\n"
            "1. 01_init_schema.sql — creación de tablas (users, trips, ratings, itineraries)\n"
            "2. 02_init_data.sql — datos de prueba (3 usuarios, 5 viajes, itinerarios de ejemplo)\n"
            "3. 03_indexes.sql — índices para optimizar las queries más frecuentes\n\n"
            "También genera backend/src/main/resources/db/migration/ con scripts Flyway:\n"
            "- V1__create_tables.sql\n"
            "- V2__add_sample_data.sql"
        )

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=20,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text

    async def setup_full_infrastructure(self) -> str:
        """Configura toda la infraestructura de una vez."""
        results = []
        for task_name, coro in [
            ("Docker", self.setup_docker()),
            ("CI/CD", self.setup_cicd()),
            ("DB Scripts", self.setup_db_scripts()),
        ]:
            print(f"  → Generando {task_name}...")
            result = await coro
            results.append(f"[{task_name}] {result[:100]}...")

        return "\n".join(results)


def run_docker(project_path: str = ".", environment: str = "dev") -> str:
    agent = DevOpsAgent(project_path=project_path)
    return anyio.run(agent.setup_docker, environment)


def run_cicd(project_path: str = ".") -> str:
    agent = DevOpsAgent(project_path=project_path)
    return anyio.run(agent.setup_cicd)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    agent = DevOpsAgent(project_path=path)
    result = anyio.run(agent.setup_full_infrastructure)
    print(result)
