// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home, Callback, Chat, ChatRoom
} from './pages';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/callback" element={<Callback />} />
        <Route path="/chat" element={<ChatRoom />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
