// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // Correct named import

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('accessToken'));
  const [user, setUser] = useState(token ? jwtDecode(token) : null);

  // Sync user state with token
  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setUser(decoded);
      } catch (error) {
        console.error("Token decoding failed:", error);
        logout();
      }
    } else {
      setUser(null);
    }
  }, [token]);

  // LOGIN
  const login = async (username, password) => {
    try {
      const response = await axios.post('https://nav-app-back.onrender.com/api/token/', {
        username,
        password,
      });

      const { access, refresh } = response.data;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      setToken(access);
      setUser(jwtDecode(access));
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  // LOGOUT
  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setToken(null);
    setUser(null);
  };

  // REGISTER
  const registerUser = async (username, password) => {
    try {
      const response = await axios.post('https://nav-app-back.onrender.com/api/register/', {
        username,
        password,
      });

      if (response.status === 201 || response.status === 200) {
        // auto-login after registration
        return await login(username, password);
      }

      return false;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout, registerUser }}>
      {children}
    </AuthContext.Provider>
  );
};
