import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // API call to Flask backend
      const response = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue.trim() })
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = {
          id: Date.now() + 1,
          type: 'assistant',
          content: data.response,
          sources: data.sources || [],
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };



  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <img 
              src="/University_of_Chicago_shield.svg.png" 
              alt="University of Chicago Shield" 
              className="uchicago-shield"
            />
            <div className="header-text">
              <h1>UChicago ADS AI Assistant</h1>
              <p>Your intelligent guide to the MS-ADS program</p>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="chat-container">
        {/* Welcome Message */}
        <div className="welcome-message">
          <h2>Hello! I'm your AI assistant.</h2>
          <p>I can help you with questions about the UChicago Master of Science in Applied Data Science program. Ask me about courses, admissions, career opportunities, and more!</p>
        </div>

        {/* Messages */}
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}-message`}>
            {message.type === 'assistant' && (
              <div className="assistant-icon">
                <img 
                  src="/Phoenix.png" 
                  alt="UChicago Phoenix" 
                  className="phoenix-icon"
                />
              </div>
            )}
            <div className="message-content">
              {message.content}
            </div>
            {message.sources && message.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                {[...new Set(message.sources)].map((source, index) => (
                  <div key={index} className="source-item">• {source}</div>
                ))}
              </div>
            )}
            <div className="message-timestamp">{message.timestamp}</div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="message assistant-message">
            <div className="loading-indicator">
              <span>AI is thinking</span>
              <div className="dots">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-area">
        <form onSubmit={handleSubmit} className="input-form">
          <div className="input-container">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="message-input"
            />
            <button 
              type="submit" 
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              ➤
            </button>
          </div>
        </form>
      </div>


    </div>
  );
}

export default App; 