import React, { useState } from "react";
import "../App.css";

function WeatherApp() {
  const [city, setCity] = useState(""); // For current weather
  const [city2, setCity2] = useState(""); // For historical weather
  const [date, setDate] = useState(""); // For historical weather date
  const [weatherData, setWeatherData] = useState(null); // To store fetched weather data
  const [error, setError] = useState(""); // To display errors

  // Function to fetch current weather
  const fetchCurrentWeather = async () => {
    setError(""); // Clear previous errors
    setWeatherData(null); // Clear previous data

    if (!city) {
      setError("City name is required for current weather.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/weather", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ city }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Server error");
      }

      const data = await response.json();
      setWeatherData({ type: "current", data: data.weather }); // Set type to "current"
    } catch (err) {
      setError(err.message);
    }
  };

  // Function to fetch historical weather
  const fetchHistoricalWeather = async () => {
    setError(""); // Clear previous errors
    setWeatherData(null); // Clear previous data

    if (!city2 || !date) {
      setError("Both city and date are required for historical weather.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/weatherhistory", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ city: city2, date }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Server error");
      }

      const data = await response.json();
      setWeatherData({ type: "historical", data: data.weather_data }); // Set type to "historical"
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>

      {/* Current Weather Section */}
      <div style={{ marginBottom: "20px" }}>
        <h2>Current Weather</h2>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="text"
            placeholder="Enter city name"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
          <button onClick={fetchCurrentWeather} style={{ marginLeft: "10px" }}>
            Get Current Weather
          </button>
        </div>
      </div>

      {/* Historical Weather Section */}
      <div style={{ marginBottom: "20px" }}>
        <h2>Historical Weather</h2>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="text"
            placeholder="Enter city name"
            value={city2}
            onChange={(e) => setCity2(e.target.value)}
          />
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            style={{ marginLeft: "10px" }}
          />
          <button onClick={fetchHistoricalWeather} style={{ marginLeft: "10px" }}>
            Get Historical Weather
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {/* Display Weather Data */}
      {weatherData && (
        <div>
          {weatherData.type === "current" && (
            <div>
              <h3>Current Weather in {city}</h3>
              <p>Temperature: {weatherData.data.temp}°C</p>
              <p>Feels Like: {weatherData.data.feels_like}°C</p>
              <p>Conditions: {weatherData.data.description}</p>
              <p>Humidity: {weatherData.data.humidity}%</p>
            </div>
          )}

          {weatherData.type === "historical" && (
            <div>
              <h3>Historical Weather Data</h3>
              {weatherData.data.length > 0 ? (
                weatherData.data.map((data, index) => (
                  <div key={index}>
                    <p>Temperature: {data.temp}°C</p>
                    <p>Temprature max: {data.tempmax}°C</p>
                    <p>Temprature min: {data.tempmin}</p>
                    <p>Humidity: {data.humidity}%</p>
                    <hr />
                  </div>
                ))
              ) : (
                <p>No historical data found for the selected date.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default WeatherApp;
