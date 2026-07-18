import { useState } from 'react';

/**
 * Compact icon-only twin of ClassroomConfusionButton, meant to sit inside a small
 * cluster next to it rather than float independently — see the collision notes on
 * ClassroomReactionsBar. Uses primary (blue) as the "active" color specifically to stay
 * visually distinct from the confusion button's amber "I'm lost" state.
 */
export default function ClassroomHandRaiseButton({ raised, micLive, onToggle }) {
  const [busy, setBusy] = useState(false);

  const handleClick = async () => {
    if (busy) return;
    setBusy(true);
    try {
      await onToggle(!raised);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="relative">
      {micLive && (
        <div className="absolute -top-8 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-md bg-red-500 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-white shadow-lg animate-pulse">
          Mic Live
        </div>
      )}
      <button
        onClick={handleClick}
        disabled={busy || micLive}
        aria-label={raised ? 'Lower hand' : 'Raise hand'}
        aria-pressed={raised}
        className={`relative flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-xl shadow-2xl transition-all duration-300 active:scale-95 ${
          micLive 
            ? 'bg-red-500 text-white shadow-red-500/50 scale-110'
            : raised
            ? 'bg-primary-500 text-white shadow-primary-500/30'
            : 'bg-slate-800 text-slate-200 shadow-black/40 hover:bg-slate-700'
        } ${busy ? 'opacity-70' : ''}`}
      >
        <span aria-hidden="true">{micLive ? '🎙️' : '✋'}</span>
        {raised && !micLive && (
          <span className="absolute -inset-1 -z-10 animate-ping rounded-full bg-primary-500/40" />
        )}
        {micLive && (
          <span className="absolute -inset-2 -z-10 animate-ping rounded-full bg-red-500/40" />
        )}
      </button>
    </div>
  );
}
