from .base_skill import BaseSkill


class CodeRefactorSkill(BaseSkill):
    name = "CodeRefactorSkill"
    description = (
        "Refactoriza código de Travel AI App mejorando legibilidad, rendimiento y mantenibilidad. "
        "Aplica patrones de diseño, elimina duplicación y asegura consistencia con el resto del proyecto."
    )

    def refactor(self, code: str, language: str = "Java", goals: str = "") -> str:
        return self.run(
            f"Refactoriza el siguiente código {language}:\n\n```{language.lower()}\n{code}\n```\n\n"
            f"Objetivos de refactorización: {goals or 'mejorar legibilidad y seguir buenas prácticas'}\n"
            "Explica cada cambio realizado."
        )
