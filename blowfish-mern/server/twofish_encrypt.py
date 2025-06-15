from twofish import Twofish
import base64
import time
import sys

def encrypt(text, key):
    try:
        # Convert text and key to bytes
        text_bytes = text.encode('utf-8')
        key_bytes = key.encode('utf-8')
        
        # Create Twofish cipher
        cipher = Twofish(key_bytes)
        
        # Pad the text to be a multiple of 16 bytes
        padding_length = 16 - (len(text_bytes) % 16)
        padded_text = text_bytes + bytes([padding_length] * padding_length)
        
        # Encrypt
        encrypted_text = cipher.encrypt(padded_text)
        
        # Convert to base64 for safe transmission
        return base64.b64encode(encrypted_text).decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def decrypt(encrypted_text, key):
    try:
        # Convert encrypted text and key to bytes
        encrypted_bytes = base64.b64decode(encrypted_text)
        key_bytes = key.encode('utf-8')
        
        # Create Twofish cipher
        cipher = Twofish(key_bytes)
        
        # Decrypt
        decrypted_text = cipher.decrypt(encrypted_bytes)
        
        # Remove padding
        padding_length = decrypted_text[-1]
        unpadded_text = decrypted_text[:-padding_length]
        
        # Convert back to string
        return unpadded_text.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python twofish.py [encrypt/decrypt] [text] [key]", file=sys.stderr)
        sys.exit(1)
        
    operation = sys.argv[1]
    text = sys.argv[2]
    key = sys.argv[3]
    
    if len(key) < 16:
        print("Key must be at least 16 characters long", file=sys.stderr)
        sys.exit(1)
    
    if operation == "encrypt":
        result = encrypt(text, key)
    elif operation == "decrypt":
        result = decrypt(text, key)
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'", file=sys.stderr)
        sys.exit(1)
        
    print(result) 