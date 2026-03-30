import os
import json
import requests
import subprocess

# ----------------------
# CONFIGURACIÓN
# ----------------------
PROJECT_NAME = "travel-ai-app"
BACKEND_PATH = "backend"
FRONTEND_PATH = "frontend"
API_KEY = "TU_API_KEY_CLAUDE"  # Cambiar
CLAUDE_AGENT_RUN_URL = "https://api.anthropic.com/v1/agents/run"
CLAUDE_SKILL_URL = "https://api.anthropic.com/v1/skills"
GITHUB_REPO = "git@github.com:TU_USUARIO/travel-ai-app.git"

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# ----------------------
# CONTEXTO DE LA APP
# ----------------------
app_context = {
    "appName": PROJECT_NAME,
    "description": "Usuarios crean viajes, IA genera itinerarios, los editan con prompts, comparten viajes y reciben valoraciones",
    "models": {
        "User":["id","username","email","password"],
        "Trip":["id","title","destination","type","startDate","endDate","userId"],
        "Rating":["id","tripId","userId","score"],
        "Itinerary":["days","activities","time","name","type"]
    },
    "technologies":["Spring Boot","JWT","PostgreSQL","Vue 3","Pinia","Tailwind","Axios","Docker","Claude Agents"],
    "flows":["Registro/Login","Crear viaje","Generar itinerario IA","Editar itinerario con prompt","Compartir viaje y valorar"],
    "requirements":["REST endpoints","JSON itinerarios","dockerizado","dev/prod"]
}

# ----------------------
# 1️⃣ CREAR ESTRUCTURA DE PROYECTO
# ----------------------
folders = [BACKEND_PATH+"/src", FRONTEND_PATH+"/src", ".github/workflows", "scripts"]
for f in folders: os.makedirs(f, exist_ok=True)
print("[OK] Estructura de proyecto creada")

# ----------------------
# 2️⃣ REGISTRAR SKILLS DE PROGRAMACIÓN
# ----------------------
programming_skills = [
    {"name": "CodeGeneratorSkill","description":"Genera código backend o frontend","example_input":{},"example_output":""},
    {"name": "VueComponentGeneratorSkill","description":"Genera componentes Vue 3 y stores Pinia","example_input":{},"example_output":""},
    {"name": "CodeRefactorSkill","description":"Refactoriza código","example_input":{},"example_output":""},
    {"name": "CodeValidatorSkill","description":"Valida código fuente","example_input":{},"example_output":""},
    {"name": "DockerfileGeneratorSkill","description":"Genera Dockerfile y docker-compose","example_input":{},"example_output":""},
    {"name": "TestGeneratorSkill","description":"Genera tests unitarios","example_input":{},"example_output":""},
    {"name": "GitCommitSkill","description":"Genera commits automáticos","example_input":{},"example_output":""}
]

for skill in programming_skills:
    payload = {
        "name": skill["name"],
        "description": skill["description"],
        "prompt_template": f"Eres {skill['name']}. Contexto de la app: {json.dumps(app_context)}. Realiza tu tarea",
        "examples":[{"input": skill["example_input"],"output": skill["example_output"]}]
    }
    response = requests.post(CLAUDE_SKILL_URL, headers=HEADERS, json=payload)
    if response.status_code in [200,201]: print(f"[OK] Skill registrada: {skill['name']}")
    else: print(f"[ERROR] Skill {skill['name']} falló: {response.text}")

# ----------------------
# 3️⃣ REGISTRAR AGENTES
# ----------------------
agents = ["BackendBuilderAgent","FrontendBuilderAgent","TravelPlannerAgent"]
for agent in agents:
    payload = {
        "name": agent,
        "description": f"Agente {agent} para Travel AI App",
        "prompt_template": f"Eres {agent}. Contexto de la app: {json.dumps(app_context)}",
        "examples":[{"input":"ejemplo","output":"ejemplo"}]
    }
    # Registrar el agente
    response = requests.post("https://api.anthropic.com/v1/skills", headers=HEADERS, json=payload)
    if response.status_code in [200,201]: print(f"[OK] Agente registrado: {agent}")
    else: print(f"[ERROR] Agente {agent} falló: {response.text}")

