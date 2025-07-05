import React, { useState } from 'react';
import './ChatRoom.css';
import { chatData } from '../../utils/chatData';

const ChatRoom = () => {
  const [activeUser, setActiveUser] = useState(chatData.users.find(user => user.isActive));
  const [messages, setMessages] = useState(chatData.messages);
  const [newMessage, setNewMessage] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      const message = {
        id: Date.now().toString(),
        senderId: chatData.currentUser.id,
        text: newMessage,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        type: 'sent'
      };
      setMessages([...messages, message]);
      setNewMessage('');
    }
  };

  const handleUserSelect = (user) => {
    setActiveUser(user);
    setIsSidebarOpen(false);
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="chatroom-container">
      {/* Mobile Menu Button */}
      <button 
        className="mobile-menu-btn"
        onClick={toggleSidebar}
        aria-label="Toggle sidebar"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Sidebar */}
      <div className={`chatroom-sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="app-logo">
            <div className="logo-icon">💬</div>
            <span>Chatapp</span>
          </div>
          <button className="menu-dots">⋮</button>
        </div>
        
        <div className="search-container">
          <input 
            type="text" 
            placeholder="Search here..." 
            className="search-input"
          />
        </div>

        <div className="users-list">
          {chatData.users.map(user => (
            <div 
              key={user.id}
              className={`user-item ${user.isActive ? 'active' : ''}`}
              onClick={() => handleUserSelect(user)}
            >
              <img src={user.avatar} alt={user.name} className="user-avatar" />
              <div className="user-info">
                <h4>{user.name}</h4>
                <p>{user.lastMessage}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chatroom-main">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="chat-user-info">
            <img src={activeUser?.avatar} alt={activeUser?.name} className="header-avatar" />
            <div>
              <h3>{activeUser?.name}</h3>
              <span className="status online">●</span>
            </div>
          </div>
          <button className="info-btn">ℹ</button>
        </div>

        {/* Messages Area */}
        <div className="messages-container">
          {messages.map(message => (
            <div 
              key={message.id}
              className={`message ${message.type}`}
            >
              <div className="message-content">
                {message.isImage ? (
                  <img src={message.text} alt="Shared image" className="message-image" />
                ) : (
                  <p>{message.text}</p>
                )}
              </div>
              <span className="message-time">{message.timestamp}</span>
            </div>
          ))}
        </div>

        {/* Message Input */}
        <form className="message-input-container" onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Send a message"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            className="message-input"
          />
          <button type="button" className="attachment-btn">📎</button>
          <button type="submit" className="send-btn">➤</button>
        </form>
      </div>

      {/* Sidebar Overlay */}
      {isSidebarOpen && <div className="sidebar-overlay" onClick={toggleSidebar}></div>}
    </div>
  );
};

export default ChatRoom; 