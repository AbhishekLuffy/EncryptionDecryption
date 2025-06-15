from flask import Flask, render_template, request, url_for
from BlowFish import encrypt_blowfish, decrypt_blowfish, plot_performance_metrics
import time
import tracemalloc
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        result = None
        performance_metrics = None
        graph_path = None
        text = None
        key = None

        if request.method == 'POST':
            text = request.form.get('text', '')
            key = request.form.get('key', 'mysecretkey123')
            action = request.form.get('action')
            logger.debug(f"Received POST request - Action: {action}, Text length: {len(text)}")

            if action == 'encrypt':
                # Measure encryption
                tracemalloc.start()
                start_encrypt = time.time()
                encrypted_bytes, encrypted_text = encrypt_blowfish(key.encode(), text)
                end_encrypt = time.time()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                result = encrypted_text
                performance_metrics = {
                    'encrypt_time': f"{end_encrypt - start_encrypt:.8f}",
                    'encrypt_memory': f"{peak / 1024:.2f}"
                }

            elif action == 'decrypt':
                # Measure decryption
                tracemalloc.start()
                start_decrypt = time.time()
                decrypted_text = decrypt_blowfish(key.encode(), text)
                end_decrypt = time.time()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                result = decrypted_text
                performance_metrics = {
                    'decrypt_time': f"{end_decrypt - start_decrypt:.8f}",
                    'decrypt_memory': f"{peak / 1024:.2f}"
                }

            elif action == 'analyze':
                # Test with different input sizes
                input_sizes = []
                encrypt_times = []
                decrypt_times = []
                encrypt_memory = []
                decrypt_memory = []

                test_sizes = [16, 64, 256, 1024, 4096]  # bytes
                
                for size in test_sizes:
                    plaintext = "A" * size
                    input_sizes.append(size)
                    
                    # Measure encryption
                    tracemalloc.start()
                    start_encrypt = time.time()
                    encrypted_bytes, encrypted_text = encrypt_blowfish(key.encode(), plaintext)
                    end_encrypt = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    encrypt_times.append(end_encrypt - start_encrypt)
                    encrypt_memory.append(peak / 1024)
                    
                    # Measure decryption
                    tracemalloc.start()
                    start_decrypt = time.time()
                    decrypted_text = decrypt_blowfish(key.encode(), encrypted_text)
                    end_decrypt = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    decrypt_times.append(end_decrypt - start_decrypt)
                    decrypt_memory.append(peak / 1024)

                # Generate performance graphs
                plot_performance_metrics(encrypt_times, decrypt_times, encrypt_memory, decrypt_memory, input_sizes)
                graph_path = url_for('static', filename='blowfish_performance.png')

        logger.debug("Rendering template with data")
        return render_template('index.html', 
                             result=result,
                             performance_metrics=performance_metrics,
                             graph_path=graph_path,
                             text=text,
                             key=key)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}", exc_info=True)
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5000) 