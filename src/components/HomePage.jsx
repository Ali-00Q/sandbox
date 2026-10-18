import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white dark:bg-gray-900 rounded-xl shadow-md border border-gray-100 dark:border-gray-800">
      <h2 className="text-xl font-bold mb-4">Welcome to the Home Page</h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        You are successfully logged in as <span className="font-semibold text-gray-900 dark:text-gray-100">{user?.username || user?.email || 'User'}</span>.
      </p>
      <button
        onClick={onLogout}
        className="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors font-medium"
      >
        Logout
      </button>
    </div>
  );
}
