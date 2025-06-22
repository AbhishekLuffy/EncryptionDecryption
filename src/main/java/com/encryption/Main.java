package com.encryption;

import com.encryption.blowfish.BlowfishEncryption;
import com.encryption.twofish.TwofishEncryption;

public class Main {
    public static void main(String[] args) {
        try {
            // Test data
            String key = "mysecretkey12345678901234567890";
            String plaintext = "Hello, this is a test message!";

            System.out.println("Original text: " + plaintext);
            System.out.println("Key: " + key);
            System.out.println("\n--- Blowfish Test ---");
            
            // Test Blowfish
            String blowfishEncrypted = BlowfishEncryption.encrypt(key, plaintext);
            System.out.println("Blowfish Encrypted: " + blowfishEncrypted);
            String blowfishDecrypted = BlowfishEncryption.decrypt(key, blowfishEncrypted);
            System.out.println("Blowfish Decrypted: " + blowfishDecrypted);

            System.out.println("\n--- Twofish Test ---");
            // Test Twofish
            String twofishEncrypted = TwofishEncryption.encrypt(key, plaintext);
            System.out.println("Twofish Encrypted: " + twofishEncrypted);
            String twofishDecrypted = TwofishEncryption.decrypt(key, twofishEncrypted);
            System.out.println("Twofish Decrypted: " + twofishDecrypted);

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
} 