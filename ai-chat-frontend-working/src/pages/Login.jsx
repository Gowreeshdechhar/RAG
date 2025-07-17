import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (email && password) {
      navigate("/chat");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <div className="bg-gray-100 dark:bg-gray-800 p-8 rounded shadow-md w-full max-w-md">
    <h1 className="text-2xl font-bold mb-4">Login</h1>
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-xl shadow-md w-96 space-y-6"
      >
        <h2 className="text-2xl font-bold text-center text-indigo-700">Login</h2>
        <input
          type="email"
          placeholder="Email"
          className="w-full border p-3 rounded focus:outline-none"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full border p-3 rounded focus:outline-none"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
        >
          Login
        </button>
        <p className="text-sm text-center text-indigo-600 cursor-pointer hover:underline">
          Forgot Password?
        </p>
      </form>
    </div>
    </div>
  );
};

export default Login;
