from .base_skill import BaseSkill


class TestGeneratorSkill(BaseSkill):
    name = "TestGeneratorSkill"
    description = (
        "Genera tests unitarios e de integración para Travel AI App. "
        "Para backend: JUnit 5 + Mockito + Spring Boot Test. "
        "Para frontend: Vitest + Vue Test Utils."
    )

    def generate_backend_test(self, code: str, test_type: str = "unit") -> str:
        return self.run(
            f"Genera tests {test_type} para el siguiente código Java/Spring Boot:\n\n"
            f"```java\n{code}\n```\n\n"
            "Usa JUnit 5, Mockito para mocks y @SpringBootTest para tests de integración.\n"
            "Incluye casos positivos, negativos y casos límite."
        )

    def generate_frontend_test(self, component_code: str) -> str:
        return self.run(
            "Genera tests para el siguiente componente Vue 3:\n\n"
            f"```vue\n{component_code}\n```\n\n"
            "Usa Vitest y Vue Test Utils. Testea: renderizado, props, emits y llamadas a la API (mockeadas)."
        )
