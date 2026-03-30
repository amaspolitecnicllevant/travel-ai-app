import json
import anthropic
from pathlib import Path

# Cargar contexto de la app una sola vez
_context_path = Path(__file__).parent.parent / "context" / "app_context.json"
APP_CONTEXT = json.loads(_context_path.read_text())

client = anthropic.Anthropic()


class BaseSkill:
    """Clase base para todas las skills de Travel AI App."""

    name: str = "BaseSkill"
    description: str = ""
    model: str = "claude-opus-4-6"

    def system_prompt(self) -> str:
        return (
            f"Eres {self.name}. {self.description}\n\n"
            f"Contexto de la aplicación:\n{json.dumps(APP_CONTEXT, indent=2, ensure_ascii=False)}"
        )

    def run(self, prompt: str, max_tokens: int = 8192) -> str:
        with client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            system=self.system_prompt(),
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            return stream.get_final_message().content[-1].text
