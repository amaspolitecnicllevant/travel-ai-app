from .base_skill import BaseSkill


class CodeValidatorSkill(BaseSkill):
    name = "CodeValidatorSkill"
    description = (
        "Valida código fuente de Travel AI App buscando errores, vulnerabilidades de seguridad, "
        "malas prácticas y problemas de rendimiento. Proporciona un informe detallado con sugerencias."
    )

    def validate(self, code: str, language: str = "Java") -> str:
        return self.run(
            f"Valida el siguiente código {language} para Travel AI App:\n\n"
            f"```{language.lower()}\n{code}\n```\n\n"
            "Revisa:\n"
            "1. Errores de sintaxis o lógica\n"
            "2. Vulnerabilidades de seguridad (SQL injection, XSS, etc.)\n"
            "3. Manejo correcto de excepciones\n"
            "4. Rendimiento y queries N+1\n"
            "5. Cumplimiento con la arquitectura del proyecto\n"
            "Proporciona un resumen con nivel de severidad: CRÍTICO, ADVERTENCIA, INFO."
        )
