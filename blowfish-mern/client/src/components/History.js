import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './History.css';

const History = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    // For demo purposes, using a simple password. In production, use proper authentication
    if (password === 'encrypt123') {
      setIsAuthenticated(true);
      setError('');
      fetchHistory();
    } else {
      setError('Incorrect password');
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/history');
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
      setError('Failed to fetch history');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="history-container">
        <div className="history-auth">
          <h2>View Encryption History</h2>
          <form onSubmit={handlePasswordSubmit}>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
            <button type="submit">View History</button>
          </form>
          {error && <p className="error">{error}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Encryption History</h2>
        <button onClick={() => setIsAuthenticated(false)}>Logout</button>
      </div>
      <div className="history-list">
        {history.length === 0 ? (
          <p>No history available</p>
        ) : (
          history.map((item, index) => (
            <div key={index} className="history-item">
              <div className="history-item-header">
                <span className="algorithm">{item.algorithm}</span>
                <span className="timestamp">{new Date(item.timestamp).toLocaleString()}</span>
              </div>
              <div className="history-item-content">
                <p><strong>Original Text:</strong> {item.plainText}</p>
                <p><strong>Encrypted Text:</strong> {item.encryptedText}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default History; 