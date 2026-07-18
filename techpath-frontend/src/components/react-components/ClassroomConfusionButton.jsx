import { useState } from 'react';

export default function ClassroomConfusionButton({ confused, onToggle }) {
  const [busy, setBusy] = useState(false);

  const handleClick = async () => {
    if (busy) return;
    setBusy(true);
    try {
      await onToggle(!confused);
    } finally {
      setBusy(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={busy}
      className={`fixed bottom-6 right-4 z-30 flex items-center gap-2 rounded-full px-5 py-3.5 font-medium shadow-2xl transition-all duration-300 active:scale-95 sm:right-6 ${
        confused
          ? 'bg-amber-500 text-slate-950 shadow-amber-500/30'
          : 'bg-slate-800 text-slate-200 shadow-black/40 hover:bg-slate-700'
      } ${busy ? 'opacity-70' : ''}`}
    >
      <span className="text-xl leading-none">{confused ? '🤔' : '👍'}</span>
      <span className="text-sm">{confused ? "I'm lost" : 'Following along'}</span>
      {confused && (
        <span className="absolute -inset-1 -z-10 animate-ping rounded-full bg-amber-500/40" />
      )}
    </button>
  );
}
