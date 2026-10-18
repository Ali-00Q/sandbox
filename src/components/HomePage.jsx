import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
        <h2 className="text-2xl font-bold mb-2">Welcome, {user?.username || user?.email || 'User'}!</h2>
        <p className="text-gray-600 dark:text-gray-400">
          You have successfully logged in to the application. Explore your dashboard and settings below.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-xl">
          <h3 className="font-semibold mb-1">Profile Status</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Active session verified.</p>
        </div>
        <div className="p-5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-xl">
          <h3 className="font-semibold mb-1">Quick Actions</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Manage account settings.</p>
        </div>
        <div className="p-5 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-xl">
          <h3 className="font-semibold mb-1">System Info</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Connected to FastAPI backend.</p>
        </div>
      </div>
    </div>
  );
}
