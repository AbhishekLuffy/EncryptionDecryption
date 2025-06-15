const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
require('dotenv').config();
const mongoose = require('mongoose');

// MongoDB Connection
console.log('Attempting to connect to MongoDB...');
mongoose.connect('mongodb://localhost:27017/encryption-app')
  .then(() => {
    console.log('Connected to MongoDB successfully');
    console.log('MongoDB connection state:', mongoose.connection.readyState);
    // Start the server only after MongoDB connects
    const PORT = process.env.PORT || 5001;
    app.listen(PORT, '0.0.0.0', () => {
      console.log(`Server running on port ${PORT}`);
      console.log(`Server accessible at http://0.0.0.0:${PORT}`);
    });
  })
  .catch(err => {
    console.error('MongoDB connection error:', err);
    console.error('MongoDB connection error details:', {
      name: err.name,
      message: err.message,
      code: err.code,
      stack: err.stack
    });
    process.exit(1);
  });

const app = express();

// CORS configuration for production
app.use(cors({
  origin: process.env.CLIENT_URL || '*',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Accept'],
  credentials: true
}));

// Middleware
app.use(express.json());

// Add headers middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', process.env.CLIENT_URL || '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Accept');
  next();
});

// Add a test route
app.get('/', (req, res) => {
  res.json({ message: 'Server is running' });
});

// Python script paths
const blowfishScript = path.join(__dirname, 'blowfish.py');
const twofishScript = path.join(__dirname, 'twofish_encrypt.py');

// Helper function to run Python script
function runPythonScript(scriptPath, args) {
  return new Promise((resolve, reject) => {
    console.log('Running Python script with args:', args);
    const pythonProcess = spawn('python3', [scriptPath, ...args]);
    let result = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
      console.log('Python stdout:', data.toString());
      result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Python stderr:', data.toString());
      error += data.toString();
    });

    pythonProcess.on('close', (code) => {
      console.log('Python process exited with code:', code);
      if (code !== 0) {
        reject(new Error(`Python script failed: ${error}`));
      } else {
        resolve(result.trim());
      }
    });
  });
}

// Add this after your existing mongoose schema definitions
const historySchema = new mongoose.Schema({
  algorithm: String,
  plainText: String,
  encryptedText: String,
  timestamp: { type: Date, default: Date.now }
});

const History = mongoose.model('History', historySchema);

// Add these new routes before your existing routes
app.get('/api/history', async (req, res) => {
  console.log('History fetch request received');
  try {
    console.log('Attempting to fetch history from MongoDB...');
    const history = await History.find().sort({ timestamp: -1 });
    console.log('History fetch successful, found entries:', history.length);
    res.json(history);
  } catch (error) {
    console.error('Error fetching history:', error);
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    });
    res.status(500).json({ error: 'Failed to fetch history' });
  }
});

// Modify your existing encrypt route to save history
app.post('/api/encrypt', async (req, res) => {
  const { text, key, algorithm } = req.body;
  console.log('Encrypt request received:', { text, algorithm });
  
  try {
    let result;
    if (algorithm === 'blowfish') {
      console.log('Using Blowfish algorithm');
      result = await runPythonScript(blowfishScript, ['encrypt', text, key]);
    } else if (algorithm === 'twofish') {
      console.log('Using Twofish algorithm');
      result = await runPythonScript(twofishScript, ['encrypt', text, key]);
    }

    console.log('Encryption successful:', result);

    // Save to history
    console.log('Attempting to save to history...');
    const historyEntry = new History({
      algorithm,
      plainText: text,
      encryptedText: result
    });
    console.log('History entry created:', historyEntry);
    
    await historyEntry.save();
    console.log('History entry saved successfully');

    res.json({ result });
  } catch (error) {
    console.error('Encryption error:', error);
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    });
    res.status(500).json({ error: error.message });
  }
});

// Routes
app.post('/api/blowfish/encrypt', async (req, res) => {
  try {
    console.log('Blowfish encrypt request received:', req.body);
    const { text, key } = req.body;
    if (!text || !key) {
      throw new Error('Text and key are required');
    }
    const encryptedText = await runPythonScript(blowfishScript, ['encrypt', text, key]);
    console.log('Blowfish encryption successful:', encryptedText);
    res.json({ encryptedText });
  } catch (error) {
    console.error('Blowfish encryption error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/blowfish/decrypt', async (req, res) => {
  try {
    console.log('Blowfish decrypt request received:', req.body);
    const { text, key } = req.body;
    if (!text || !key) {
      throw new Error('Text and key are required');
    }
    const decryptedText = await runPythonScript(blowfishScript, ['decrypt', text, key]);
    console.log('Blowfish decryption successful:', decryptedText);
    res.json({ decryptedText });
  } catch (error) {
    console.error('Blowfish decryption error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/twofish/encrypt', async (req, res) => {
  try {
    console.log('Twofish encrypt request received:', req.body);
    const { text, key } = req.body;
    if (!text || !key) {
      throw new Error('Text and key are required');
    }
    if (key.length < 16) {
      throw new Error('Key must be at least 16 characters long for Twofish');
    }
    const encryptedText = await runPythonScript(twofishScript, ['encrypt', text, key]);
    console.log('Twofish encryption successful:', encryptedText);
    res.json({ encryptedText });
  } catch (error) {
    console.error('Twofish encryption error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/twofish/decrypt', async (req, res) => {
  try {
    console.log('Twofish decrypt request received:', req.body);
    const { text, key } = req.body;
    if (!text || !key) {
      throw new Error('Text and key are required');
    }
    if (key.length < 16) {
      throw new Error('Key must be at least 16 characters long for Twofish');
    }
    const decryptedText = await runPythonScript(twofishScript, ['decrypt', text, key]);
    console.log('Twofish decryption successful:', decryptedText);
    res.json({ decryptedText });
  } catch (error) {
    console.error('Twofish decryption error:', error);
    res.status(500).json({ error: error.message });
  }
}); 