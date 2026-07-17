import { useState } from 'react';

export default function ClassroomPollSheet({ poll, onVote }) {
  const [minimized, setMinimized] = useState(false);
  const [voting, setVoting] = useState(false);

  if (!poll || minimized) {
    return minimized ? (
      <button
        onClick={() => setMinimized(false)}
        className="fixed bottom-6 left-4 z-30 flex items-center gap-2 rounded-full bg-primary-500 px-4 py-3 text-sm font-medium text-white shadow-2xl shadow-primary-500/30 sm:left-6"
      >
        📊 Poll open
      </button>
    ) : null;
  }

  const hasVoted = poll.my_vote != null;
  const results = poll.results || {};
  const totalVotes = Object.values(results).reduce((a, b) => a + b, 0);
  const isOpen = poll.status === 'open';

  const castVote = async (index) => {
    if (voting || hasVoted) return;
    setVoting(true);
    try {
      await onVote(index);
    } finally {
      setVoting(false);
    }
  };

  return (
    <div className="fixed inset-x-0 bottom-0 z-40 animate-fade-in-up px-3 pb-3 sm:inset-x-auto sm:bottom-6 sm:left-6 sm:w-96 sm:px-0 sm:pb-0">
      <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/95 shadow-2xl backdrop-blur">
        <div className="flex items-start justify-between gap-3 border-b border-slate-800 px-5 py-4">
          <div className="min-w-0">
            <span
              className={`mb-1 inline-block rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${
                isOpen ? 'bg-primary-500/20 text-primary-400' : 'bg-slate-800 text-slate-500'
              }`}
            >
              {isOpen ? 'Live poll' : 'Poll closed'}
            </span>
            <p className="font-medium text-white">{poll.question}</p>
          </div>
          <button
            onClick={() => setMinimized(true)}
            className="shrink-0 rounded-lg p-1 text-slate-500 transition hover:bg-slate-800 hover:text-slate-300"
            aria-label="Minimize"
          >
            ✕
          </button>
        </div>

        <div className="max-h-72 overflow-y-auto p-4">
          {!hasVoted && isOpen ? (
            <div className="space-y-2">
              {poll.options.map((opt, i) => (
                <button
                  key={i}
                  onClick={() => castVote(i)}
                  disabled={voting}
                  className="w-full rounded-xl border border-slate-700 px-4 py-3 text-left text-sm text-slate-200 transition hover:border-primary-500 hover:bg-primary-500/10 disabled:opacity-60"
                >
                  {opt}
                </button>
              ))}
            </div>
          ) : (
            <div className="space-y-3">
              {poll.options.map((opt, i) => {
                const count = results[i] ?? 0;
                const pct = totalVotes > 0 ? Math.round((count / totalVotes) * 100) : 0;
                const mine = poll.my_vote === i;
                // Only ever shown once the poll is fully closed — this is quiz-derived
                // metadata, not something to leak while people can still vote.
                const isCorrect =
                  poll.status === 'closed' &&
                  poll.correct_option_index != null &&
                  poll.correct_option_index === i;
                return (
                  <div
                    key={i}
                    className={
                      isCorrect
                        ? 'rounded-lg ring-2 ring-accent-500/60 ring-offset-2 ring-offset-slate-900'
                        : ''
                    }
                  >
                    <div className="mb-1 flex items-center justify-between text-xs">
                      <span className={mine ? 'font-semibold text-primary-300' : 'text-slate-300'}>
                        {opt} {mine && '✓'}
                        {isCorrect && (
                          <span className="ml-1.5 inline-flex items-center gap-0.5 rounded-full bg-accent-500/15 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-accent-400">
                            ✔ Correct
                          </span>
                        )}
                      </span>
                      <span className="text-slate-500">{pct}%</span>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                      <div
                        className={`h-full rounded-full transition-all duration-700 ease-out ${
                          isCorrect ? 'bg-accent-500' : mine ? 'bg-primary-500' : 'bg-slate-600'
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
              <p className="pt-1 text-xs text-slate-500">
                {totalVotes} vote{totalVotes === 1 ? '' : 's'}
                {hasVoted && isOpen && ' · your answer is locked in'}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
