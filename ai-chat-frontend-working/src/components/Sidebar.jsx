import React from "react";

const Sidebar = () => {
  return (
    <div className="w-64 bg-white p-4 shadow-md rounded-l-2xl">
      <h3 className="font-semibold text-indigo-700 mb-4">Chat History</h3>
      <ul className="space-y-2">
        <li className="p-2 rounded hover:bg-indigo-100 cursor-pointer">Chat 1</li>
        <li className="p-2 rounded hover:bg-indigo-100 cursor-pointer">Chat 2</li>
      </ul>
    </div>
  );
};

export default Sidebar;