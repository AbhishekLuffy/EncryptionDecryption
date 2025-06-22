package com.encryption.twofish;

import com.encryption.utils.PerformanceMetrics;
import java.util.ArrayList;
import java.util.List;

public class TwofishMain {
    public static void main(String[] args) {
        try {
            String key = "mysecretkey123";
            System.out.println("Twofish Encryption & Decryption Performance Analysis");

            // Test with different input sizes
            List<Integer> inputSizes = new ArrayList<>();
            List<Double> encryptTimes = new ArrayList<>();
            List<Double> decryptTimes = new ArrayList<>();
            List<Double> encryptMemory = new ArrayList<>();
            List<Double> decryptMemory = new ArrayList<>();

            // Test sizes in bytes
            int[] testSizes = {16, 64, 256, 1024, 4096};

            for (int size : testSizes) {
                // Generate test data
                String plaintext = "A".repeat(size);
                inputSizes.add(size);

                // Measure encryption
                long startTime = System.nanoTime();
                TwofishEncryption.EncryptionResult result = TwofishEncryption.encrypt(key, plaintext);
                long endTime = System.nanoTime();
                double encryptTime = (endTime - startTime) / 1_000_000_000.0; // Convert to seconds
                encryptTimes.add(encryptTime);

                // Measure memory usage (approximate)
                Runtime runtime = Runtime.getRuntime();
                long beforeMemory = runtime.totalMemory() - runtime.freeMemory();
                result = TwofishEncryption.encrypt(key, plaintext);
                long afterMemory = runtime.totalMemory() - runtime.freeMemory();
                double memoryUsed = (afterMemory - beforeMemory) / 1024.0; // Convert to KB
                encryptMemory.add(memoryUsed);

                // Measure decryption
                startTime = System.nanoTime();
                String decrypted = TwofishEncryption.decrypt(key, result.getEncryptedBase64());
                endTime = System.nanoTime();
                double decryptTime = (endTime - startTime) / 1_000_000_000.0; // Convert to seconds
                decryptTimes.add(decryptTime);

                // Measure decryption memory
                beforeMemory = runtime.totalMemory() - runtime.freeMemory();
                decrypted = TwofishEncryption.decrypt(key, result.getEncryptedBase64());
                afterMemory = runtime.totalMemory() - runtime.freeMemory();
                memoryUsed = (afterMemory - beforeMemory) / 1024.0; // Convert to KB
                decryptMemory.add(memoryUsed);

                System.out.printf("\nTest with input size: %d bytes%n", size);
                System.out.printf("Encryption time: %.8f seconds%n", encryptTime);
                System.out.printf("Encryption memory: %.2f KB%n", encryptMemory.get(encryptMemory.size() - 1));
                System.out.printf("Decryption time: %.8f seconds%n", decryptTime);
                System.out.printf("Decryption memory: %.2f KB%n", decryptMemory.get(decryptMemory.size() - 1));
            }

            // Generate performance graphs
            PerformanceMetrics.plotPerformanceMetrics(
                encryptTimes, decryptTimes,
                encryptMemory, decryptMemory,
                inputSizes
            );
            System.out.println("\nPerformance graphs have been saved as 'twofish_performance_time.png' and 'twofish_performance_memory.png'");

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
} 