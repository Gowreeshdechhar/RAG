import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Chat from "./pages/Chat";

function App() {
  return (
    <div
      className="min-h-screen bg-cover bg-center text-white"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      {/* Optional dark overlay */}
      <div className="min-h-screen bg-black bg-opacity-70">
        <Router>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </Router>
      </div>
    </div>
  );
}

export default App;
