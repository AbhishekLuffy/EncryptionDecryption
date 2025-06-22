package com.encryption.blowfish;

import com.encryption.utils.PerformanceMetrics;
import java.util.ArrayList;
import java.util.List;

public class BlowfishPerformance {
    public static void main(String[] args) {
        try {
            String key = "mysecretkey123";
            System.out.println("Blowfish Encryption & Decryption Performance Analysis");

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
                String encrypted = BlowfishEncryption.encrypt(key, plaintext);
                long endTime = System.nanoTime();
                double encryptTime = (endTime - startTime) / 1_000_000_000.0; // Convert to seconds
                encryptTimes.add(encryptTime);

                // Measure memory usage (approximate)
                Runtime runtime = Runtime.getRuntime();
                long beforeMemory = runtime.totalMemory() - runtime.freeMemory();
                encrypted = BlowfishEncryption.encrypt(key, plaintext);
                long afterMemory = runtime.totalMemory() - runtime.freeMemory();
                double memoryUsed = (afterMemory - beforeMemory) / 1024.0; // Convert to KB
                encryptMemory.add(memoryUsed);

                // Measure decryption
                startTime = System.nanoTime();
                String decrypted = BlowfishEncryption.decrypt(key, encrypted);
                endTime = System.nanoTime();
                double decryptTime = (endTime - startTime) / 1_000_000_000.0; // Convert to seconds
                decryptTimes.add(decryptTime);

                // Measure decryption memory
                beforeMemory = runtime.totalMemory() - runtime.freeMemory();
                decrypted = BlowfishEncryption.decrypt(key, encrypted);
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
            System.out.println("\nPerformance graphs have been saved as 'blowfish_performance_time.png' and 'blowfish_performance_memory.png'");

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
} 