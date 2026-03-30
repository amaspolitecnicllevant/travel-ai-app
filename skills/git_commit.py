from .base_skill import BaseSkill


class GitCommitSkill(BaseSkill):
    name = "GitCommitSkill"
    description = (
        "Genera mensajes de commit semánticos y descriptivos para Travel AI App. "
        "Sigue el estándar Conventional Commits (feat, fix, docs, refactor, test, chore)."
    )

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        return self.run(
            f"Genera un mensaje de commit para el siguiente diff de Git:\n\n```diff\n{diff}\n```\n\n"
            f"Contexto adicional: {context}\n"
            "Sigue el formato Conventional Commits:\n"
            "  <type>(<scope>): <descripción corta>\n\n"
            "  [cuerpo opcional explicando el por qué]\n\n"
            "Tipos: feat, fix, docs, style, refactor, test, chore, perf",
            max_tokens=512,
        )
