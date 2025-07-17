import React from "react";

const Chat = () => {
  return (
    <div className="min-h-screen flex flex-col bg-black text-white">
      {/* Header */}
      <div className="p-4 text-2xl font-bold border-b border-gray-700">
        AI Chat Assistant
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Example messages */}
        <div className="self-start max-w-xs p-3 bg-gray-800 rounded-xl">
          Hello! How can I help you?
        </div>
        <div className="self-end max-w-xs p-3 bg-blue-700 rounded-xl">
          Tell me about today’s weather.
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 bg-gray-900 border-t border-gray-700 flex items-center space-x-2">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 p-2 rounded-md bg-gray-800 text-white placeholder-gray-400 focus:outline-none"
        />
        <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md text-white">
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
