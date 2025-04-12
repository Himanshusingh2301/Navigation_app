import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Feedback.css'; // Import the CSS file for styling

const FeedbackPage = () => {
  const [roomId, setRoomId] = useState(""); // Store roomId input
  const [feedbacks, setFeedbacks] = useState([]);
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleRoomIdChange = (e) => {
    setRoomId(e.target.value);
  };

  const handleSubmitFeedback = (e) => {
    e.preventDefault();

    if (isSubmitting || !feedbackMessage.trim() || !roomId) return;

    setIsSubmitting(true);

    const feedbackData = {
      room: roomId,
      message: feedbackMessage,
    };

    axios.post(`http://localhost:8000/api/feedbacks/`, feedbackData)
      .then(response => {
        setFeedbacks([response.data, ...feedbacks]);
        setFeedbackMessage(""); // Reset input field
      })
      .catch(error => console.error('Error submitting feedback:', error))
      .finally(() => setIsSubmitting(false));
  };

  useEffect(() => {
    // Fetch feedback for the specific room if roomId is set
    if (roomId) {
      axios.get(`http://localhost:8000/api/feedbacks/?room=${roomId}`)
        .then(response => {
          setFeedbacks(response.data);
        })
        .catch(error => console.error('Error fetching feedback:', error));
    }
  }, [roomId]);

  return (
    <div className="feedback-container">
      <h2 className="feedback-title">Submit Feedback</h2>

      <div className="room-id-container">
        <label htmlFor="roomId" className="label">Room ID: </label>
        <input
          type="text"
          id="roomId"
          value={roomId}
          onChange={handleRoomIdChange}
          placeholder="Enter Room ID"
          className="input-field"
        />
      </div>

      <form onSubmit={handleSubmitFeedback} className="feedback-form">
        <textarea
          value={feedbackMessage}
          onChange={(e) => setFeedbackMessage(e.target.value)}
          placeholder="Enter your feedback"
          rows="4"
          className="textarea-field"
        />
        <button type="submit" disabled={isSubmitting} className="submit-button">
          {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
        </button>
      </form>

      {roomId && (
        <div className="feedback-list">
          <h3 className="previous-feedback-title">Previous Feedback for Room {roomId}</h3>
          <ul className="feedback-ul">
            {feedbacks.map(feedback => (
              <li key={feedback.id} className="feedback-item">
                <p><strong>{feedback.user.username}</strong>: {feedback.message}</p>
                <p><em>{new Date(feedback.created_at).toLocaleString()}</em></p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FeedbackPage;
