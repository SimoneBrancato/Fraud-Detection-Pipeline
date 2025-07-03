# Build dependencies stage
FROM maven:3.9.4-eclipse-temurin-17 AS build
WORKDIR /app
COPY . .
RUN mvn package

# Code execution stage
FROM eclipse-temurin:17
WORKDIR /app
COPY --from=build /app/target/kafka-producer-1.0.jar .
COPY src/main/resources/test-data.csv .

CMD ["java", "-cp", "kafka-producer-1.0.jar", "com.fraud.Producer"]
