from .base_skill import BaseSkill


class VueComponentGeneratorSkill(BaseSkill):
    name = "VueComponentGeneratorSkill"
    description = (
        "Genera componentes Vue 3 con Composition API y stores Pinia para Travel AI App. "
        "Produce componentes reutilizables con TypeScript, Tailwind CSS y manejo de estado reactivo."
    )

    def generate_component(self, component_name: str, props: str = "", features: str = "") -> str:
        return self.run(
            f"Genera el componente Vue 3 llamado '{component_name}'.\n"
            f"Props esperadas: {props}\n"
            f"Funcionalidades: {features}\n"
            "Usa <script setup lang='ts'>, Tailwind para estilos, emits tipados y composables si aplica."
        )

    def generate_store(self, store_name: str, state_fields: str, actions: str = "") -> str:
        return self.run(
            f"Genera el store Pinia llamado '{store_name}'.\n"
            f"Campos de estado: {state_fields}\n"
            f"Acciones: {actions}\n"
            "Usa defineStore con Composition API style. Incluye llamadas a la API REST con Axios."
        )

    def generate_view(self, view_name: str, description: str = "") -> str:
        return self.run(
            f"Genera la vista Vue 3 llamada '{view_name}'.\n"
            f"Descripción: {description}\n"
            "Incluye vue-router para navegación, el store Pinia correspondiente y manejo de loading/errores."
        )
