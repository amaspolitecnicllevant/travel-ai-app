"""
Travel AI App — Orquestador principal
Todos los agentes y skills disponibles sin endpoints ficticios.

Uso:
    python main.py                        # ejecuta todo el setup inicial
    python main.py --only backend         # genera backend Spring Boot
    python main.py --only frontend        # genera frontend Vue 3 completo
    python main.py --only vue-components  # genera componentes Vue específicos
    python main.py --only itinerary       # genera itinerario de prueba (París 5 días)
    python main.py --only docker          # genera infraestructura Docker
    python main.py --only cicd            # genera pipeline CI/CD GitHub Actions
    python main.py --only db              # genera scripts SQL y migraciones Flyway
    python main.py --only demo            # demo de todos los agentes IA
"""
import argparse
import json
import os
import anyio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


# ──────────────────────────────────────────────
# Pasos de construcción (Agent SDK — crea ficheros)
# ──────────────────────────────────────────────

def step_backend():
    print("\n[1] Generando backend Spring Boot con BackendBuilderAgent...")
    from agents.backend_builder_agent import run as build_backend
    result = build_backend(project_path=str(PROJECT_ROOT))
    print(f"[OK] Backend generado:\n{result[:200]}...")


def step_frontend():
    print("\n[2] Generando frontend Vue 3 con FrontendBuilderAgent...")
    from agents.frontend_builder_agent import run as build_frontend
    result = build_frontend(project_path=str(PROJECT_ROOT), api_url="http://localhost:8080/api")
    print(f"[OK] Frontend generado:\n{result[:200]}...")


def step_vue_components():
    print("\n[3] Generando componentes Vue con FrontendVueAgent...")
    from agents.frontend_vue_agent import FrontendVueAgent

    async def _run():
        agent = FrontendVueAgent(project_path=str(PROJECT_ROOT))
        r1 = await agent.create_itinerary_components()
        print(f"[OK] Componentes de itinerario: {r1[:100]}...")
        r2 = await agent.create_trip_components()
        print(f"[OK] Componentes de viaje: {r2[:100]}...")

    anyio.run(_run)


def step_docker():
    print("\n[4] Generando infraestructura Docker con DevOpsAgent...")
    from agents.devops_agent import DevOpsAgent

    async def _run():
        agent = DevOpsAgent(project_path=str(PROJECT_ROOT))
        result = await agent.setup_docker(environment="dev")
        print(f"[OK] Docker configurado: {result[:100]}...")

    anyio.run(_run)


def step_cicd():
    print("\n[5] Generando CI/CD con DevOpsAgent...")
    from agents.devops_agent import DevOpsAgent

    async def _run():
        agent = DevOpsAgent(project_path=str(PROJECT_ROOT))
        result = await agent.setup_cicd()
        print(f"[OK] CI/CD generado: {result[:100]}...")

    anyio.run(_run)


def step_db():
    print("\n[6] Generando scripts de base de datos con DevOpsAgent...")
    from agents.devops_agent import DevOpsAgent

    async def _run():
        agent = DevOpsAgent(project_path=str(PROJECT_ROOT))
        result = await agent.setup_db_scripts()
        print(f"[OK] Scripts BD generados: {result[:100]}...")

    anyio.run(_run)


# ──────────────────────────────────────────────
# Demo de agentes IA (Claude API — sin ficheros)
# ──────────────────────────────────────────────

def step_itinerary():
    print("\n[Demo] TravelPlannerAgent — París 5 días...")
    from agents.travel_planner_agent import TravelPlannerAgent
    agent = TravelPlannerAgent()
    itinerary = agent.generate_itinerary(destination="París", days=5, trip_type="cultural")
    out = PROJECT_ROOT / "travel-ai-app" / "itinerary_paris.json"
    agent.save_itinerary(itinerary, str(out))
    print(f"[OK] Itinerario: {out}")


