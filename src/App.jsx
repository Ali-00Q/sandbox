import React, { useEffect } from 'react';
import LoginForm from './components/LoginForm';
import HomePage from './components/HomePage';
import ThemeToggle from './components/ThemeToggle';

function App() {
  useEffect(() => {
    try {
      const stored = localStorage.getItem('theme:v1');
      if (stored === 'dark') {
        document.documentElement.classList.add('dark');
      } else if (stored === 'light') {
        document.documentElement.classList.remove('dark');
      }
    } catch {}
  }, []);

  const [user, setUser] = React.useState(null);

  const handleLogin = (credentials) => {
    console.log('Logging in with:', credentials);
    setUser(credentials);
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div className="App min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors">
      <header className="flex flex-col sm:flex-row items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800 max-w-4xl mx-auto gap-4">
        <h1 className="text-xl font-bold">{user ? 'Home Page' : 'App Navigation'}</h1>
        <nav className="flex items-center justify-between w-full sm:w-auto space-x-4">
          <div className="flex items-center space-x-2">
            <ThemeToggle />
          </div>
          <div className="flex items-center space-x-2">
            {user ? (
              <button
                onClick={handleLogout}
                className="text-xs bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-300 px-3 py-1.5 rounded-lg hover:bg-red-200 transition-colors"
              >
                Logout
              </button>
            ) : (
              <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-800 flex items-center justify-center text-xs font-semibold" aria-label="User Profile">
                UP
              </div>
            )}
          </div>
        </nav>
      </header>
      <main className="p-4">
        {user ? (
          <HomePage user={user} onLogout={handleLogout} />
        ) : (
          <LoginForm onLogin={handleLogin} />
        )}
      </main>
    </div>
  );
}

export default App;