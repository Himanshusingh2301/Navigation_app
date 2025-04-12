// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import MapComponent from './components/navigation/MapComponent';
import Login from './components/auth/Login';
import Profile from './components/auth/Profile';
import RoomDetails from './components/RoomDetails';
import FeedbackPage from './components/FeedbackPage';
import HomePage from './components/HomePage';
import { AuthProvider } from './components/auth/AuthContext';

const App = () => (
  <AuthProvider>
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/map" element={<MapComponent />} />
        <Route path="/roomDetails" element={<RoomDetails />} />
        <Route path="/room/feedback" element={<FeedbackPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
  </AuthProvider>
);

export default App;
