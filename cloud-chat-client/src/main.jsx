// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import Callback from './Callback';
import ChatRoom from './ChatRoom';
import Login from './pages/login/Login';
import CommunityHero from './components/Hero';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/callback" element={<Callback />} />
        <Route path="/chat" element={<ChatRoom />} />
        <Route path="/login" element={<Login />} />
        <Route path="/Hero" element={<CommunityHero />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
