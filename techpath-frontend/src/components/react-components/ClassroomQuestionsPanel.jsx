import { useState, useEffect } from 'react';
import { MessageCircleQuestion, Send, ThumbsUp, X } from 'lucide-react';
import { getQuestions, askQuestion, upvoteQuestion } from '@/services/classroomService';

export default function ClassroomQuestionsPanel({
  sessionId,
  token,
  isOpen,
  onClose,
  questions,
  setQuestions,
}) {
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [myUpvotes, setMyUpvotes] = useState(new Set()); // client-side tracking of my upvotes

  useEffect(() => {
    if (isOpen) {
      void fetchQuestions();
    }
  }, [isOpen, sessionId, token]);

  const fetchQuestions = async () => {
    setLoading(true);
    const res = await getQuestions(sessionId, token);
    setLoading(false);
    if (res.success && res.data) {
      setQuestions(res.data);
    }
  };

  const submit = async () => {
    if (!text.trim() || submitting) return;
    setSubmitting(true);
    setError('');
    const res = await askQuestion(sessionId, token, text.trim());
    setSubmitting(false);
    if (res.success) {
      setText('');
      // It will also be pushed via WS, but let's wait for WS or optimistically add it?
      // Since WS is already active, we don't strictly need to add it, but we can do it optimistically.
    } else {
      setError(res.error || 'Failed to submit question');
    }
  };

  const handleUpvote = async (qId) => {
    if (myUpvotes.has(qId)) return; // prevent double vote locally
    setMyUpvotes(new Set([...myUpvotes, qId]));
    await upvoteQuestion(sessionId, token, qId);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 flex w-full max-w-sm flex-col border-l border-slate-800 bg-slate-950 shadow-2xl transition-transform">
      <div className="flex items-center justify-between border-b border-slate-800 p-4">
        <h2 className="flex items-center gap-2 font-heading font-semibold text-white">
          <MessageCircleQuestion className="h-5 w-5 text-primary-500" />
          Live Q&A
        </h2>
        <button
          onClick={onClose}
          className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {loading && questions.length === 0 ? (
          <div className="text-center text-sm text-slate-500 py-4">Loading questions...</div>
        ) : questions.length === 0 ? (
          <div className="text-center text-sm text-slate-500 py-8">
            No questions asked yet. Be the first!
          </div>
        ) : (
          questions.map((q) => (
            <div
              key={q.id}
              className={`rounded-xl border p-3 ${
                q.is_answered
                  ? 'border-emerald-900/30 bg-emerald-950/10'
                  : 'border-slate-800 bg-slate-900/60'
              }`}
            >
              <div className="flex gap-3">
                <div className="flex-1">
                  <p className={`text-sm ${q.is_answered ? 'text-slate-400' : 'text-slate-200'}`}>
                    {q.question_text}
                  </p>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-[10px] text-slate-500">{q.student_name || 'Guest'}</span>
                    {q.is_answered && (
                      <span className="rounded bg-emerald-900/40 px-1.5 py-0.5 text-[10px] font-medium text-emerald-400">
                        Answered
                      </span>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleUpvote(q.id)}
                  disabled={q.is_answered || myUpvotes.has(q.id)}
                  className={`flex h-fit shrink-0 flex-col items-center gap-1 rounded-lg border px-2 py-1.5 transition ${
                    myUpvotes.has(q.id)
                      ? 'border-primary-500/50 bg-primary-500/10 text-primary-400'
                      : 'border-slate-700 bg-slate-800 text-slate-400 hover:bg-slate-700 disabled:opacity-50'
                  }`}
                >
                  <ThumbsUp className="h-3.5 w-3.5" />
                  <span className="text-[10px] font-bold leading-none">{q.upvotes}</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="border-t border-slate-800 bg-slate-900/50 p-4">
        {error && <p className="mb-2 text-xs text-red-400">{error}</p>}
        <div className="flex gap-2">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && submit()}
            placeholder="Ask a question..."
            maxLength={500}
            className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white placeholder-slate-500 outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
          />
          <button
            onClick={submit}
            disabled={!text.trim() || submitting}
            className="flex shrink-0 items-center justify-center rounded-xl bg-primary-500 px-3 py-2 text-white transition hover:bg-primary-600 disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
