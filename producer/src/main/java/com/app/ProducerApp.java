package com.app;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer; // Converts strings in bytes (Kafka requirement)

import java.io.*;
import java.nio.file.*;
import java.util.Properties;

public class ProducerApp {

    // Configuration constants
    private static final String KAFKA_SERVERS = "kafka:9092";
    private static final String KAFKA_TOPIC = "fraud-transactions";
    private static final String TEST_DATA_PATH = "src/main/resources/fraudTest.csv";

    public static void main(String[] args) throws Exception {

        // Configure Kafka Producer
        Properties props = new Properties();
        props.put("bootstrap.servers", KAFKA_SERVERS); // To search the Kafka Broker
        props.put("key.serializer", StringSerializer.class.getName()); // To convert from key to byte
        props.put("value.serializer", StringSerializer.class.getName()); // To convert from byte to value

        // Create a new instance of Kafka Producer with defined properties (Key,Value -> String,String)
        Producer<String, String> producer = new KafkaProducer<>(props);

        // Converts the string path into a Path object, enabling cross-platform usage
        Path path = Paths.get(TEST_DATA_PATH);

        // Try to open a BufferedReader to the given path
        try (BufferedReader reader = Files.newBufferedReader(path)) {

            // Read line by line the test data, send each of them to the Kafka Broker 
            String line;
            while ((line = reader.readLine()) != null) {
                producer.send(new ProducerRecord<>(KAFKA_TOPIC, line));
                System.out.println("Sent: " + line);
                Thread.sleep(1000); // To simulate a real-time data flow
            }
        }

        producer.close();
    }
}
