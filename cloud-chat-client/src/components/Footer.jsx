import React from "react";
import "./Footer.css";

const Footer = () => (
  <footer className="footer">
    <div className="footer-content">
      <div className="footer-links">
        <div className="footer-section">
          <a href="#">About Us</a>
          <a href="#">Jobs</a>
          <a href="#">Press</a>
          <a href="#">Blog</a>
        </div>
        <div className="footer-section">
          <a href="#">Contact Us</a>
          <a href="#">Terms</a>
          <a href="#">Privacy</a>
        </div>
        <div className="footer-section">
          <div className="footer-contact">
            <p>+1-543-123-4567</p>
            <p>example@connect.com</p>
          </div>
        </div>
      </div>
      <div className="footer-socials">
        <a href="#" aria-label="Facebook">
          <i className="fa-brands fa-facebook"></i>
        </a>
        <a href="#" aria-label="Twitter">
          <i className="fa-brands fa-twitter"></i>
        </a>
        <a href="#" aria-label="Instagram">
          <i className="fa-brands fa-instagram"></i>
        </a>
      </div>
    </div>
  </footer>
);

export default Footer;