from twofish import Twofish
import base64
import time
import tracemalloc

# Function to encrypt plaintext using Twofish
def encrypt_twofish(key, plaintext):
    cipher = Twofish(key)  # Initialize Twofish cipher
    # Pad plaintext to be a multiple of 16 bytes (Twofish block size)
    padded_text = plaintext + ' ' * (16 - len(plaintext) % 16)
    encrypted_bytes = b''.join([cipher.encrypt(padded_text[i:i+16].encode()) for i in range(0, len(padded_text), 16)])
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()
    return encrypted_base64

# Function to decrypt ciphertext using Twofish
def decrypt_twofish(key, ciphertext):
    cipher = Twofish(key)  # Initialize Twofish cipher
    encrypted_bytes = base64.b64decode(ciphertext)
    decrypted_bytes = b''.join([cipher.decrypt(encrypted_bytes[i:i+16]) for i in range(0, len(encrypted_bytes), 16)])
    # Strip padding
    decrypted_text = decrypted_bytes.decode().rstrip()
    return decrypted_text

# Main function
if __name__ == "__main__":
    print("Twofish Encryption & Decryption")

    # User input for plaintext
    plaintext = input("Enter the plaintext to encrypt: ")
    key = input("Enter a key (must be exactly 16 bytes): ").encode()

    # Ensure key length is valid
    if len(key) != 16:
        print("Error: Key must be exactly 16 bytes long!")
    else:
        print("\nOriginal plaintext:", plaintext)

        # Measure encryption time and memory usage
        tracemalloc.start()
        start_encrypt = time.time()
        encrypted_text = encrypt_twofish(key, plaintext)
        end_encrypt = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("Encrypted (Base64):", encrypted_text)
        print(f"Encryption time: {end_encrypt - start_encrypt:.6f} seconds")
        print(f"Encryption memory usage: Current={current / 1024:.2f} KB, Peak={peak / 1024:.2f} KB")

        # Measure decryption time and memory usage
        tracemalloc.start()
        start_decrypt = time.time()
        decrypted_text = decrypt_twofish(key, encrypted_text)
        end_decrypt = time.time()
        current, peak = tracemalloc.get_traced_memory() 
        tracemalloc.stop()
        print("Decrypted plaintext:", decrypted_text)
        print(f"Decryption time: {end_decrypt - start_decrypt:.6f} seconds")
        print(f"Decryption memory usage: Current={current / 1024:.2f} KB, Peak={peak / 1024:.2f} KB")
