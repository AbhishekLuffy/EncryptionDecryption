import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import base64
import time
import tracemalloc
import numpy as np

# Function to encrypt plaintext using Blowfish
def encrypt_blowfish(key, plaintext):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)  # Using ECB mode
    padded_text = pad(plaintext.encode(), Blowfish.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()
    return encrypted_bytes, encrypted_base64

# Function to decrypt ciphertext using Blowfish
def decrypt_blowfish(key, ciphertext):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)  # Using ECB mode
    encrypted_bytes = base64.b64decode(ciphertext)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted_text = unpad(decrypted_padded, Blowfish.block_size).decode()
    return decrypted_text

def plot_performance_metrics(encrypt_times, decrypt_times, encrypt_memory, decrypt_memory, input_sizes):
    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot execution times
    ax1.plot(input_sizes, encrypt_times, 'b-', label='Encryption Time')
    ax1.plot(input_sizes, decrypt_times, 'r-', label='Decryption Time')
    ax1.set_xlabel('Input Size (bytes)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Encryption/Decryption Time vs Input Size')
    ax1.legend()
    ax1.grid(True)
    
    # Plot memory usage
    ax2.plot(input_sizes, encrypt_memory, 'b-', label='Encryption Memory')
    ax2.plot(input_sizes, decrypt_memory, 'r-', label='Decryption Memory')
    ax2.set_xlabel('Input Size (bytes)')
    ax2.set_ylabel('Memory Usage (KB)')
    ax2.set_title('Memory Usage vs Input Size')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('blowfish_performance.png')
    plt.close()

# Main function
if __name__ == "__main__":
    key = b"mysecretkey123"  # Key must be bytes and 4-56 bytes long
    print("Blowfish Encryption & Decryption Performance Analysis")

    # Test with different input sizes
    input_sizes = []
    encrypt_times = []
    decrypt_times = []
    encrypt_memory = []
    decrypt_memory = []

    # Test with different input sizes
    test_sizes = [16, 64, 256, 1024, 4096]  # bytes
    
    for size in test_sizes:
        # Generate random text of specified size
        plaintext = "A" * size
        input_sizes.append(size)
        
        # Measure encryption
        tracemalloc.start()
        start_encrypt = time.time()
        encrypted_bytes, encrypted_text = encrypt_blowfish(key, plaintext)
        end_encrypt = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        encrypt_times.append(end_encrypt - start_encrypt)
        encrypt_memory.append(peak / 1024)  # Convert to KB
        
        # Measure decryption
        tracemalloc.start()
        start_decrypt = time.time()
        decrypted_text = decrypt_blowfish(key, encrypted_text)
        end_decrypt = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        decrypt_times.append(end_decrypt - start_decrypt)
        decrypt_memory.append(peak / 1024)  # Convert to KB
        
        print(f"\nTest with input size: {size} bytes")
        print(f"Encryption time: {encrypt_times[-1]:.8f} seconds")
        print(f"Encryption memory: {encrypt_memory[-1]:.2f} KB")
        print(f"Decryption time: {decrypt_times[-1]:.8f} seconds")
        print(f"Decryption memory: {decrypt_memory[-1]:.2f} KB")

    # Generate performance graphs
    plot_performance_metrics(encrypt_times, decrypt_times, encrypt_memory, decrypt_memory, input_sizes)
    print("\nPerformance graphs have been saved as 'blowfish_performance.png'")
