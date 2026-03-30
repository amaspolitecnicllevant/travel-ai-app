import os
import subprocess
import json
import requests

# ----------------------
# CONFIGURACIÓN
# ----------------------
GITHUB_REPO = "git@github.com:amaspolitecnicllevant/travel-ai-app.git"  # Cambia por tu repo
CLAUDE_API_URL = "https://api.anthropic.com/v1/skills"
API_KEY = "TU_API_KEY_CLAUDE"  # Cambia por tu API Key
PROJECT_NAME = "travel-ai-app"

# ----------------------
# 1️⃣ CREAR ESTRUCTURA DE PROYECTO
# ----------------------
folders = [
    "backend/src",
    "frontend/src",
    "scripts",
    ".github/workflows"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
print("[OK] Estructura de carpetas creada")

# ----------------------
# 2️⃣ CREAR DOCKERFILES
# ----------------------
backend_dockerfile = """
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN ./mvnw clean package -DskipTests
EXPOSE 8080
CMD ["java","-jar","target/backend.jar"]
"""

frontend_dockerfile = """
FROM node:20
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY src ./src
RUN npm run build
EXPOSE 5173
CMD ["npm","run","dev","--","--host"]
"""

with open("backend/Dockerfile", "w") as f:
    f.write(backend_dockerfile)
with open("frontend/Dockerfile", "w") as f:
    f.write(frontend_dockerfile)
print("[OK] Dockerfiles creados")

# ----------------------
# 3️⃣ CREAR DOCKER-COMPOSE
# ----------------------
docker_compose = """
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    depends_on:
      - db
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: travel_ai
    ports:
      - "5432:5432"
"""

with open("docker-compose.yml", "w") as f:
    f.write(docker_compose)
print("[OK] docker-compose.yml creado")

# ----------------------
# 4️⃣ CREAR .gitignore
# ----------------------
gitignore = """
# backend
/backend/target/
/backend/.mvn/
/backend/*.iml

# frontend
/frontend/node_modules/
/frontend/dist/
"""

with open(".gitignore", "w") as f:
    f.write(gitignore)
print("[OK] .gitignore creado")

# ----------------------
# 5️⃣ INICIALIZAR GIT Y PUSH A GITHUB
# ----------------------
subprocess.run(["git", "init"])
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Proyecto inicial Travel AI App"])
subprocess.run(["git", "push", "-u", "origin", "main"])
print("[OK] GitHub inicializado y commit inicial realizado")

# ----------------------
# 6️⃣ CREAR WORKFLOW CI/CD
# ----------------------
ci_cd = """
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        ports:
          - 5432:5432
        env:
          POSTGRES_USER: root
          POSTGRES_PASSWORD: root
          POSTGRES_DB: travel_ai
        options: >-
          --health-cmd "pg_isready -U root"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK
        uses: actions/setup-java@v3
        with:
          distribution: temurin
          java-version: 17
      - name: Build Backend
        working-directory: backend
        run: mvn clean package
      - name: Build Frontend
        working-directory: frontend
        run: |
          npm install
          npm run build
      - name: Build Docker
        run: docker-compose build
"""

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(ci_cd)
print("[OK] Workflow CI/CD creado")

# ----------------------
# 7️⃣ REGISTRAR AGENTES EN CLAUDE
# ----------------------
app_context = {
    "appName": PROJECT_NAME,
    "description": "Usuarios registran viajes, generan itinerarios con IA, los editan con prompts, comparten viajes y reciben valoraciones",
    "models": {
        "User": ["id","username","email","password"],
        "Trip": ["id","title","destination","type","startDate","endDate","userId"],
        "Rating": ["id","tripId","userId","score"],
        "Itinerary": ["days","activities","time","name","type"]
    },
    "technologies": ["Spring Boot","JWT","PostgreSQL","Vue 3","Pinia","Tailwind","Axios","Docker","Claude Agents"],
    "flows":["Registro/Login","Crear viaje","Generar itinerario IA","Editar itinerario con prompt","Compartir viaje y valorar"],
    "requirements":["REST endpoints","JSON itinerarios","dockerizado","dev/prod"]
}

agents = [
    # TravelPlanner, Budget, Experience, Editor, Social, PromptEngineer, FrontendVue, DevOps
    # BackendBuilder y FrontendBuilder
]

# Generar payloads para cada agente
for name in ["TravelPlannerAgent","BudgetAgent","ExperienceAgent","EditorAgent",
             "SocialAgent","PromptEngineerAgent","FrontendVueAgent","DevOpsAgent",
             "BackendBuilderAgent","FrontendBuilderAgent"]:
    payload = {
        "name": name,
        "description": f"Agente {name} con contexto completo de la app {PROJECT_NAME}",
        "prompt_template": f"Eres {name}. Contexto de la aplicación: {json.dumps(app_context)} Genera tu tarea específica.",
        "examples":[{"input":"Ejemplo de input","output":"Ejemplo de output"}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
    if response.status_code in [200,201]:
        print(f"[OK] {name} registrado")
    else:
        print(f"[ERROR] {name} falló: {response.status_code} {response.text}")

print("[OK] Todos los agentes registrados y proyecto listo para desarrollo profesional con GitHub y Docker")