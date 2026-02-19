import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MediaItem from './MediaItem';
import { Loader2, FolderSearch, AlertCircle, Film } from 'lucide-react';

const MediaList = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [path, setPath] = useState('dummy_library'); // Default for quick testing
  const [scannedPath, setScannedPath] = useState('');

  const scanLibrary = async () => {
    if (!path) return;

    setLoading(true);
    setError(null);
    try {
      // Use relative URL assuming proxy or CORS allows localhost:8000
      // In development, we can point to http://localhost:8000
      const response = await axios.get(`http://localhost:8000/scan?path=${encodeURIComponent(path)}`);
      setItems(response.data);
      setScannedPath(path);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to scan library. Make sure backend is running and path is correct.");
    } finally {
      setLoading(false);
    }
  };

  // Auto-scan on mount if desired, but maybe let user click scan first.
  // useEffect(() => { scanLibrary(); }, []);

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8 bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
        <h2 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
          <FolderSearch className="text-blue-400" />
          Scan Media Library
        </h2>
        <div className="flex gap-4">
          <input
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder="Enter full folder path (e.g., /mnt/media/Anime)"
            className="flex-1 bg-gray-900 border border-gray-600 rounded-md px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={scanLibrary}
            disabled={loading || !path}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white px-6 py-2 rounded-md font-medium transition-colors flex items-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : 'Scan'}
          </button>
        </div>
        {error && (
          <div className="mt-4 p-3 bg-red-900/30 border border-red-800 rounded-md text-red-200 flex items-center gap-2">
            <AlertCircle size={20} />
            {error}
          </div>
        )}
      </div>

      {items.length > 0 ? (
        <div className="bg-gray-800 rounded-lg shadow-xl border border-gray-700 overflow-hidden">
           <div className="p-4 bg-gray-900 border-b border-gray-700 flex justify-between items-center">
              <span className="text-gray-400 text-sm">Found {items.length} items in <span className="text-gray-300 font-mono">{scannedPath}</span></span>
           </div>
           <div>
             {items.map((item, index) => (
               <MediaItem key={index} item={item} />
             ))}
           </div>
        </div>
      ) : (
        !loading && !error && (
          <div className="text-center py-20 text-gray-500">
            <Film className="mx-auto h-16 w-16 mb-4 opacity-20" />
            <p className="text-xl">Enter a path and scan to see your media library.</p>
          </div>
        )
      )}
    </div>
  );
};

export default MediaList;
