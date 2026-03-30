"""
FrontendVueAgent — especializado en crear componentes Vue 3 específicos de la UI
de Travel AI App usando el Agent SDK (acceso real a ficheros).
Complementa FrontendBuilderAgent con generación a nivel de componente individual.
"""
import anyio
import json
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

SYSTEM_PROMPT = f"""Eres FrontendVueAgent, experto en Vue 3 con Composition API, TypeScript, Pinia y Tailwind CSS.

Tu especialidad es crear componentes Vue 3 de alta calidad para Travel AI App:
- Componentes de itinerario: ItineraryDay, ActivityCard, TimelineView
- Componentes de viaje: TripCard, TripForm, DestinationSearch
- Componentes de UI: PromptEditor, AILoadingIndicator, RatingStars, ShareModal
- Integraciones con Claude API para edición en tiempo real de itinerarios

Contexto de la aplicación:
{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}

Reglas de código:
- Usar siempre <script setup lang="ts">
- Props tipadas con defineProps<{{...}}>()
- Emits tipados con defineEmits<{{...}}>()
- Tailwind CSS para todos los estilos (sin CSS personalizado salvo animaciones)
- Composables en /composables/ para lógica reutilizable
- Llamadas a la API siempre a través de los stores Pinia
"""


class FrontendVueAgent:
    def __init__(self, project_path: str = "."):
        self.project_path = project_path

    async def create_component(self, component_name: str, description: str, props: str = "") -> str:
        """Crea un componente Vue 3 específico en el sistema de archivos."""
        prompt = (
            f"Crea el componente Vue 3 '{component_name}' en frontend/src/components/.\n"
            f"Descripción: {description}\n"
            + (f"Props esperadas: {props}\n" if props else "")
            + "Incluye también un composable si la lógica es compleja."
        )

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=15,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text

    async def create_itinerary_components(self) -> str:
        """Crea todos los componentes del módulo de itinerarios."""
        prompt = (
            "Crea el conjunto completo de componentes para el módulo de itinerarios:\n"
            "1. ItineraryView.vue — vista principal del itinerario con timeline\n"
            "2. ItineraryDay.vue — card de un día con lista de actividades\n"
            "3. ActivityCard.vue — tarjeta de una actividad individual\n"
            "4. PromptEditor.vue — campo de texto con botón para editar itinerario con IA\n"
            "5. AILoadingIndicator.vue — animación mientras la IA genera/edita\n\n"
            "El PromptEditor debe enviar el prompt al store y mostrar el resultado en tiempo real."
        )

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=30,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text

    async def create_trip_components(self) -> str:
        """Crea todos los componentes del módulo de viajes."""
        prompt = (
            "Crea el conjunto completo de componentes para el módulo de viajes:\n"
            "1. TripCard.vue — tarjeta de viaje para el dashboard (con imagen, destino, fechas, rating)\n"
            "2. TripForm.vue — formulario para crear/editar un viaje\n"
            "3. DestinationSearch.vue — buscador de destinos con autocompletado\n"
            "4. RatingStars.vue — componente de valoración con estrellas interactivas\n"
            "5. ShareModal.vue — modal para compartir un viaje con contenido social generado por IA\n"
        )

        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=self.project_path,
                allowed_tools=["Read", "Write", "Edit", "Glob"],
                permission_mode="acceptEdits",
                system_prompt=SYSTEM_PROMPT,
                max_turns=30,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        return result_text


def run_component(project_path: str, component_name: str, description: str, props: str = "") -> str:
    agent = FrontendVueAgent(project_path=project_path)
    return anyio.run(agent.create_component, component_name, description, props)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    agent = FrontendVueAgent(project_path=path)
    result = anyio.run(agent.create_itinerary_components)
    print(result)
