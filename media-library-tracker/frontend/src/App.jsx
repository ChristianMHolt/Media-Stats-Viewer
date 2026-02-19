import React from 'react';
import MediaList from './components/MediaList';
import { Film } from 'lucide-react';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans antialiased">
      <header className="bg-gray-800 border-b border-gray-700 p-4 sticky top-0 z-50 shadow-md">
        <div className="max-w-7xl mx-auto flex items-center gap-3">
          <Film className="text-blue-500 h-8 w-8" />
          <h1 className="text-2xl font-bold tracking-tight">My Media Library</h1>
        </div>
      </header>
      <main className="py-8">
        <MediaList />
      </main>
    </div>
  );
}

export default App;
