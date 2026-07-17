import { useState } from 'react';

const EMOJIS = ['👍', '❤️', '😂', '🎉', '👏', '🤯'];

/**
 * Reaction send control + the floating-and-fading visual feedback for every reaction
 * broadcast to the room (yours or anyone else's — ClassroomApp feeds every `reaction`
 * WS event into `floating`, this component doesn't track its own optimistic copy).
 *
 * The trigger button expands an emoji row rather than showing all six all the time —
 * keeps this a single compact control next to ClassroomHandRaiseButton instead of
 * another row of floating buttons (see the layout notes on that component).
 */
export default function ClassroomReactionsBar({ onSend, floating = [] }) {
  const [open, setOpen] = useState(false);
  const [cooling, setCooling] = useState(false);

  const handleSend = async (emoji) => {
    if (cooling) return;
    // Self-disable immediately so a double-tap can't fire a second request before the
    // server's own 1.5s cooldown would reject it anyway.
    setCooling(true);
    window.setTimeout(() => setCooling(false), 1500);
    await onSend(emoji);
  };

  return (
    <>
      <div
        className="pointer-events-none fixed bottom-40 right-4 z-50 flex flex-col items-end gap-1 sm:right-6"
        aria-hidden="true"
      >
        {floating.map((r) => (
          <span
            key={r.id}
            className="flex max-w-[70vw] animate-float-up-fade items-center gap-1.5 rounded-full bg-slate-900/90 px-3 py-1.5 text-sm shadow-xl backdrop-blur"
          >
            <span className="text-base leading-none">{r.emoji}</span>
            <span className="max-w-[7rem] truncate text-xs text-slate-300">
              {r.display_name}
            </span>
          </span>
        ))}
      </div>

      <div className="relative">
        {open && (
          <div className="absolute bottom-full right-0 mb-2 flex items-center gap-1 rounded-full border border-slate-800 bg-slate-900/95 p-1.5 shadow-2xl backdrop-blur">
            {EMOJIS.map((emoji) => (
              <button
                key={emoji}
                onClick={() => handleSend(emoji)}
                disabled={cooling}
                aria-label={`React with ${emoji}`}
                className="flex h-9 w-9 items-center justify-center rounded-full text-lg transition hover:bg-slate-800 disabled:opacity-40"
              >
                {emoji}
              </button>
            ))}
          </div>
        )}
        <button
          onClick={() => setOpen((o) => !o)}
          aria-label="Send a reaction"
          aria-expanded={open}
          className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-xl shadow-2xl transition-all duration-300 active:scale-95 ${
            open
              ? 'bg-primary-500 text-white shadow-primary-500/30'
              : 'bg-slate-800 text-slate-200 shadow-black/40 hover:bg-slate-700'
          }`}
        >
          <span aria-hidden="true">😊</span>
        </button>
      </div>
    </>
  );
}
