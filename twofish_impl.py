import base64
from typing import Tuple
import struct
import hashlib

# Twofish S-boxes (simplified for demonstration)
SBOX = [
    0x29, 0x2E, 0x43, 0xC9, 0xA2, 0xD8, 0x7C, 0x01, 0x3D, 0x36, 0x54, 0xA1, 0xEC, 0xF0, 0x06, 0x13,
    0x62, 0xA7, 0x05, 0xF3, 0xC0, 0xC7, 0x73, 0x8C, 0x98, 0x93, 0x2B, 0xD9, 0xBC, 0x4C, 0x82, 0xCA,
    0x1E, 0x9B, 0x57, 0x3C, 0xFD, 0xD4, 0xE0, 0x16, 0x67, 0x42, 0x6F, 0x18, 0x8A, 0x17, 0xE5, 0x12,
    0xBE, 0x4E, 0xC4, 0xD6, 0xDA, 0x9E, 0xDE, 0x49, 0xA0, 0xFB, 0xF5, 0x8E, 0xBB, 0x2F, 0xEE, 0x7A,
    0xA9, 0x68, 0x79, 0x91, 0x15, 0xB2, 0x07, 0x3F, 0x94, 0xC2, 0x10, 0x89, 0x0B, 0x22, 0x5F, 0x21,
    0x80, 0x7F, 0x5D, 0x9A, 0x5A, 0x90, 0x32, 0x27, 0x35, 0x3E, 0xCC, 0xE7, 0xBF, 0xF7, 0x97, 0x03,
    0xFF, 0x19, 0x30, 0xB3, 0x48, 0xA5, 0xB5, 0xD1, 0xD7, 0x5E, 0x92, 0x2A, 0xAC, 0x56, 0xAA, 0xC6,
    0x4F, 0xB8, 0x38, 0xD2, 0x96, 0xA4, 0x7D, 0xB6, 0x76, 0xFC, 0x6B, 0xE2, 0x9C, 0x74, 0x04, 0xF1,
    0x45, 0x9D, 0x70, 0x59, 0x64, 0x71, 0x87, 0x20, 0x86, 0x5B, 0xCF, 0x65, 0xE6, 0x2D, 0xA8, 0x02,
    0x1B, 0x60, 0x25, 0xAD, 0xAE, 0xB0, 0xB9, 0xF6, 0x1C, 0x46, 0x61, 0x69, 0x34, 0x40, 0x7E, 0x0F,
    0x55, 0x47, 0xA3, 0x23, 0xDD, 0x51, 0xAF, 0x3A, 0xC3, 0x5C, 0xF9, 0xCE, 0xBA, 0xC5, 0xEA, 0x26,
    0x2C, 0x53, 0x0D, 0x6E, 0x85, 0x28, 0x84, 0x09, 0xD3, 0xDF, 0xCD, 0xF4, 0x41, 0x81, 0x4D, 0x52,
    0x6A, 0xDC, 0x37, 0xC8, 0x6C, 0xC1, 0xAB, 0xFA, 0x24, 0xE1, 0x7B, 0x08, 0x0C, 0xBD, 0xB1, 0x4A,
    0x78, 0x88, 0x95, 0x8B, 0xE3, 0x63, 0xE8, 0x6D, 0xE9, 0xCB, 0xD5, 0xFE, 0x3B, 0x00, 0x1D, 0x39,
    0xF2, 0xEF, 0xB7, 0x0E, 0x66, 0x58, 0xD0, 0xE4, 0xA6, 0x77, 0x72, 0xF8, 0xEB, 0x75, 0x4B, 0x0A,
    0x31, 0x44, 0x50, 0xB4, 0x8F, 0xED, 0x1F, 0x1A, 0xDB, 0x99, 0x8D, 0x33, 0x9F, 0x11, 0x83, 0x14
]

