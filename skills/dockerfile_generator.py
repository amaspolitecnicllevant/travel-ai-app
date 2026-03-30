from .base_skill import BaseSkill


class DockerfileGeneratorSkill(BaseSkill):
    name = "DockerfileGeneratorSkill"
    description = (
        "Genera Dockerfiles optimizados y docker-compose.yml para Travel AI App. "
        "Produce imágenes multi-stage ligeras para backend Spring Boot y frontend Vue 3, "
        "con configuración para entornos dev y prod."
    )

    def generate_backend_dockerfile(self, extra_requirements: str = "") -> str:
        return self.run(
            "Genera un Dockerfile multi-stage optimizado para el backend Spring Boot.\n"
            "Debe usar Maven para build, JRE slim para runtime y exponer el puerto 8080.\n"
            f"Requisitos adicionales: {extra_requirements}"
        )

    def generate_frontend_dockerfile(self, extra_requirements: str = "") -> str:
        return self.run(
            "Genera un Dockerfile multi-stage optimizado para el frontend Vue 3 + Vite.\n"
            "Debe compilar el proyecto con npm run build y servir con nginx.\n"
            f"Requisitos adicionales: {extra_requirements}"
        )

    def generate_docker_compose(self, include_db: bool = True, include_pgadmin: bool = False) -> str:
        extras = []
        if include_db:
            extras.append("PostgreSQL 15")
        if include_pgadmin:
            extras.append("pgAdmin para administración de BD")

        return self.run(
            "Genera un docker-compose.yml completo para Travel AI App con:\n"
            "- Backend Spring Boot (puerto 8080)\n"
            "- Frontend Vue 3 con nginx (puerto 80)\n"
            + ("\n".join(f"- {e}" for e in extras))
            + "\nIncluye variables de entorno, volúmenes, healthchecks y redes Docker."
        )
