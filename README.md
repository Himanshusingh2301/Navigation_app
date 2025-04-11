<h1>🏫 KALPATHON_Campus Navigation System</h1>

<p><strong>Problem:</strong><br>
Navigating large and unfamiliar campuses can be frustrating, especially for newcomers. Students, staff, and visitors often struggle to find specific halls, labs, buildings, or rooms, resulting in lost time and confusion.</p>

<p><strong>Goal:</strong><br>
To simplify and streamline campus navigation using a web-based solution that offers real-time directions, QR-based room access, search features, and a user-friendly interface for first-time visitors and regular students.</p>

<h2>💡 Solution</h2>
<ul>
  <li>Interactive campus map with directions between buildings/rooms.</li>
  <li>QR code generation for every room/location for quick scanning.</li>
  <li>Search functionality for rooms, departments, facilities, and notices.</li>
  <li>Role-based access for Admin (add/update locations) and Users (search/view/favorite).</li>
</ul>

<h2>🛠 Tech Stack</h2>
<ul>
  <li><strong>Frontend:</strong> React.js, HTML5, CSS3, JavaScript</li>
  <li><strong>Backend:</strong> Django (Python)</li>
  <li><strong>Database:</strong> PostgreSQL</li>
  <li><strong>APIs:</strong> Google Maps / Mapbox (for navigation)</li>
  <li><strong>QR Scanning:</strong> html5-qrcode (React)</li>
</ul>

<h2>📁 Features</h2>
<ul>
  <li>🗺️ Map view with directions</li>
  <li>🔍 Room/building search with categories</li>
  <li>📌 Mark favorite rooms/visited locations</li>
  <li>📷 QR code scan to navigate instantly</li>
  <li>🛠️ Admin dashboard to manage data</li>
  <li>📝 Notice & feedback system</li>
</ul>

<h2>🚀 Getting Started</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/Himanshusingh2301/Navigation_app.git
cd campus-navigation</code></pre>

<h3>2. Backend Setup (Django)</h3>
<pre><code>cd backend
python -m venv env
source env\Scripts\activate
pip install -r requirements.txt

# Set up environment variables (.env)
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser

# Run development server
python manage.py runserver</code></pre>

<h3>3. Frontend Setup (React)</h3>
<pre><code>cd frontend
npm install
npm start</code></pre>

<h3>4. Environment Variables</h3>
<p>Set your Django and React <code>.env</code> files for database, frontend-backend communication, and API keys (e.g., Google Maps or Mapbox).</p>

<h2>🔐 Authentication</h2>
<ul>
  <li>JWT-based login system</li>
  <li>Roles: <code>Admin</code> and <code>User</code></li>
</ul>

<h2>📌 Future Improvements</h2>
<ul>
  <li>Voice-based navigation</li>
  <li>Mobile app integration (React Native)</li>
  <li>Indoor navigation with WiFi/Bluetooth beacons</li>
</ul>

<h2>📝 License</h2>
<p>MIT License</p>

<h2>🤝 Contributing</h2>
<p>Pull requests and suggestions are welcome! Let’s make campus navigation easier together.</p>

<h2>Participants</h2>
<p>Created by <strong>Himanshu Singh</strong>
<p>Created by <strong>Rahul kumar</strong> 
<p>Created by <strong>Vibha Pandey</strong> 
<p>Created by <strong>Prashant kumar</strong> 
<p>Created by <strong>Prince Sharma</strong> 
