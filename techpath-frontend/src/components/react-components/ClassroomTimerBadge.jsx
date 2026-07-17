import { useEffect, useState } from 'react';

function formatRemaining(totalSeconds) {
  const clamped = Math.max(0, Math.round(totalSeconds));
  const minutes = Math.floor(clamped / 60);
  const seconds = clamped % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

/**
 * Small header badge for a trainer-started countdown. Lives next to the "N online"
 * indicator per the layout notes in ClassroomApp — glanceable info, not an action, so it
 * doesn't need a fixed-position slot of its own. Renders nothing while liveState.timer
 * is null/absent (no timer running).
 */
export default function ClassroomTimerBadge({ timer }) {
  const [remaining, setRemaining] = useState(null);

  useEffect(() => {
    if (!timer) {
      setRemaining(null);
      return undefined;
    }
    const startedAtMs = new Date(timer.started_at).getTime();
    const compute = () =>
      Math.max(0, timer.duration_seconds - (Date.now() - startedAtMs) / 1000);

    setRemaining(compute());
    const interval = setInterval(() => setRemaining(compute()), 1000);
    return () => clearInterval(interval);
  }, [timer]);

  if (!timer || remaining === null) return null;

  const low = remaining <= 30;

  return (
    <span
      className={`flex shrink-0 items-center gap-1 rounded-full px-2.5 py-1 font-mono text-xs font-medium tabular-nums ${
        low ? 'bg-red-500/15 text-red-400' : 'bg-primary-500/15 text-primary-300'
      }`}
    >
      <span aria-hidden="true">⏱</span>
      {formatRemaining(remaining)}
    </span>
  );
}
