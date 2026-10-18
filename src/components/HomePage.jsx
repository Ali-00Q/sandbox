import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl shadow-sm">
      <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">Welcome back, {user?.username || 'User'}!</h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        You have successfully logged in to the application. This is your home dashboard.
      </p>
      <div className="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-100 dark:border-gray-800">
        <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Session Details</h3>
        <pre className="text-xs text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-800 overflow-x-auto">
          {JSON.stringify(user, null, 2)}
        </pre>
      </div>
    </div>
  );
}
