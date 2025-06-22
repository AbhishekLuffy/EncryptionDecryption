# ✅ Blowfish vs Twofish Benchmark Script
# This script compares the performance of Blowfish and Twofish encryption algorithms

from BlowFish import encrypt_blowfish, decrypt_blowfish
from twofish_impl import encrypt_twofish, decrypt_twofish
import time
import matplotlib.pyplot as plt
import random
import string
import numpy as np

def generate_random_text(length):
    """Generate random text of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def benchmark_algorithm(algorithm_name, encrypt_func, decrypt_func, key, data_sizes, custom_text=None):
    """Benchmark encryption and decryption performance for given algorithm."""
    encryption_times = []
    decryption_times = []
    
    print(f"\n🔍 Benchmarking {algorithm_name}...")
    
    for i, size in enumerate(data_sizes):
        if custom_text and i == 0:  # Use custom text for first test
            plaintext = custom_text
            print(f"  Using custom text (length: {len(plaintext)} bytes)")
        else:
            plaintext = generate_random_text(size)
        
        # Encryption Time
        start = time.time()
        if algorithm_name == "Blowfish":
            encrypted_bytes, encrypted_text = encrypt_func(key, plaintext)
        else:  # Twofish
            encrypted_bytes, encrypted_text = encrypt_func(key, plaintext)
        end = time.time()
        encryption_times.append(end - start)
        
        # Decryption Time
        start = time.time()
        decrypted_text = decrypt_func(key, encrypted_text)
        end = time.time()
        decryption_times.append(end - start)
        
        # Verify decryption
        if decrypted_text != plaintext:
            print(f"⚠️  Warning: Decryption verification failed for {algorithm_name} at size {size}")
        
        print(f"  Size {len(plaintext):5d} bytes: Encrypt={encryption_times[-1]:.6f}s, Decrypt={decryption_times[-1]:.6f}s")
    
    return encryption_times, decryption_times

def plot_comparison(data_sizes, blowfish_enc, blowfish_dec, twofish_enc, twofish_dec):
    """Create performance comparison plots."""
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Encryption Times
    ax1.plot(data_sizes, blowfish_enc, 'b-o', label='Blowfish Encrypt', linewidth=2, markersize=6)
    ax1.plot(data_sizes, twofish_enc, 'r-s', label='Twofish Encrypt', linewidth=2, markersize=6)
    ax1.set_xlabel('Data Size (bytes)', fontsize=12)
    ax1.set_ylabel('Time (seconds)', fontsize=12)
    ax1.set_title('Encryption Performance Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Plot 2: Decryption Times
    ax2.plot(data_sizes, blowfish_dec, 'b-o', label='Blowfish Decrypt', linewidth=2, markersize=6)
    ax2.plot(data_sizes, twofish_dec, 'r-s', label='Twofish Decrypt', linewidth=2, markersize=6)
    ax2.set_xlabel('Data Size (bytes)', fontsize=12)
    ax2.set_ylabel('Time (seconds)', fontsize=12)
    ax2.set_title('Decryption Performance Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('blowfish_vs_twofish_benchmark.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Performance comparison chart saved as 'blowfish_vs_twofish_benchmark.png'")

def print_summary(data_sizes, blowfish_enc, blowfish_dec, twofish_enc, twofish_dec):
    """Print a summary of the benchmark results."""
    print("\n" + "="*60)
    print("📈 BENCHMARK SUMMARY")
    print("="*60)
    
    print(f"{'Size (bytes)':<12} {'Blowfish Enc':<12} {'Blowfish Dec':<12} {'Twofish Enc':<12} {'Twofish Dec':<12}")
    print("-" * 60)
    
    for i, size in enumerate(data_sizes):
        print(f"{size:<12} {blowfish_enc[i]:<12.6f} {blowfish_dec[i]:<12.6f} {twofish_enc[i]:<12.6f} {twofish_dec[i]:<12.6f}")
    
    # Calculate averages
    avg_blow_enc = np.mean(blowfish_enc)
    avg_blow_dec = np.mean(blowfish_dec)
    avg_two_enc = np.mean(twofish_enc)
    avg_two_dec = np.mean(twofish_dec)
    
    print("-" * 60)
    print(f"{'AVERAGE':<12} {avg_blow_enc:<12.6f} {avg_blow_dec:<12.6f} {avg_two_enc:<12.6f} {avg_two_dec:<12.6f}")
    
    # Performance comparison
    print("\n🏆 PERFORMANCE COMPARISON:")
    if avg_blow_enc < avg_two_enc:
        print(f"  • Blowfish encryption is {avg_two_enc/avg_blow_enc:.2f}x faster than Twofish")
    else:
        print(f"  • Twofish encryption is {avg_blow_enc/avg_two_enc:.2f}x faster than Blowfish")
    
    if avg_blow_dec < avg_two_dec:
        print(f"  • Blowfish decryption is {avg_two_dec/avg_blow_dec:.2f}x faster than Twofish")
    else:
        print(f"  • Twofish decryption is {avg_blow_dec/avg_two_dec:.2f}x faster than Blowfish")

def main():
    """Main benchmark function."""
    print("🚀 Starting Blowfish vs Twofish Performance Benchmark")
    print("=" * 60)
    
    # Get custom plaintext from user
    custom_text = input("Enter your plaintext to test (or press Enter for random data): ").strip()
    if not custom_text:
        custom_text = None
        print("Using random data for all tests")
    else:
        print(f"Using custom text: '{custom_text}' (length: {len(custom_text)} bytes)")
    
    # Define test parameters
    if custom_text:
        # Use custom text length and generate sizes around it
        custom_length = len(custom_text)
        data_sizes = [custom_length]
        # Add some additional sizes for comparison
        if custom_length < 500:
            data_sizes.extend([500, 1000, 5000])
        elif custom_length < 1000:
            data_sizes.extend([1000, 5000, 10000])
        else:
            data_sizes.extend([custom_length * 2, custom_length * 5, custom_length * 10])
    else:
        data_sizes = [100, 500, 1000, 5000, 10000, 20000]
    
    key_blowfish = b"mysecretkey12345"             # 16 bytes for Blowfish
    key_twofish = b"mysecretkey1234567890abcd"     # 24 bytes for Twofish
    
    print(f"📊 Testing data sizes: {data_sizes}")
    print(f"🔑 Blowfish key length: {len(key_blowfish)} bytes")
    print(f"🔑 Twofish key length: {len(key_twofish)} bytes")
    
    # Run benchmarks
    blowfish_enc, blowfish_dec = benchmark_algorithm(
        "Blowfish", encrypt_blowfish, decrypt_blowfish, key_blowfish, data_sizes, custom_text
    )
    
    twofish_enc, twofish_dec = benchmark_algorithm(
        "Twofish", encrypt_twofish, decrypt_twofish, key_twofish, data_sizes, custom_text
    )
    
    # Generate plots and summary
    plot_comparison(data_sizes, blowfish_enc, blowfish_dec, twofish_enc, twofish_dec)
    print_summary(data_sizes, blowfish_enc, blowfish_dec, twofish_enc, twofish_dec)
    
    print("\n✅ Benchmark completed successfully!")

if __name__ == "__main__":
    main() 