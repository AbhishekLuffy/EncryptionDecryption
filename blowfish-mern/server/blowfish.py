from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import base64
import sys

def encrypt_blowfish(key, plaintext):
    cipher = Blowfish.new(key.encode(), Blowfish.MODE_ECB)
    padded_text = pad(plaintext.encode(), Blowfish.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_bytes).decode()

def decrypt_blowfish(key, ciphertext):
    cipher = Blowfish.new(key.encode(), Blowfish.MODE_ECB)
    encrypted_bytes = base64.b64decode(ciphertext)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    return unpad(decrypted_padded, Blowfish.block_size).decode()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python blowfish.py [encrypt|decrypt] text key")
        sys.exit(1)

    action = sys.argv[1]
    text = sys.argv[2]
    key = sys.argv[3]

    try:
        if action == "encrypt":
            result = encrypt_blowfish(key, text)
        elif action == "decrypt":
            result = decrypt_blowfish(key, text)
        else:
            print("Invalid action. Use 'encrypt' or 'decrypt'")
            sys.exit(1)
        
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1) 