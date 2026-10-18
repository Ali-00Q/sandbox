import React from 'react';

export default function HomePage({ user, onLogout }) {
  const username = typeof user === 'object' && user !== null ? (user.username || user.email || 'User') : user;

  return (
    <div className="max-w-xl mx-auto mt-8 p-6 bg-white dark:bg-gray-900 rounded-xl shadow border border-gray-100 dark:border-gray-800 text-left">
      <h2 className="text-2xl font-bold mb-2">Welcome, {username}!</h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        You have successfully logged into your account. Explore your home dashboard below.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700">
          <h3 className="font-semibold text-sm mb-1">Account Status</h3>
          <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">Active & Verified</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700">
          <h3 className="font-semibold text-sm mb-1">Session Type</h3>
          <p className="text-xs text-gray-500 dark:text-gray-400">Standard Web Session</p>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
        <span className="text-xs text-gray-400">ID: {JSON.stringify(user)}</span>
        {onLogout && (
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition-colors"
          >
            Logout
          </button>
        )}
      </div>
    </div>
  );
}
