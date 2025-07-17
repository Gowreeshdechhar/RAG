import React from "react";

const ChatArea = () => {
  return (
    <div className="flex-1 bg-white rounded-xl shadow-md p-4 overflow-y-auto mb-4">
      <div className="mb-2">
        <div className="text-sm text-gray-500">User:</div>
        <div className="p-2 bg-indigo-100 rounded">Hello!</div>
      </div>
      <div>
        <div className="text-sm text-gray-500">AI:</div>
        <div className="p-2 bg-gray-100 rounded">Hi there! How can I help?</div>
      </div>
    </div>
  );
};

export default ChatArea;