import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm">
      <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">
        Welcome, {user?.username || 'User'}!
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        You have successfully logged in to the application.
      </p>
      <button
        onClick={onLogout}
        className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors"
      >
        Log Out
      </button>
    </div>
  );
}
