from .base_skill import BaseSkill


class CodeGeneratorSkill(BaseSkill):
    name = "CodeGeneratorSkill"
    description = (
        "Genera código backend (Java/Spring Boot) o frontend (Vue 3) para Travel AI App. "
        "Produce código limpio, siguiendo buenas prácticas REST y estructura de proyecto estándar."
    )

    def generate_backend(self, component: str, requirements: str = "") -> str:
        """Genera un componente backend (Controller, Service, Repository, Entity)."""
        return self.run(
            f"Genera el código Java/Spring Boot para: {component}\n"
            f"Requisitos adicionales: {requirements}\n"
            "Incluye anotaciones JPA, validaciones Bean Validation y manejo de excepciones."
        )

    def generate_frontend(self, component: str, requirements: str = "") -> str:
        """Genera un componente frontend Vue 3."""
        return self.run(
            f"Genera el código Vue 3 (Composition API) para: {component}\n"
            f"Requisitos adicionales: {requirements}\n"
            "Usa Tailwind CSS para estilos y Axios para llamadas a la API."
        )
