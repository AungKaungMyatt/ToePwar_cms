import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState(""); // For storing user email
  const [password, setPassword] = useState(""); // For storing user password
  const [error, setError] = useState(""); // For error messages
  const navigate = useNavigate(); // To navigate to other routes

  const handleLogin = async (e) => {
    e.preventDefault();

    // Debugging logs for email and password
    console.log("Attempting login with:");
    console.log("Email:", email);
    console.log("Password:", password);

    try {
      // API request to backend for login
      const response = await axios.post("https://toepwar.onrender.com/admin/login", {
        email,
        password,
      });

      // Debugging log for API response
      console.log("Login successful, response data:", response.data);

      // Storing token in localStorage
      localStorage.setItem("token", response.data.access_token);

      // Navigate to admin dashboard on successful login
      navigate("/admin");
    } catch (err) {
      // Logging full error details for debugging
      console.error("Login error:", err.response?.data || err.message);
      console.log("Full error object:", err);

      // Setting error message from backend or default message
      setError(err.response?.data?.message || "Invalid email or password.");
    }
  };

  return (
    <div>
      <h1>Admin Login</h1>
      <form onSubmit={handleLogin}>
        {/* Email input */}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {/* Password input */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {/* Login button */}
        <button type="submit">Login</button>
      </form>
      {/* Error message display */}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default LoginPage;
