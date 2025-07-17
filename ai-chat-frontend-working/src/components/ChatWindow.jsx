import React from "react";
import { motion } from "framer-motion";

const ChatWindow = ({ messages, user }) => {
  return (
    <div className="flex flex-col flex-1 p-4 overflow-y-auto bg-gradient-to-b from-[#0f172a] via-[#1e293b] to-[#0f172a] text-white">
      {messages.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center text-gray-400 mt-10"
        >
          Start a conversation
        </motion.div>
      ) : (
        messages.map((msg, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.05 }}
            className={`max-w-lg rounded-2xl p-3 my-2 text-sm md:text-base ${
              msg.sender === user
                ? "bg-blue-600 self-end text-right"
                : "bg-gray-700 self-start text-left"
            }`}
          >
            {msg.text}
          </motion.div>
        ))
      )}
    </div>
  );
};

export default ChatWindow;
