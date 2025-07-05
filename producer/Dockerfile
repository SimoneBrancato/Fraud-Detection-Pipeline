FROM maven:3.8.4-openjdk-17 AS build
WORKDIR /app
COPY . .
RUN mvn package

# Code execution stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/kafka-producer-1.0-jar-with-dependencies.jar ./app.jar
COPY --from=build /app/src/main/resources/fraudTest.csv .

ENV TEST_DATA_PATH=fraudTest.csv

CMD ["java", "-jar", "app.jar"]