// src/components/AuthForm.jsx
import React, { useState } from "react";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendPasswordResetEmail } from "firebase/auth";
import { initializeApp } from "firebase/app";
import firebaseConfig from "../firebaseConfig";
import { motion } from "framer-motion";

initializeApp(firebaseConfig);
const auth = getAuth();

export default function AuthForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleAuth = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password);
        setMessage("Logged in successfully!");
      } else {
        await createUserWithEmailAndPassword(auth, email, password);
        setMessage("Account created successfully!");
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) return setError("Enter your email to reset password");
    try {
      await sendPasswordResetEmail(auth, email);
      setMessage("Reset link sent to your email");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black p-4">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/10 backdrop-blur-lg shadow-xl p-8 rounded-2xl w-full max-w-md border border-white/20"
      >
        <h2 className="text-3xl font-bold text-white text-center mb-6">
          {isLogin ? "Login" : "Register"}
        </h2>

        <form onSubmit={handleAuth} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full p-3 bg-white/20 text-white rounded-md outline-none placeholder-white"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 bg-white/20 text-white rounded-md outline-none placeholder-white"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && <p className="text-red-500 text-sm">{error}</p>}
          {message && <p className="text-green-400 text-sm">{message}</p>}

          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 transition-all text-white py-2 rounded-md"
          >
            {isLogin ? "Login" : "Sign Up"}
          </button>

          <div className="flex justify-between text-sm text-white mt-2">
            <button
              type="button"
              className="hover:underline"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Don't have an account? Register" : "Already have an account? Login"}
            </button>
            <button
              type="button"
              className="hover:underline text-red-400"
              onClick={handleForgotPassword}
            >
              Forgot Password?
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
}
