import React, { useState, useEffect } from 'react'; // Added React, useState, useEffect
import logo from './logo.svg';
import './App.css';

function App() {
  const [message, setMessage] = useState(''); // State to store the message

  useEffect(() => {
    // Fetch data from the FastAPI backend
    fetch('http://backend:8000/') // Use 'backend' as the service name in Docker Compose
      .then(response => response.json())
      .then(data => setMessage(data.message))
      .catch(error => console.error('Error fetching data:', error));
  }, []); // Empty dependency array means this effect runs once after the initial render

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        {/* Display the message from the backend */}
        {message && <p>Message from Backend: {message}</p>} {/* Display message */}
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
