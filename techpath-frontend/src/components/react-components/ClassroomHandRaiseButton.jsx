import { useState } from 'react';

/**
 * Compact icon-only twin of ClassroomConfusionButton, meant to sit inside a small
 * cluster next to it rather than float independently — see the collision notes on
 * ClassroomReactionsBar. Uses primary (blue) as the "active" color specifically to stay
 * visually distinct from the confusion button's amber "I'm lost" state.
 */
export default function ClassroomHandRaiseButton({ raised, onToggle }) {
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
    <button
      onClick={handleClick}
      disabled={busy}
      aria-label={raised ? 'Lower hand' : 'Raise hand'}
      aria-pressed={raised}
      className={`relative flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-xl shadow-2xl transition-all duration-300 active:scale-95 ${
        raised
          ? 'bg-primary-500 text-white shadow-primary-500/30'
          : 'bg-slate-800 text-slate-200 shadow-black/40 hover:bg-slate-700'
      } ${busy ? 'opacity-70' : ''}`}
    >
      <span aria-hidden="true">✋</span>
      {raised && (
        <span className="absolute -inset-1 -z-10 animate-ping rounded-full bg-primary-500/40" />
      )}
    </button>
  );
}
