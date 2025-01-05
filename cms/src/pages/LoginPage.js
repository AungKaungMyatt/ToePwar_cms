import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState(""); // To store user email
  const [password, setPassword] = useState(""); // To store user password
  const [error, setError] = useState(""); // To display error messages
  const [loading, setLoading] = useState(false); // For showing loading state
  const navigate = useNavigate(); // To navigate between routes

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(""); // Clear any previous errors
    setLoading(true); // Show loading state

    // Debugging logs for email and password
    console.log("Attempting login with:");
    console.log("Email:", email);
    console.log("Password:", password);

    try {
      // API request to backend for login
      const response = await axios.post("/admin/login", {
        email,
        password,
      });

      // Debugging log for successful response
      console.log("Login successful, response data:", response.data);

      // Storing tokens in localStorage
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);

      // Navigate to admin dashboard
      navigate("/admin");
    } catch (err) {
      // Logging full error details
      console.error("Login error:", err.response?.data || err.message);
      console.log("Full error object:", err);

      // Displaying backend error message or default error
      setError(err.response?.data?.message || "Invalid email or password.");
    } finally {
      setLoading(false); // Hide loading state
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
        {/* Submit button */}
        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
      {/* Error message display */}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default LoginPage;
