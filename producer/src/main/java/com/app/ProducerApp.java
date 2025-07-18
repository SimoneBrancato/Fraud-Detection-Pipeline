package com.app;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer; // Converts strings in bytes (Kafka requirement)

import java.io.*;
import java.nio.file.*;
import java.util.Properties;
import java.util.concurrent.ThreadLocalRandom;

public class ProducerApp {

    // Configuration constants
    private static final String KAFKA_BOOTSTRAP_SERVERS = System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", "kafka1:9092");
    private static final String KAFKA_TOPIC = System.getenv().getOrDefault("KAFKA_TOPIC", "fraud-transactions");
    private static final String TEST_DATA_PATH = System.getenv().getOrDefault("TEST_DATA_PATH", "src/main/resources/fraudTest.csv");


    public static void main(String[] args) throws Exception {

        Thread.sleep(60000);

        System.out.println("Starting data producer...");

        // Configure Kafka Producer
        Properties props = new Properties();
        props.put("bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS); // To search the Kafka Broker
        props.put("key.serializer", StringSerializer.class.getName()); // To convert from key to byte
        props.put("value.serializer", StringSerializer.class.getName()); // To convert from byte to value

        // Create a new instance of Kafka Producer with defined properties (Key,Value -> String,String)
        Producer<String, String> producer = new KafkaProducer<>(props);

        // Converts the string path into a Path object, enabling cross-platform usage
        Path path = Paths.get(TEST_DATA_PATH);

        // Try to open a BufferedReader to the given path
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            
            reader.readLine(); // Skip the first line (header)

            int i = 0;

            // Read line by line the test data, send each of them to the Kafka Broker 
            String line;
            while ((line = reader.readLine()) != null) {
                String key = "key-" + i;
                producer.send(new ProducerRecord<>(KAFKA_TOPIC, key, line));
                i++;

                Thread.sleep(ThreadLocalRandom.current().nextInt(50, 300)); // To simulate a real-time data flow
            }
        }

        producer.close();
    }
}
