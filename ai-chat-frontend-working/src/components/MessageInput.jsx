import React from "react";
import { Mic, ImagePlus, Video, Paperclip } from "lucide-react";

const MessageInput = () => {
  return (
    <div className="flex items-center gap-2 bg-white p-3 rounded-xl shadow-md">
      <input
        type="text"
        placeholder="Type a message..."
        className="flex-1 p-2 border rounded focus:outline-none"
      />
      <button><Mic className="text-indigo-600" /></button>
      <button><ImagePlus className="text-indigo-600" /></button>
      <button><Video className="text-indigo-600" /></button>
      <button><Paperclip className="text-indigo-600" /></button>
    </div>
  );
};

export default MessageInput;