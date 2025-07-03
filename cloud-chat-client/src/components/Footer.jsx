import React from "react";
import "./Footer.css";

const Footer = () => (
  <footer className="footer">
    <div className="footer-main">
      <div className="footer-description">
        <p>
          Connect IO is a cutting-edge cloud-based web service built for modern communities. Deployed using Infrastructure as Code (IaC) principles, our platform ensures scalable, reliable, and secure communication solutions for teams and organizations worldwide.
        </p>
      </div>
      
      <div className="footer-links-group">
        <div className="footer-column">
          <a href="#">About Us</a>
          <a href="#">Pricing</a>
          <a href="#">Features</a>
          <a href="#">Blog</a>
        </div>
        
        <div className="footer-column">
          <a href="#">Contact Us</a>
          <a href="#">Terms</a>
          <a href="#">Privacy</a>
        </div>
      </div>
      
      <div className="footer-contact">
        <p>+1-123-456-7891</p>
        <p>support@connectio.com</p>
      </div>
      
      <div className="footer-socials">
        <a href="#" aria-label="Facebook">
          <i className="fa-brands fa-facebook"></i>
        </a>
        <a href="#" aria-label="twitter">
          <i className="fa-brands fa-twitter"></i>
        </a>
        <a href="#" aria-label="Instagram">
          <i className="fa-brands fa-instagram"></i>
        </a>
      </div>
    </div>
    <div className="footer-copyright">©2025 Connect IO</div>
  </footer>
);

export default Footer;