def step_demo():
    print("\n=== DEMO de todos los agentes IA ===\n")

    # TravelPlannerAgent
    print("[TravelPlannerAgent] Generando itinerario Tokio 4 días...")
    from agents.travel_planner_agent import TravelPlannerAgent
    planner = TravelPlannerAgent()
    itinerary = planner.generate_itinerary(destination="Tokio", days=4, trip_type="cultural")
    print(f"  Destino: {itinerary.get('destination')}, días: {len(itinerary.get('days', []))}")

    # EditorAgent
    print("\n[EditorAgent] Editando itinerario...")
    from agents.editor_agent import EditorAgent
    editor = EditorAgent()
    editor.load_itinerary(itinerary)
    updated = editor.edit("Añade más experiencias gastronómicas en el día 2.")
    print(f"  Actividades día 2: {len(updated['days'][1]['activities'])}")

    # BudgetAgent
    print("\n[BudgetAgent] Calculando presupuesto Tokio 4 días...")
    from agents.budget_agent import BudgetAgent
    budget_agent = BudgetAgent()
    budget = budget_agent.estimate_budget(destination="Tokio", days=4, travelers=2)
    print(f"  Presupuesto total: {budget.get('total_estimate_eur')}€")

    # ExperienceAgent
    print("\n[ExperienceAgent] Recomendando experiencias en Tokio...")
    from agents.experience_agent import ExperienceAgent
    exp_agent = ExperienceAgent()
    experiences = exp_agent.recommend_experiences(
        destination="Tokio", traveler_profile="cultural", days=4
    )
    print(f"  Experiencias recomendadas: {len(experiences.get('experiences', []))}")

    # PromptEngineerAgent
    print("\n[PromptEngineerAgent] Mejorando prompt de usuario...")
    from agents.prompt_engineer_agent import PromptEngineerAgent
    pe_agent = PromptEngineerAgent()
    improved = pe_agent.improve_prompt("quiero algo cool en japón unos días")
    print(f"  Prompt mejorado: {improved.get('improved_prompt', '')[:80]}...")

    # SocialAgent
    print("\n[SocialAgent] Generando contenido social...")
    from agents.social_agent import SocialAgent
    social_agent = SocialAgent()
    trip = {"title": "Tokio Cultural", "destination": "Tokio", "type": "cultural", "days": 4}
    content = social_agent.generate_trip_content(trip, itinerary)
    instagram = content.get("platform_content", {}).get("instagram", {})
    print(f"  Instagram caption: {instagram.get('caption', '')[:80]}...")

    # Guardar demo
    demo_output = {
        "itinerary": updated,
        "budget": budget,
        "experiences": experiences,
        "social_content": content,
    }
    out_path = PROJECT_ROOT / "travel-ai-app" / "demo_tokio.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(demo_output, indent=2, ensure_ascii=False))
    print(f"\n[OK] Demo completo guardado en: {out_path}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Travel AI App - Orquestador")
    parser.add_argument(
        "--only",
        choices=["backend", "frontend", "vue-components", "docker", "cicd", "db", "itinerary", "demo"],
        help="Ejecutar solo un paso específico",
    )
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise EnvironmentError(
            "Falta la variable de entorno ANTHROPIC_API_KEY.\n"
            "Configúrala con: export ANTHROPIC_API_KEY=tu_clave"
        )

    steps = {
        "backend": step_backend,
        "frontend": step_frontend,
        "vue-components": step_vue_components,
        "docker": step_docker,
        "cicd": step_cicd,
        "db": step_db,
        "itinerary": step_itinerary,
        "demo": step_demo,
    }

    if args.only:
        steps[args.only]()
    else:
        # Setup completo: infraestructura + código
        for name in ["backend", "frontend", "vue-components", "docker", "cicd", "db"]:
            try:
                steps[name]()
            except Exception as e:
                print(f"[ERROR] Paso '{name}' falló: {e}")

    print("\n[✓] Travel AI App lista.")


if __name__ == "__main__":
    main()