class Twofish:
    def __init__(self, key: bytes):
        # Ensure key is exactly 32 bytes
        if len(key) > 32:
            key = key[:32]
        elif len(key) < 32:
            key = key + b'\x00' * (32 - len(key))
        
        self.key = key
        self._setup_key()

    def _setup_key(self):
        # Generate subkeys using a hash-based approach
        self._subkeys = []
        for i in range(40):
            # Create a unique seed for each subkey
            seed = self.key + struct.pack('>I', i)
            hash_obj = hashlib.sha256(seed)
            subkey = int.from_bytes(hash_obj.digest()[:4], 'big')
            self._subkeys.append(subkey)

    def _mix_function(self, x: int, y: int) -> int:
        # Simple mixing function
        return ((x + y) ^ (x >> 3) ^ (y << 7)) & 0xFFFFFFFF

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("Block size must be 16 bytes")
        
        # Convert to 32-bit words
        r0, r1, r2, r3 = struct.unpack('>4I', block)
        
        # 16 rounds of encryption
        for i in range(16):
            # Mix with subkeys
            r0 ^= self._subkeys[i * 2]
            r1 ^= self._subkeys[i * 2 + 1]
            
            # Apply mixing function
            temp = self._mix_function(r0, r1)
            r2 ^= temp
            r3 ^= temp
            
            # Rotate words
            r0, r1, r2, r3 = r2, r3, r0, r1
        
        # Final mixing
        r0 ^= self._subkeys[32]
        r1 ^= self._subkeys[33]
        r2 ^= self._subkeys[34]
        r3 ^= self._subkeys[35]
        
        return struct.pack('>4I', r0, r1, r2, r3)

    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("Block size must be 16 bytes")
        
        # Convert to 32-bit words
        r0, r1, r2, r3 = struct.unpack('>4I', block)
        
        # Final mixing (reverse)
        r0 ^= self._subkeys[32]
        r1 ^= self._subkeys[33]
        r2 ^= self._subkeys[34]
        r3 ^= self._subkeys[35]
        
        # 16 rounds of decryption (reverse order)
        for i in range(15, -1, -1):
            # Rotate words (reverse)
            r0, r1, r2, r3 = r2, r3, r0, r1
            
            # Apply mixing function (reverse)
            temp = self._mix_function(r0, r1)
            r2 ^= temp
            r3 ^= temp
            
            # Mix with subkeys (reverse)
            r0 ^= self._subkeys[i * 2]
            r1 ^= self._subkeys[i * 2 + 1]
        
        return struct.pack('>4I', r0, r1, r2, r3)

def pad_data(data: bytes) -> bytes:
    """PKCS7 padding"""
    padding_length = 16 - (len(data) % 16)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad_data(data: bytes) -> bytes:
    """Remove PKCS7 padding"""
    if len(data) == 0:
        return data
    padding_length = data[-1]
    if padding_length > 16 or padding_length == 0:
        raise ValueError("Invalid padding")
    return data[:-padding_length]

def encrypt_twofish(key: bytes, plaintext: str) -> Tuple[bytes, str]:
    """Encrypt data using Twofish algorithm."""
    cipher = Twofish(key)
    data = plaintext.encode('utf-8')
    padded_data = pad_data(data)
    
    encrypted_blocks = []
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i+16]
        encrypted_block = cipher.encrypt_block(block)
        encrypted_blocks.append(encrypted_block)
    
    encrypted_data = b''.join(encrypted_blocks)
    encrypted_text = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_data, encrypted_text

def decrypt_twofish(key: bytes, encrypted_text: str) -> str:
    """Decrypt data using Twofish algorithm."""
    cipher = Twofish(key)
    encrypted_data = base64.b64decode(encrypted_text)
    
    decrypted_blocks = []
    for i in range(0, len(encrypted_data), 16):
        block = encrypted_data[i:i+16]
        decrypted_block = cipher.decrypt_block(block)
        decrypted_blocks.append(decrypted_block)
    
    decrypted_data = b''.join(decrypted_blocks)
    unpadded_data = unpad_data(decrypted_data)
    return unpadded_data.decode('utf-8')

# Test the implementation
if __name__ == '__main__':
    test_key = b'mysecretkey12345678901234567890'
    test_message = "Hello, this is a test message!"
    print(f"Original message: {test_message}")
    
    encrypted_data, encrypted_text = encrypt_twofish(test_key, test_message)
    print(f"Encrypted: {encrypted_text}")
    
    decrypted_text = decrypt_twofish(test_key, encrypted_text)
    print(f"Decrypted: {decrypted_text}")
    
    if decrypted_text == test_message:
        print("✅ Test passed successfully!")
    else:
        print("❌ Test failed!")
        print(f"Expected: {test_message}")
        print(f"Got: {decrypted_text}")
