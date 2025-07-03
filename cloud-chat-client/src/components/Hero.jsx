import React from "react";
import assets from "../assets/assets";
import "./Hero.css";
import HeaderNav from "./Header";
import { login } from '../utils/google_auth_login';

const CommunityHero = () => (
  <>
    <HeaderNav />
    <div className="hero-container">
      <div
        className="hero-background"
        style={{ backgroundImage: `url(${assets.background})` }}
      >
        <div className="hero-content">
          <h1>Connect with your community</h1>
          <p>
            Connect is where you can make a home for your communities and
            friends. Where you can stay close and have fun over text, voice, and
            video.
          </p>
          <button className="hero-btn" onClick={login}>Try the App</button>
        </div>
      </div>
      <footer className="hero-footer">
        <div className="hero-socials">
          <a href="#">
            <i className="fa-brands fa-twitter"></i>
          </a>
          <a href="#">
            <i className="fa-brands fa-instagram"></i>
          </a>
          <a href="#">
            <i className="fa-brands fa-facebook"></i>
          </a>
        </div>
        <div className="hero-copyright">©2025 Connect</div>
      </footer>
    </div>
  </>
);

export default CommunityHero;
