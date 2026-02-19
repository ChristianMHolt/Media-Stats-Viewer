import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Folder, Film, Tv } from 'lucide-react';

const StatBadge = ({ label, value, colorClass = "bg-gray-700 text-gray-200" }) => {
  if (!value) return null;
  return (
    <span className={`text-xs px-2 py-1 rounded-md font-medium ${colorClass} mr-2`}>
      {value}
    </span>
  );
};

const MediaItem = ({ item, depth = 0 }) => {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = item.children && item.children.length > 0;

  const toggleExpand = () => setExpanded(!expanded);

  // Determine icon based on type (heuristic)
  const Icon = hasChildren ? Tv : Film;

  return (
    <div className="border-b border-gray-700 last:border-0">
      <div
        className={`flex items-center p-4 hover:bg-gray-800 transition-colors ${depth > 0 ? 'bg-gray-800/50 pl-8' : ''}`}
      >
        <div className="flex-1 flex items-center gap-3">
          {hasChildren ? (
            <button onClick={toggleExpand} className="p-1 hover:bg-gray-700 rounded text-gray-400">
              {expanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          ) : (
            <div className="w-6 h-6 flex items-center justify-center text-gray-500">
               {depth > 0 ? <div className="w-2 h-2 rounded-full bg-gray-600"></div> : <Film size={16}/>}
            </div>
          )}

          <div className="flex flex-col">
            <span className="font-semibold text-white text-lg">{item.name}</span>
            {depth === 0 && item.path && <span className="text-xs text-gray-500 truncate max-w-md">{item.path}</span>}
          </div>
        </div>

        <div className="flex items-center gap-2 flex-wrap justify-end max-w-2xl">
           <StatBadge value={item.stats.resolution} colorClass="bg-blue-900 text-blue-200" />
           <StatBadge value={item.stats.source} colorClass="bg-purple-900 text-purple-200" />
           <StatBadge value={item.stats.video_codec} colorClass="bg-green-900 text-green-200" />
           <StatBadge value={item.stats.audio_codec} colorClass="bg-orange-900 text-orange-200" />
           <StatBadge value={item.stats.group} colorClass="bg-gray-600 text-gray-200" />
        </div>
      </div>

      {expanded && hasChildren && (
        <div className="border-t border-gray-700">
          {item.children.map((child, index) => (
            <MediaItem key={index} item={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MediaItem;
