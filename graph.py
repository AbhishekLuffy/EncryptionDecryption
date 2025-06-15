import time
import matplotlib.pyplot as plt
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import base64
from twofish import Twofish

# Ensure key length is 16 bytes for Twofish
def get_valid_key(key):
    return key.ljust(16, b'\0')[:16]  # Pads to 16 bytes if shorter, trims if longer

# Example usage
twofish_key = get_valid_key(b"my16bytekeyhere")  # Ensure key is 16 bytes long

# Blowfish encryption function
def encrypt_blowfish(key, plaintext):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    padded_text = pad(plaintext.encode(), Blowfish.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()
    return encrypted_base64

# Blowfish decryption function
def decrypt_blowfish(key, ciphertext):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    encrypted_bytes = base64.b64decode(ciphertext)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted_text = unpad(decrypted_padded, Blowfish.block_size).decode()
    return decrypted_text

# Twofish encryption function
def encrypt_twofish(key, plaintext):
    cipher = Twofish(key)
    padded_text = plaintext + ' ' * (16 - len(plaintext) % 16)
    encrypted_bytes = b''.join([cipher.encrypt(padded_text[i:i+16].encode()) for i in range(0, len(padded_text), 16)])
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()
    return encrypted_base64

# Twofish decryption function
def decrypt_twofish(key, ciphertext):
    cipher = Twofish(key)
    encrypted_bytes = base64.b64decode(ciphertext)
    decrypted_bytes = b''.join([cipher.decrypt(encrypted_bytes[i:i+16]) for i in range(0, len(encrypted_bytes), 16)])
    decrypted_text = decrypted_bytes.decode().rstrip()
    return decrypted_text

# Testing and graphing performance
def measure_time(algorithm_name, encrypt_func, decrypt_func, key, data_sizes):
    encrypt_times = []
    decrypt_times = []

    for size in data_sizes:
        plaintext = "A" * size

        # Measure encryption time (convert to picoseconds)
        start = time.time()
        encrypted = encrypt_func(key, plaintext)
        end = time.time()
        encryption_time = (end - start) * 1e12  # Convert to picoseconds
        encrypt_times.append(encryption_time)

        # Measure decryption time (convert to picoseconds)
        start = time.time()
        decrypt_func(key, encrypted)
        end = time.time()
        decryption_time = (end - start) * 1e12  # Convert to picoseconds
        decrypt_times.append(decryption_time)

    return encrypt_times, decrypt_times

# Keys for testing
blowfish_key = b"mysecretkey123"
twofish_key = b"my16bytekeyhere"

# Data sizes for testing (in bytes), now including much larger sizes
data_sizes = [
    1024, 2048, 4096, 8192, 16384, 32768, 65536, 
    131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608
]

# Ensure valid key length for Twofish
twofish_key = get_valid_key(b"my16bytekeyhere")

# Measure performance
blowfish_encrypt, blowfish_decrypt = measure_time("Blowfish", encrypt_blowfish, decrypt_blowfish, blowfish_key, data_sizes)
twofish_encrypt, twofish_decrypt = measure_time("Twofish", encrypt_twofish, decrypt_twofish, twofish_key, data_sizes)

# Plot the results
plt.figure(figsize=(12, 6))

# Plot the times and adjust y-axis for better visualization
plt.plot(data_sizes, blowfish_encrypt, label="Blowfish Encryption", marker="o", color='blue')
plt.plot(data_sizes, blowfish_decrypt, label="Blowfish Decryption", marker="o", color='red')
plt.plot(data_sizes, twofish_encrypt, label="Twofish Encryption", marker="x", color='green')
plt.plot(data_sizes, twofish_decrypt, label="Twofish Decryption", marker="x", color='purple')

# Add labels and title
plt.xlabel("Data Size (bytes)")
plt.ylabel("Time (picoseconds)")
plt.title("Performance of Blowfish vs Twofish for Large Data Sizes")

# Enable logarithmic scaling for better visibility of larger values
plt.yscale('log')

plt.legend()
plt.grid(True)
plt.show()
