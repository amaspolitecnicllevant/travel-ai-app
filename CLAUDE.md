# Travel AI App – Agentes Claude

Este archivo documenta los agentes Claude usados en el proyecto Travel AI App, su rol, contexto y cómo interactúan con el backend, frontend y la generación de itinerarios.

---

## 1. TravelPlannerAgent
**Rol:** Genera itinerarios de viaje por días en formato JSON.  
**Uso:** Cuando un usuario crea un viaje, este agente sugiere un itinerario inicial.  
**Entrada:** `destination` (ciudad o región), `days` (número de días), preferencias del usuario.  
**Salida:** JSON con los días y actividades sugeridas.  
**Contexto:** Conoce todos los modelos (`User`, `Trip`, `Rating`, `Itinerary`) y el flujo de la app.

---

## 2. BudgetAgent
**Rol:** Ajusta itinerarios según presupuesto.  
**Uso:** Limita actividades o modifica opciones para cumplir con el presupuesto del usuario.  
**Entrada:** JSON de itinerario + `budget`.  
**Salida:** JSON ajustado.  
**Contexto:** Conoce el modelo `Itinerary` y los flujos de edición de la app.

---

## 3. ExperienceAgent
**Rol:** Añade experiencias locales al itinerario.  
**Entrada:** JSON de itinerario.  
**Salida:** JSON enriquecido con actividades culturales, gastronómicas y ocio.  

---

## 4. EditorAgent
**Rol:** Modifica itinerarios según prompt del usuario.  
**Entrada:** JSON de itinerario + `prompt_usuario` (ej: "hacer día 2 más relajado").  
**Salida:** JSON modificado según las instrucciones.  

---

## 5. SocialAgent
**Rol:** Ajusta itinerario según valoraciones de otros usuarios.  
**Entrada:** JSON de itinerario + valoraciones `[score]`.  
**Salida:** JSON optimizado según feedback social.  

---

## 6. PromptEngineerAgent
**Rol:** Optimiza prompts para Claude.  
**Uso:** Mejora prompts para generar itinerarios, backend o frontend más precisos.  
**Entrada:** Prompt original.  
**Salida:** Prompt optimizado.  

---

## 7. FrontendVueAgent
**Rol:** Genera componentes Vue 3 y stores Pinia.  
**Entrada:** Endpoint REST y modelo DTO.  
**Salida:** Código Vue 3 listo para integración.  

---

## 8. DevOpsAgent
**Rol:** Optimiza Docker, docker-compose y CI/CD.  
**Entrada:** Dockerfiles existentes o proyecto completo.  
**Salida:** Dockerfiles optimizados y scripts CI/CD.  

---

## 9. BackendBuilderAgent
**Rol:** Genera backend completo en Spring Boot.  
**Entrada:** Contexto de la app (modelos, flujo, seguridad, base de datos).  
**Salida:** Código backend listo para compilar y dockerizar.  

---

## 10. FrontendBuilderAgent
**Rol:** Genera frontend completo en Vue 3.  
**Entrada:** Contexto de la app + URL del backend.  
**Salida:** Código frontend listo para integrar con la API.  

---

## 🔹 Flujo general de interacción

1. Usuario crea un viaje → **TravelPlannerAgent** genera itinerario inicial.  
2. Usuario ajusta itinerario → **EditorAgent** o **BudgetAgent** modifican JSON.  
3. Experiencias locales → **ExperienceAgent** agrega actividades.  
4. Valoraciones → **SocialAgent** ajusta itinerario según feedback.  
5. Frontend → **FrontendVueAgent** genera componentes y stores para consumir API.  
6. Backend → **BackendBuilderAgent** genera endpoints REST, seguridad JWT y acceso a PostgreSQL.  
7. DevOps → **DevOpsAgent** prepara Docker y CI/CD.  
8. Prompts → **PromptEngineerAgent** optimiza prompts de todos los agentes.  

---

## 🔹 Notas importantes

- Todos los agentes usan el **contexto completo de la aplicación**, incluyendo modelos, flujos y requisitos de dockerización.  
- Los agentes generan código listo para **GitHub**, siguiendo la estructura `backend/` y `frontend/`.  
- Los cambios generados por agentes se pueden versionar en GitHub y probar automáticamente con el workflow CI/CD.
