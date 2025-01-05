import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
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
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUsers(response.data);
      } catch (err) {
        console.error("Error fetching users:", err);
        if (err.response?.status === 401) {
          setError("Session expired. Please log in again.");
          localStorage.removeItem("token");
          navigate("/");
        } else {
          setError(err.response?.data?.message || "Failed to fetch users.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [navigate]);

  const updateUserStatus = async (userId, status) => {
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      await axios.put(
        `/admin/users/${userId}/status`,
        { status },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      alert(`User status updated to ${status} successfully!`);
      setUsers((prev) =>
        prev.map((user) => (user.id === userId ? { ...user, status } : user))
      );
    } catch (err) {
      console.error("Error updating user status:", err);
      setError(err.response?.data?.message || "Failed to update user status.");
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = async (userId) => {
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      await axios.delete(`/admin/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert("User deleted successfully!");
      setUsers((prev) => prev.filter((user) => user.id !== userId));
    } catch (err) {
      console.error("Error deleting user:", err);
      setError(err.response?.data?.message || "Failed to delete user.");
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  return (
    <div>
      <h1>User Management</h1>
      {loading && <p>Loading...</p>}
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.email} - {user.status}
            <button onClick={() => updateUserStatus(user.id, "active")}>
              Activate
            </button>
            <button onClick={() => updateUserStatus(user.id, "suspended")}>
              Suspend
            </button>
            <button onClick={() => updateUserStatus(user.id, "banned")}>
              Ban
            </button>
            <button onClick={() => deleteUser(user.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserManagement;
