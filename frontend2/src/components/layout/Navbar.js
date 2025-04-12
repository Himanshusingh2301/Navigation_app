import React from 'react';
import { Link } from 'react-router-dom';
const Navbar = () => (
  <nav style={styles.navbar}>
    {/* Logo on the left */}
    <div style={styles.logo}>
      <img src="your-logo-url-here" alt="Logo" style={styles.logoImage} />
    </div>

    {/* Links on the left */}
    <div style={styles.links}>
      <Link to="/" style={styles.link}>Home</Link>
      <Link to="/map" style={styles.link}>Map</Link>
    </div>

    {/* Buttons (Login and Profile) on the right */}
    <div style={styles.right}>
      <Link to="/login" style={styles.button}>Login</Link>
      <Link to="/profile" style={styles.button}>Profile</Link>
    </div>
    <div style={styles.right}>
      <Link to="/roomDetails" style={styles.button}>RoomDetails</Link>
      <Link to="/map" style={styles.link}>Map</Link>
      
    </div>
  </nav>
);

const styles = {
  navbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px 40px',
    background: 'linear-gradient(90deg, #007bff, #00bcd4)',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    borderRadius: '10px',
    position: 'sticky',
    top: '0',
    zIndex: '1000',
  },
  logo: {
    flex: 1,
  },
  logoImage: {
    height: '40px', // Adjust logo size
  },
  links: {
    flex: 2,
    display: 'flex',
    justifyContent: 'left',
  },
  link: {
    margin: '0 20px',
    textDecoration: 'none',
    color: 'white',
    fontSize: '18px',
    fontWeight: '500',
    textTransform: 'uppercase',
    transition: 'all 0.3s ease',
  },
  linkActive: {
    borderBottom: '2px solid white', // Active link indicator
    paddingBottom: '5px',
  },
  right: {
    display: 'flex',
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  button: {
    margin: '0 15px',
    padding: '12px 25px',
    background: '#ffffff',
    color: '#007bff',
    textDecoration: 'none',
    borderRadius: '30px',
    fontSize: '16px',
    fontWeight: '500',
    border: '2px solid #007bff',
    transition: 'all 0.3s ease',
    textAlign: 'center',
  },
  buttonHover: {
    background: '#007bff',
    color: 'white',
    cursor: 'pointer',
  },
};

// Add hover effect to buttons and links
const NavbarWithHover = () => {
  const handleButtonHover = (e) => {
    e.target.style.background = '#007bff';
    e.target.style.color = 'white';
  };

  const handleButtonLeave = (e) => {
    e.target.style.background = 'white';
    e.target.style.color = '#007bff';
  };

  return (
    <nav style={styles.navbar}>
      <div style={styles.logo}>
        <img src="your-logo-url-here" alt="Logo" style={styles.logoImage} />
      </div>

      <div style={styles.links}>
        <Link to="/" style={styles.link} activeStyle={styles.linkActive}>Home</Link>
        <Link to="/map" style={styles.link} activeStyle={styles.linkActive}>Map</Link>
        <Link to="/roomDetails" style={styles.link} activeStyle={styles.linkActive}>RoomDetails</Link>
        <Link to="/room/feedback" style={styles.link} activeStyle={styles.linkActive}>feedback</Link>
 
      </div>

      <div style={styles.right}>
        <Link
          to="/login"
          style={styles.button}
          onMouseEnter={handleButtonHover}
          onMouseLeave={handleButtonLeave}
        >
          Login
        </Link>
        <Link
          to="/profile"
          style={styles.button}
          onMouseEnter={handleButtonHover}
          onMouseLeave={handleButtonLeave}
        >
          Profile
        </Link>
      </div>
    </nav>
  );
};

export default NavbarWithHover;
