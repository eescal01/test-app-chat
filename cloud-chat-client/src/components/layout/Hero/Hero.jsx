import React from "react";
import assets from "../../../assets/assets";
import "./Hero.css";
import HeaderNav from "../Header";
import Footer from "../Footer";
import { login } from '../../../utils/google_auth_login';

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
          <button className="hero-btn" onClick={login}>
            Try the App
          </button>
        </div>
      </div>
    </div>
    <Footer />
  </>
);

export default CommunityHero; 