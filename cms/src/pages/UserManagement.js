import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Fetch users
  const fetchUsers = async (page = 1, searchQuery = "", status = "") => {
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      if (!token) {
        setError("Session expired. Please log in again.");
        localStorage.removeItem("token");
        navigate("/");
        return;
      }

      const response = await axios.get("/admin/users", {
        params: { page, search: searchQuery, status },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.data.results) {
        setUsers(response.data.results);
        setCurrentPage(response.data.page || 1);
        setTotalPages(response.data.total_pages || 1);
      } else {
        setUsers(response.data);
        setCurrentPage(1);
        setTotalPages(1);
      }
    } catch (err) {
      console.error("Error fetching users:", err);
      setError(err.response?.data?.message || "Failed to fetch users.");
    } finally {
      setLoading(false);
    }
  };

  // Fetch users whenever currentPage, search, or statusFilter changes
  useEffect(() => {
    fetchUsers(currentPage, search, statusFilter);
  }, [currentPage, search, statusFilter]);

  // Handle user actions
  const handleAction = async (userId, action) => {
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      const url =
        action === "delete"
          ? `/admin/users/${userId}`
          : `/admin/users/${userId}/status`;

      const method = action === "delete" ? "delete" : "put";
      const data = action !== "delete" ? { status: action } : null;

      await axios({
        method,
        url,
        data,
        headers: { Authorization: `Bearer ${token}` },
      });

      alert(
        `User ${
          action === "delete" ? "deleted" : `status updated to ${action}`
        } successfully!`
      );
      fetchUsers(currentPage, search, statusFilter);
    } catch (err) {
      console.error(`Error performing action (${action}):`, err);
      setError(err.response?.data?.message || "Action failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>User Management</h1>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <input
          type="text"
          placeholder="Search by email"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          onChange={(e) => setStatusFilter(e.target.value)}
          value={statusFilter}
        >
          <option value="">All</option>
          <option value="active">Active</option>
          <option value="suspended">Suspended</option>
          <option value="banned">Banned</option>
        </select>
        <button onClick={() => fetchUsers(1, search, statusFilter)}>Search</button>
      </div>
      {users.length === 0 && !loading && (
        <p>No users found matching your criteria.</p>
      )}
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.email} - {user.status}
            <select
              onChange={(e) => handleAction(user.id, e.target.value)}
              defaultValue=""
            >
              <option value="" disabled>
                Actions
              </option>
              <option value="active">Activate</option>
              <option value="suspended">Suspend</option>
              <option value="banned">Ban</option>
              <option value="delete">Delete</option>
            </select>
          </li>
        ))}
      </ul>
      <div>
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() =>
            setCurrentPage((prev) => Math.min(prev + 1, totalPages))
          }
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default UserManagement;
