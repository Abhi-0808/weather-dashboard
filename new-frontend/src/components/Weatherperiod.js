import React, { useState } from "react";
import "../App.css";

function Weatherperiod() {
  const [city, setCity] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [weatherData, setWeatherData] = useState([]);
  const [error, setError] = useState("");

  // Function to fetch weather data between start and end dates
  const fetchWeatherData = async () => {
    setError(""); // Clear any previous error messages
    setWeatherData([]); // Clear previous data

    if (!city || !startDate || !endDate) {
      setError("City name, start date, and end date are required.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/weatherhistoryrange", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ city, startDate, endDate }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Server error");
      }

      const data = await response.json();
      setWeatherData(data.weather_data || []);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>

      {/* Input Section */}
      <div style={{ marginBottom: "20px" }}>
        <h2> Weather Data Range</h2>
        <div>
          <input
            type="text"
            placeholder="Enter city name"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            style={{ marginLeft: "10px" }}
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            style={{ marginLeft: "10px" }}
          />
          <button onClick={fetchWeatherData} style={{ marginLeft: "10px" }}>
            Get Weather Data
          </button>
        </div>
      </div>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {/* Table Section */}
      {weatherData.length > 0 && (
        <div>
          <h2>Weather Data for {city}</h2>
          <table border="1" cellPadding="10" cellSpacing="0">
            <thead>
              <tr>
                <th>Date</th>
                <th>Max Temp (°C)</th>
                <th>Min Temp (°C)</th>
                <th>Avg Temp (°C)</th>
                <th>Humidity (%)</th>
              </tr>
            </thead>
            <tbody>
              {weatherData.map((data, index) => (
                <tr key={index}>
                  <td>{data.datetime}</td>
                  <td>{data.tempmax}</td>
                  <td>{data.tempmin}</td>
                  <td>{data.temp}</td>
                  <td>{data.humidity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Weatherperiod;

// #modify