import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const RoomDetails = () => {
  const [roomId, setRoomId] = useState('');
  const [room, setRoom] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();  // React Router navigation hook

  const fetchRoomDetails = () => {
    if (!roomId) return;
    setLoading(true);
    setError(null);
    setRoom(null);

    axios.get(`http://localhost:8000/api/rooms/${roomId}/`)
      .then(response => {
        setRoom(response.data);
      })
      .catch(error => {
        console.error('Error fetching room details:', error);
        setError('Room not found or an error occurred.');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const goToFeedbackPage = () => {
    if (roomId) {
      // Navigate to feedback page with roomId as a parameter
      navigate(`/room/feedback/${roomId}`);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: 'auto' }}>
      <h2>Room Details</h2>

      <input
        type="number"
        placeholder="Enter Room ID"
        value={roomId}
        onChange={(e) => setRoomId(e.target.value)}
        style={{ padding: '8px', width: '60%', marginRight: '10px' }}
      />
      <button onClick={fetchRoomDetails} style={{ padding: '8px 16px' }}>
        Fetch Room Details
      </button>

      {loading && <p>Loading room data...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {room && (
        <div style={{ marginTop: '20px' }}>
          <h3>{room.name}</h3>
          <p><strong>Building:</strong> {room?.building?.name || 'N/A'}</p>
          <p><strong>Floor:</strong> {room?.floor}</p>
          <p><strong>Category:</strong> {room?.category?.name || 'N/A'}</p>
          <p><strong>Latitude:</strong> {room?.latitude}</p>
          <p><strong>Longitude:</strong> {room?.longitude}</p>
          {room?.qr_code && (
            <div>
              <h4>QR Code Preview</h4>
              <img src={`data:image/png;base64,${room.qr_code}`} alt="Room QR" style={{ width: '200px' }} />
            </div>
          )}
          {/* Button to navigate to Feedback Page */}
          <button onClick={goToFeedbackPage} style={{ marginTop: '20px' }}>
            Give Feedback for this Room
          </button>
        </div>
      )}
    </div>
  );
};

export default RoomDetails;
