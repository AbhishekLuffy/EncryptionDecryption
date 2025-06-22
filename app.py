from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from BlowFish import encrypt_blowfish, decrypt_blowfish, plot_performance_metrics
import time
import tracemalloc
import os
import logging
from twofish_impl import encrypt_twofish, decrypt_twofish
import importlib.util
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
    static_folder='static',
    template_folder='templates',
    static_url_path='/static')

# Configure Flask app
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for session management

# Ensure static and templates directories exist
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

def create_performance_graphs(blowfish_data, twofish_data):
    """Create performance comparison graphs with dark theme"""
    # Set dark theme for matplotlib
    plt.style.use('dark_background')
    
    # Create figure with dark background
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.patch.set_facecolor('#0a0e1a')
    fig.suptitle('Blowfish vs Twofish Performance Comparison', fontsize=16, fontweight='bold', color='#f8fafc')
    
    # Extract data
    algorithms = ['Blowfish', 'Twofish']
    times = [blowfish_data.get('time', 0), twofish_data.get('time', 0)]
    memory_usage = [blowfish_data.get('memory', 0), twofish_data.get('memory', 0)]
    text_lengths = [blowfish_data.get('text_length', 0), twofish_data.get('text_length', 0)]
    key_lengths = [blowfish_data.get('key_length', 0), twofish_data.get('key_length', 0)]
    
    # Define cyber colors
    cyber_blue = '#00d4ff'
    cyber_purple = '#7c3aed'
    cyber_green = '#10b981'
    cyber_red = '#ef4444'
    dark_bg = '#1a1f2e'
    light_text = '#f8fafc'
    muted_text = '#cbd5e1'
    
    # Set dark background for all subplots
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_facecolor(dark_bg)
        ax.grid(True, alpha=0.2, color='#334155')
        ax.tick_params(colors=muted_text)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.spines['bottom'].set_color('#334155')
    
    # 1. Processing Time Comparison
    colors = [cyber_blue, cyber_purple]
    bars1 = ax1.bar(algorithms, times, color=colors, alpha=0.8, edgecolor='#334155', linewidth=1)
    ax1.set_title('Processing Time Comparison', fontweight='bold', fontsize=12, color=light_text, pad=20)
    ax1.set_ylabel('Time (seconds)', fontweight='bold', color=light_text)
    ax1.set_xlabel('Algorithm', color=light_text)
    
    # Add value labels on bars
    for bar, time_val in zip(bars1, times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(times)*0.01,
                f'{time_val:.6f}s', ha='center', va='bottom', fontweight='bold', 
                color=light_text, fontsize=10)
    
    # 2. Memory Usage Comparison
    bars2 = ax2.bar(algorithms, memory_usage, color=colors, alpha=0.8, edgecolor='#334155', linewidth=1)
    ax2.set_title('Memory Usage Comparison', fontweight='bold', fontsize=12, color=light_text, pad=20)
    ax2.set_ylabel('Memory (KB)', fontweight='bold', color=light_text)
    ax2.set_xlabel('Algorithm', color=light_text)
    
    for bar, mem_val in zip(bars2, memory_usage):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(memory_usage)*0.01,
                f'{mem_val:.2f} KB', ha='center', va='bottom', fontweight='bold', 
                color=light_text, fontsize=10)
    
    # 3. Speed vs Memory Efficiency
    if times[0] > 0 and times[1] > 0:
        efficiency_blowfish = text_lengths[0] / (times[0] * memory_usage[0]) if memory_usage[0] > 0 else 0
        efficiency_twofish = text_lengths[1] / (times[1] * memory_usage[1]) if memory_usage[1] > 0 else 0
        efficiencies = [efficiency_blowfish, efficiency_twofish]
        
        bars3 = ax3.bar(algorithms, efficiencies, color=colors, alpha=0.8, edgecolor='#334155', linewidth=1)
        ax3.set_title('Efficiency (Text Length / Time × Memory)', fontweight='bold', fontsize=12, color=light_text, pad=20)
        ax3.set_ylabel('Efficiency Score', fontweight='bold', color=light_text)
        ax3.set_xlabel('Algorithm', color=light_text)
        
        for bar, eff_val in zip(bars3, efficiencies):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + max(efficiencies)*0.01,
                    f'{eff_val:.2f}', ha='center', va='bottom', fontweight='bold', 
                    color=light_text, fontsize=10)
    else:
        ax3.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center', 
                transform=ax3.transAxes, color=muted_text, fontsize=14)
        ax3.set_title('Efficiency (Text Length / Time × Memory)', fontweight='bold', fontsize=12, color=light_text, pad=20)
    
    # 4. Key Length Comparison
    bars4 = ax4.bar(algorithms, key_lengths, color=colors, alpha=0.8, edgecolor='#334155', linewidth=1)
    ax4.set_title('Key Length Comparison', fontweight='bold', fontsize=12, color=light_text, pad=20)
    ax4.set_ylabel('Key Length (bytes)', fontweight='bold', color=light_text)
    ax4.set_xlabel('Algorithm', color=light_text)
    
    for bar, key_len in zip(bars4, key_lengths):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + max(key_lengths)*0.01,
                f'{key_len} bytes', ha='center', va='bottom', fontweight='bold', 
                color=light_text, fontsize=10)
    
    # Adjust layout with dark theme
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, hspace=0.3, wspace=0.3)
    
    # Save to base64 string
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0e1a', edgecolor='none')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize session variables if they don't exist
    if 'blowfish_result' not in session:
        session['blowfish_result'] = None
        session['blowfish_time'] = None
        session['blowfish_text'] = None
        session['blowfish_key'] = None
        session['blowfish_error'] = None
        session['blowfish_memory'] = None
        
    if 'twofish_result' not in session:
        session['twofish_result'] = None
        session['twofish_time'] = None
        session['twofish_text'] = None
        session['twofish_key'] = None
        session['twofish_error'] = None
        session['twofish_memory'] = None

    performance_graph = None

    if request.method == 'POST':
        algorithm = request.form.get('algorithm')
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        action = request.form.get('action')
        
        logger.debug(f"Received POST request - Algorithm: {algorithm}, Action: {action}, Text length: {len(text)}")

        if algorithm == 'blowfish':
            # Clear previous error
            session['blowfish_error'] = None
            
            try:
                if action == 'encrypt':
                    # Blowfish encryption
                    tracemalloc.start()
                    start_time = time.time()
                    encrypted_bytes, encrypted_text = encrypt_blowfish(key.encode(), text)
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    session['blowfish_result'] = encrypted_text
                    session['blowfish_time'] = f"{end_time - start_time:.6f}"
                    session['blowfish_memory'] = f"{peak / 1024:.2f}"
                    session['blowfish_text'] = text
                    session['blowfish_key'] = key
                    
                elif action == 'decrypt':
                    # Blowfish decryption
                    tracemalloc.start()
                    start_time = time.time()
                    decrypted_text = decrypt_blowfish(key.encode(), text)
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    session['blowfish_result'] = decrypted_text
                    session['blowfish_time'] = f"{end_time - start_time:.6f}"
                    session['blowfish_memory'] = f"{peak / 1024:.2f}"
                    session['blowfish_text'] = text
                    session['blowfish_key'] = key
                    
            except Exception as e:
                logger.error(f"Blowfish error: {str(e)}", exc_info=True)
                session['blowfish_error'] = f"Blowfish {action} error: {str(e)}"
                session['blowfish_result'] = None
                session['blowfish_time'] = None
                session['blowfish_memory'] = None

        elif algorithm == 'twofish':
            # Clear previous error
            session['twofish_error'] = None
            
            try:
                if action == 'encrypt':
                    # Twofish encryption
                    tracemalloc.start()
                    start_time = time.time()
                    encrypted_bytes, encrypted_text = encrypt_twofish(key.encode(), text)
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    session['twofish_result'] = encrypted_text
                    session['twofish_time'] = f"{end_time - start_time:.6f}"
                    session['twofish_memory'] = f"{peak / 1024:.2f}"
                    session['twofish_text'] = text
                    session['twofish_key'] = key
                    
                elif action == 'decrypt':
                    # Twofish decryption
                    tracemalloc.start()
                    start_time = time.time()
                    decrypted_text = decrypt_twofish(key.encode(), text)
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    session['twofish_result'] = decrypted_text
                    session['twofish_time'] = f"{end_time - start_time:.6f}"
                    session['twofish_memory'] = f"{peak / 1024:.2f}"
                    session['twofish_text'] = text
                    session['twofish_key'] = key
                    
            except Exception as e:
                logger.error(f"Twofish error: {str(e)}", exc_info=True)
                session['twofish_error'] = f"Twofish {action} error: {str(e)}"
                session['twofish_result'] = None
                session['twofish_time'] = None
                session['twofish_memory'] = None

        # Generate performance graph if both algorithms have results
        if (session.get('blowfish_result') and session.get('twofish_result') and 
            session.get('blowfish_time') and session.get('twofish_time')):
            
            blowfish_data = {
                'time': float(session.get('blowfish_time', 0)),
                'memory': float(session.get('blowfish_memory', 0)),
                'text_length': len(session.get('blowfish_text', '')),
                'key_length': len(session.get('blowfish_key', ''))
            }
            
            twofish_data = {
                'time': float(session.get('twofish_time', 0)),
                'memory': float(session.get('twofish_memory', 0)),
                'text_length': len(session.get('twofish_text', '')),
                'key_length': len(session.get('twofish_key', ''))
            }
            
            performance_graph = create_performance_graphs(blowfish_data, twofish_data)

    logger.debug("Rendering template with data")
    return render_template('index.html', 
                         blowfish_result=session.get('blowfish_result'),
                         blowfish_time=session.get('blowfish_time'),
                         blowfish_memory=session.get('blowfish_memory'),
                         blowfish_text=session.get('blowfish_text'),
                         blowfish_key=session.get('blowfish_key'),
                         blowfish_error=session.get('blowfish_error'),
                         twofish_result=session.get('twofish_result'),
                         twofish_time=session.get('twofish_time'),
                         twofish_memory=session.get('twofish_memory'),
                         twofish_text=session.get('twofish_text'),
                         twofish_key=session.get('twofish_key'),
                         twofish_error=session.get('twofish_error'),
                         performance_graph=performance_graph)

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    """Generate performance graph via AJAX"""
    try:
        blowfish_data = {
            'time': float(request.json.get('blowfish_time', 0)),
            'memory': float(request.json.get('blowfish_memory', 0)),
            'text_length': int(request.json.get('blowfish_text_length', 0)),
            'key_length': int(request.json.get('blowfish_key_length', 0))
        }
        
        twofish_data = {
            'time': float(request.json.get('twofish_time', 0)),
            'memory': float(request.json.get('twofish_memory', 0)),
            'text_length': int(request.json.get('twofish_text_length', 0)),
            'key_length': int(request.json.get('twofish_key_length', 0))
        }
        
        graph_data = create_performance_graphs(blowfish_data, twofish_data)
        return jsonify({'success': True, 'graph': graph_data})
    except Exception as e:
        logger.error(f"Graph generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear', methods=['POST'])
def clear_results():
    """Clear all stored results"""
    session['blowfish_result'] = None
    session['blowfish_time'] = None
    session['blowfish_memory'] = None
    session['blowfish_text'] = None
    session['blowfish_key'] = None
    session['blowfish_error'] = None
    session['twofish_result'] = None
    session['twofish_time'] = None
    session['twofish_memory'] = None
    session['twofish_text'] = None
    session['twofish_key'] = None
    session['twofish_error'] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 