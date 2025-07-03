import React from "react";
import logo from "../assets/react.svg";
import "./Header.css";
import { login } from '../utils/google_auth_login';

const HeaderNav = () => (
  <header className="header-nav">
    <div className="nav-logo">
      <img src={logo} alt="Logo" />
      <span>Connect IO</span>
    </div>
    <nav className="nav-links">
      <a href="#">Product</a>
      <a href="#">Support</a>
      <a href="#">Pricing</a>
      <a href="#">Blog</a>
      <button className="nav-btn" onClick={login}>Try the App</button>
    </nav>
    {/* Menú hamburguesa para móviles */}
    <input type="checkbox" id="nav-toggle" className="nav-toggle" />
    <label htmlFor="nav-toggle" className="nav-toggle-label">
      <span></span>
    </label>
    <div className="nav-mobile">
      <a href="#">Product</a>
      <a href="#">Download</a>
      <a href="#">Safety</a>
      <a href="#">Support</a>
      <button className="nav-btn">Try the App</button>
    </div>
  </header>
);

export default HeaderNav;