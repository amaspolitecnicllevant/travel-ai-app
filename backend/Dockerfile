# Build stage - uses cached image
FROM maven:3.9.5-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -q
COPY src ./src
RUN mvn clean package -DskipTests -q

# Run stage - uses cached image
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=builder /app/target/backend.jar backend.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "backend.jar"]
