import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css'; // External CSS file for styling

const HomePage = () => (
  <div className="home-page">
    <div className="hero-section">
      <h1 className="headline">Welcome to Campus Navigation System</h1>
      <p className="subheading">Find rooms, scan QR codes, and get the shortest paths inside campus.</p>
      <div className="cta-container">
        <Link to="/map" className="cta-button">Explore Map</Link>
      </div>
    </div>
    <div className="image-gallery">
      <img src="https://example.com/navigation-image1.jpg" alt="Campus Map" className="gallery-image" />
      <img src="https://example.com/navigation-image2.jpg" alt="QR Code Scanning" className="gallery-image" />
    </div>
  </div>
);

export default HomePage;