# ----------------------
# 4️⃣ GENERAR BACKEND con BackendBuilderAgent
# ----------------------
backend_payload = {"agent":"BackendBuilderAgent","input":{"appContext":app_context,"projectPath":BACKEND_PATH}}
response = requests.post(CLAUDE_AGENT_RUN_URL, headers=HEADERS, json=backend_payload)
if response.status_code == 200:
    code = response.json().get("output","")
    with open(os.path.join(BACKEND_PATH,"backend_generated.java"), "w") as f: f.write(code)
    print("[OK] Backend generado")
else:
    print(f"[ERROR] BackendBuilderAgent falló: {response.text}")

# ----------------------
# 5️⃣ GENERAR FRONTEND con FrontendBuilderAgent
# ----------------------
frontend_payload = {"agent":"FrontendBuilderAgent","input":{"appContext":app_context,"projectPath":FRONTEND_PATH,"apiUrl":"http://localhost:8080/api"}}
response = requests.post(CLAUDE_AGENT_RUN_URL, headers=HEADERS, json=frontend_payload)
if response.status_code == 200:
    code = response.json().get("output","")
    with open(os.path.join(FRONTEND_PATH,"frontend_generated.vue"), "w") as f: f.write(code)
    print("[OK] Frontend generado")
else:
    print(f"[ERROR] FrontendBuilderAgent falló: {response.text}")

# ----------------------
# 6️⃣ GENERAR ITINERARIO DE PRUEBA con TravelPlannerAgent
# ----------------------
travel_payload = {"agent":"TravelPlannerAgent","input":{"appContext":app_context,"destination":"París","days":5}}
response = requests.post(CLAUDE_AGENT_RUN_URL, headers=HEADERS, json=travel_payload)
if response.status_code == 200:
    itinerary = response.json().get("output","")
    os.makedirs(PROJECT_NAME, exist_ok=True)
    with open(os.path.join(PROJECT_NAME,"itinerary_paris.json"), "w") as f: f.write(itinerary)
    print("[OK] Itinerario de prueba generado")
else:
    print(f"[ERROR] TravelPlannerAgent falló: {response.text}")

# ----------------------
# 7️⃣ INICIALIZAR GIT Y GITHUB
# ----------------------
subprocess.run(["git","init"])
subprocess.run(["git","branch","-M","main"])
subprocess.run(["git","remote","add","origin",GITHUB_REPO])
subprocess.run(["git","add","."])
subprocess.run(["git","commit","-m","Proyecto inicial Travel AI App"])
subprocess.run(["git","push","-u","origin","main"])
print("[OK] GitHub inicializado y proyecto subido")

# ----------------------
# 8️⃣ CREAR DOCKERFILES Y DOCKER-COMPOSE
# ----------------------
backend_docker = "FROM openjdk:17-jdk-slim\nWORKDIR /app\nCOPY . .\nRUN ./mvnw clean package -DskipTests\nEXPOSE 8080\nCMD [\"java\",\"-jar\",\"target/backend.jar\"]"
frontend_docker = "FROM node:20\nWORKDIR /app\nCOPY . .\nRUN npm install\nRUN npm run build\nEXPOSE 5173\nCMD [\"npm\",\"run\",\"dev\",\"--\",\"--host\"]"
with open(os.path.join(BACKEND_PATH,"Dockerfile"),"w") as f: f.write(backend_docker)
with open(os.path.join(FRONTEND_PATH,"Dockerfile"),"w") as f: f.write(frontend_docker)
docker_compose = "version:'3.8'\nservices:\n backend:\n  build: ./backend\n  ports: ['8080:8080']\n frontend:\n  build: ./frontend\n  ports: ['5173:5173']"
with open("docker-compose.yml","w") as f: f.write(docker_compose)
print("[OK] Dockerfiles y docker-compose creados")

print("[🎉] Proyecto completo inicializado profesionalmente con agentes, skills, Docker y GitHub")