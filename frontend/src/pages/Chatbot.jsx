import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchChatHistory = async () => {
    try {
      const response = await api.get('/chatbot/history');
      setMessages(response.data.messages);
    } catch (err) {
      console.error('Failed to fetch chat history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setLoading(true);

    // Add user message optimistically
    const tempUserMsg = {
      message: userMessage,
      sender: 'user',
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const response = await api.post('/chatbot/send', { message: userMessage });
      
      // Replace temp message with actual response
      setMessages(prev => {
        const withoutTemp = prev.slice(0, -1);
        return [
          ...withoutTemp,
          response.data.user_message,
          response.data.bot_message
        ];
      });
    } catch (err) {
      console.error('Failed to send message:', err);
      // Remove optimistic message on error
      setMessages(prev => prev.slice(0, -1));
      alert('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (!window.confirm('Are you sure you want to clear your chat history?')) {
      return;
    }

    try {
      await api.delete('/chatbot/clear');
      setMessages([]);
    } catch (err) {
      console.error('Failed to clear history:', err);
      alert('Failed to clear chat history');
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (loadingHistory) {
    return (
      <div className="page-container">
        <LoadingSpinner message="Loading chat history..." />
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="chatbot-page">
        <div className="chatbot-header">
          <h1>AI Coding Assistant</h1>
          <button 
            onClick={handleClearHistory} 
            className="btn btn-danger btn-small"
            disabled={messages.length === 0}
          >
            Clear History
          </button>
        </div>

        <div className="chat-container">
          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="empty-chat">
                <div className="empty-icon">💬</div>
                <h3>Start a conversation</h3>
                <p>Ask me anything about programming, debugging, or code best practices!</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div 
                  key={index} 
                  className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
                >
                  <div className="message-content">
                    <div className="message-text">{msg.message}</div>
                    <div className="message-time">
                      {formatTimestamp(msg.created_at)}
                    </div>
                  </div>
                </div>
              ))
            )}
            
            {loading && (
              <div className="message bot-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSendMessage} className="chat-input-form">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your question here..."
              disabled={loading}
              className="chat-input"
            />
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading || !inputMessage.trim()}
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
