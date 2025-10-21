import React from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import Dash from "./dash";

// LoginForm component
function LoginForm() {
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      body: formData,
      credentials: "include", // needed if your backend sets cookies
    });

    const data = await res.json();
    if (data.success) {
      navigate("/dash"); // client-side redirect to dashboard
    } else {
      alert("Login failed");
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "400px", margin: "0 auto" }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input type="email" name="email" required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" name="password" required />
        </div>
        <button type="submit">Login</button>
      </form>

      <h2>Signup</h2>
      <form action="http://localhost:8000/auth/signup" method="post">
        <div>
          <label>Email:</label>
          <input type="email" name="email" required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" name="password" required />
        </div>
        <button type="submit">Signup</button>
      </form>
    </div>
  );
}

// Main App component with routes
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/dash" element={<Dash />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;