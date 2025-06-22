package com.encryption.twofish;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class TwofishEncryption {
    public static class EncryptionResult {
        private final byte[] encryptedBytes;
        private final String encryptedBase64;

        public EncryptionResult(byte[] encryptedBytes, String encryptedBase64) {
            this.encryptedBytes = encryptedBytes;
            this.encryptedBase64 = encryptedBase64;
        }

        public byte[] getEncryptedBytes() {
            return encryptedBytes;
        }

        public String getEncryptedBase64() {
            return encryptedBase64;
        }
    }

    public static EncryptionResult encrypt(String key, String plaintext) throws Exception {
        // Ensure key is exactly 16 bytes
        byte[] keyBytes = padKey(key.getBytes(StandardCharsets.UTF_8));
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, "Twofish");

        Cipher cipher = Cipher.getInstance("Twofish/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);

        byte[] encryptedBytes = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));
        String encryptedBase64 = Base64.getEncoder().encodeToString(encryptedBytes);

        return new EncryptionResult(encryptedBytes, encryptedBase64);
    }

    public static String decrypt(String key, String encryptedBase64) throws Exception {
        // Ensure key is exactly 16 bytes
        byte[] keyBytes = padKey(key.getBytes(StandardCharsets.UTF_8));
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, "Twofish");

        Cipher cipher = Cipher.getInstance("Twofish/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);

        byte[] encryptedBytes = Base64.getDecoder().decode(encryptedBase64);
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);

        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }

    private static byte[] padKey(byte[] key) {
        byte[] paddedKey = new byte[16];
        System.arraycopy(key, 0, paddedKey, 0, Math.min(key.length, 16));
        return paddedKey;
    }
} 