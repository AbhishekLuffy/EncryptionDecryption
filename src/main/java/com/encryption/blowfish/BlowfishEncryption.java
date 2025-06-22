package com.encryption.blowfish;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class BlowfishEncryption {
    private static final String ALGORITHM = "Blowfish";
    private static final String TRANSFORMATION = "Blowfish/ECB/PKCS5Padding";

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
        byte[] keyBytes = padKey(key.getBytes());
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, ALGORITHM);
        
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        
        byte[] encryptedBytes = cipher.doFinal(plaintext.getBytes());
        String encryptedBase64 = Base64.getEncoder().encodeToString(encryptedBytes);
        
        return new EncryptionResult(encryptedBytes, encryptedBase64);
    }

    public static String decrypt(String key, String ciphertext) throws Exception {
        // Ensure key is exactly 16 bytes
        byte[] keyBytes = padKey(key.getBytes());
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, ALGORITHM);
        
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(ciphertext));
        return new String(decryptedBytes);
    }

    private static byte[] padKey(byte[] key) {
        if (key.length < 16) {
            byte[] paddedKey = new byte[16];
            System.arraycopy(key, 0, paddedKey, 0, key.length);
            return paddedKey;
        } else if (key.length > 16) {
            byte[] truncatedKey = new byte[16];
            System.arraycopy(key, 0, truncatedKey, 0, 16);
            return truncatedKey;
        }
        return key;
    }
} 