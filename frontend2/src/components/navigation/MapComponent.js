import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import axios from 'axios';
import L from 'leaflet';
import { Html5Qrcode } from 'html5-qrcode';
import './MapComponent.css';  // Make sure to import the CSS file

const icon = new L.Icon({
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const FlyToLocation = ({ position }) => {
  const map = useMap();
  useEffect(() => {
    if (position) map.flyTo(position, 18);
  }, [position, map]);
  return null;
};

const MapComponent = () => {
  const [buildings, setBuildings] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [pathCoords, setPathCoords] = useState([]);
  const [startPoint, setStartPoint] = useState('');
  const [endPoint, setEndPoint] = useState('');
  const [startCoordinates, setStartCoordinates] = useState(null);
  const [endCoordinates, setEndCoordinates] = useState(null);
  const [scanning, setScanning] = useState(false);
  const qrRef = useRef(null);  // Using a ref to access the QR reader div

  useEffect(() => {
    // Fetch buildings data
    axios.get('https://nav-app-back.onrender.com/api/buildings/')
      .then(res => setBuildings(res.data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    if (scanning && qrRef.current) {
      // Initialize the QR code scanner
      const scanner = new Html5Qrcode("qr-reader"); // Use qr-reader div for scanner
      scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        async (decodedText) => {
          await scanner.stop();
          setScanning(false);

          try {
            const res = await axios.get(`https://nav-app-back.onrender.com/api/qrlocations/?code=${decodedText}`);
            const room = res.data[0].room;
            const { latitude, longitude } = room;
            setSelectedLocation([latitude, longitude]);

            if (startCoordinates) {
              // Fetch path if start is selected
              const pathRes = await axios.get(`https://nav-app-back.onrender.com/api/shortest-path/?start_lat=${startCoordinates[0]}&start_lng=${startCoordinates[1]}&end_lat=${latitude}&end_lng=${longitude}`);
              setPathCoords(pathRes.data.path_coordinates);
            }
          } catch (err) {
            console.error("Invalid QR code or room not found", err);
            alert("Invalid QR code or room not found");
          }
        }
      ).catch((err) => {
        console.error("QR Scan error", err);
        setScanning(false);
      });
    }
  }, [scanning, startCoordinates]); // Re-initialize when scanning state changes

  const handleSearch = async () => {
    try {
      const roomRes = await axios.get(`https://nav-app-back.onrender.com/api/roomsearch/?query=${searchQuery}`);
      const buildingRes = await axios.get(`https://nav-app-back.onrender.com/api/buildingsearch/?query=${searchQuery}`);
      const target = roomRes.data[0] || buildingRes.data[0];
      if (!target) return alert('Not found');
      const { latitude, longitude } = target;
      setSelectedLocation([latitude, longitude]);
    } catch (err) {
      console.error(err);
      alert('Search failed');
    }
  };

  const handleShortestPath = async () => {
    try {
      const startRes = await axios.get(`https://nav-app-back.onrender.com/api/buildingsearch/?query=${startPoint}`);
      const endRes = await axios.get(`https://nav-app-back.onrender.com/api/buildingsearch/?query=${endPoint}`);

      const startLoc = startRes.data[0];
      const endLoc = endRes.data[0];

      if (!startLoc || !endLoc) return alert('Start or End location not found');

      const { latitude: startLat, longitude: startLng } = startLoc;
      const { latitude: endLat, longitude: endLng } = endLoc;

      setStartCoordinates([startLat, startLng]);
      setEndCoordinates([endLat, endLng]);
      setSelectedLocation([startLat, startLng]);

      const pathRes = await axios.get(`https://nav-app-back.onrender.com/api/shortest-path/?start_lat=${startLat}&start_lng=${startLng}&end_lat=${endLat}&end_lng=${endLng}`);
      setPathCoords(pathRes.data.path_coordinates);
    } catch (err) {
      console.error("Shortest path fetch failed", err);
    }
  };

  const handleQRScan = () => {
    setScanning(true);  // Trigger the QR scanning
  };

  return (
    <div className="map-container">
      {/* Search Bar */}
      <div className="search-section">
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search building or room"
        />
        <button onClick={handleSearch}>Search</button>
        <button onClick={handleQRScan}>Scan QR</button>
      </div>

      {/* Shortest Path Section */}
      <div className="search-section">
        <input
          value={startPoint}
          onChange={(e) => setStartPoint(e.target.value)}
          placeholder="Enter start point"
        />
        <input
          value={endPoint}
          onChange={(e) => setEndPoint(e.target.value)}
          placeholder="Enter end point"
        />
        <button onClick={handleShortestPath}>Find Shortest Path</button>
      </div>

      {/* QR Reader */}
      {scanning && (
        <div
          id="qr-reader"
          ref={qrRef}
          className="qr-reader"
        />
      )}

      {/* Map */}
      <MapContainer
        center={[28.6139, 77.2090]}
        zoom={16}
        style={{ height: "600px", width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {selectedLocation && <FlyToLocation position={selectedLocation} />}

        {buildings.map((b) => (
          <Marker key={b.id} position={[b.latitude, b.longitude]} icon={icon}>
            <Popup>
              <strong>{b.name}</strong><br />
              {b.description}
            </Popup>
          </Marker>
        ))}

        {pathCoords.length > 0 && (
          <Polyline positions={pathCoords} color="blue" />
        )}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
