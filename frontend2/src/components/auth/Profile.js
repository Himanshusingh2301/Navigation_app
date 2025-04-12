import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';
import './Profile.css';
const Register = () => {
  const [userInfo, setUserInfo] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const { registerUser } = useContext(AuthContext); // ✅ Access from context

  const handleChange = (e) => {
    setUserInfo({ ...userInfo, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await registerUser(userInfo.username, userInfo.password); // email optional depending on backend
    if (success) {
      navigate('/login');
    } else {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="register-container">
      <h2 className="register-title">Create Account</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit} className="register-form">
        <div className="input-container">
          <input
            type="text"
            name="username"
            placeholder="Username"
            onChange={handleChange}
            required
            className="input-field"
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            onChange={handleChange}
            required
            className="input-field"
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            required
            className="input-field"
          />
        </div>
        <button
          type="submit"
          className="submit-button"
        >
          Register
        </button>
      </form>
      <div className="login-link">
        <p>
          Already have an account?{' '}
          <a href="/login" className="login-text">
            Login here
          </a>
        </p>
      </div>
    </div>
  );
};

export default Register;
