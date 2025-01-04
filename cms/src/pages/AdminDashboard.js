import React from "react";
import { useNavigate } from "react-router-dom";

function AdminDashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <button onClick={() => navigate("/users")}>Manage Users</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default AdminDashboard;