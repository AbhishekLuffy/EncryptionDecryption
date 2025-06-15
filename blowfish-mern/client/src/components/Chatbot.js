import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      text: "Hello! I'm your encryption assistant. How can I help you today?",
      isBot: true
    }
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const commonQuestions = [
    "How do I encrypt text?",
    "How do I decrypt text?",
    "What is Blowfish?",
    "What is Twofish?",
    "How do I view encryption history?"
  ];

  const handleQuestion = (question) => {
    let answer = "";
    switch (question) {
      case "How do I encrypt text?":
        answer = "To encrypt text: 1) Select 'Blowfish' or 'Twofish' algorithm, 2) Enter your text in the input field, 3) Enter your encryption key, 4) Click 'Encrypt'";
        break;
      case "How do I decrypt text?":
        answer = "To decrypt text: 1) Select the same algorithm used for encryption, 2) Paste the encrypted text, 3) Enter the same key used for encryption, 4) Click 'Decrypt'";
        break;
      case "What is Blowfish?":
        answer = "Blowfish is a symmetric-key block cipher that uses a variable-length key from 32 bits to 448 bits. It's known for its speed and security.";
        break;
      case "What is Twofish?":
        answer = "Twofish is a symmetric key block cipher with a block size of 128 bits and key sizes up to 256 bits. It's known for its high security and flexibility.";
        break;
      case "How do I view encryption history?":
        answer = "Your encryption history is automatically displayed in the 'History' section below the encryption form. It shows your recent encryption and decryption operations.";
        break;
      default:
        answer = "I'm not sure about that. Please try asking about encryption, decryption, or the algorithms used.";
    }

    setMessages(prev => [...prev, 
      { text: question, isBot: false },
      { text: answer, isBot: true }
    ]);
  };

  return (
    <div className="chatbot-container">
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>Encryption Assistant</h3>
            <button onClick={() => setIsOpen(false)}>×</button>
          </div>
          <div className="chatbot-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.isBot ? 'bot' : 'user'}`}>
                {message.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="chatbot-suggestions">
            {commonQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuestion(question)}
                className="suggestion-button"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      <button
        className="chatbot-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '×' : '?'}
      </button>
    </div>
  );
};

export default Chatbot; 