'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import {
  Users,
  BarChart3,
  Code2,
  Wifi,
  WifiOff,
  Plus,
  X,
  Send,
  Square,
  RotateCcw,
  Frown,
  PanelRightClose,
  PanelRightOpen,
  Maximize2,
  Minimize2,
  Hand,
  UserX,
  Timer,
  ListChecks,
  ChevronDown,
  CheckCircle2,
  MessageCircleQuestion,
  ThumbsUp,
  Eye,
  EyeOff,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { CodeEditor } from '@/components/editors/CodeEditor';
import { DoubtQueue } from './DoubtQueue';
import { AudioMixer } from './AudioMixer';
import { trainerService } from '@/services/trainer.service';
import { useClassroomStore } from '@/store/classroom.store';
import type { ClassroomEvent, PollResultsResponse, RosterResponse, TimerView } from '@/types/classroom';
import type { LectureAsset, ModuleAssetLink, QuizQuestion } from '@/types/training';

const CODE_LANGUAGES = [
  'python',
  'javascript',
  'typescript',
  'java',
  'csharp',
  'go',
  'rust',
  'sql',
  'bash',
  'html',
  'css',
  'json',
  'yaml',
];

type Tab = 'roster' | 'poll' | 'code' | 'questions';

interface Props {
  sessionId: number;
  connected: boolean;
  subscribe: (handler: (event: ClassroomEvent) => void) => () => void;
  assets: ModuleAssetLink[];
}

function ConfusionMeter({ online, confused, ratio }: RosterResponse['confusion']) {
  const pct = Math.round(ratio * 100);
  const color =
    pct >= 50 ? 'bg-red-500' : pct >= 20 ? 'bg-amber-500' : 'bg-teal-500';
  const label = pct >= 50 ? 'Struggling' : pct >= 20 ? 'Some confusion' : 'On track';

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-4">
      <div className="mb-2 flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-wide text-gray-500">
          Room pulse
        </span>
        <span
          className={`text-xs font-semibold ${
            pct >= 50 ? 'text-red-400' : pct >= 20 ? 'text-amber-400' : 'text-teal-400'
          }`}
        >
          {label}
        </span>
      </div>
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-gray-800">
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out ${color}`}
          style={{ width: `${Math.max(pct, confused > 0 ? 4 : 0)}%` }}
        />
      </div>
      <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
        <span>
          {confused} of {online} confused
        </span>
        <span>{pct}%</span>
      </div>
    </div>
  );
}

function RosterTab({ sessionId }: { sessionId: number }) {
  const [roster, setRoster] = useState<RosterResponse | null>(null);
  const [kickingId, setKickingId] = useState<number | null>(null);
  const [loweringId, setLoweringId] = useState<number | null>(null);
  const setDoubtRequests = useClassroomStore((s) => s.setDoubtRequests);

  useEffect(() => {
    void trainerService.getRoster(sessionId).then((r) => {
      setRoster(r);
      setDoubtRequests(r.doubt_requests || []);
    }).catch(() => {});
  }, [sessionId, setDoubtRequests]);

  const kick = async (participantId: number, displayName: string) => {
    if (!confirm(`Remove ${displayName} from the session?`)) return;
    setKickingId(participantId);
    try {
      await trainerService.kickParticipant(sessionId, participantId);
      setRoster((r) =>
        r ? { ...r, participants: r.participants.filter((p) => p.id !== participantId) } : r
      );
      toast.success(`${displayName} removed`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not remove participant');
    } finally {
      setKickingId(null);
    }
  };

  const lowerHand = async (participantId: number) => {
    setLoweringId(participantId);
    try {
      await trainerService.lowerHand(sessionId, participantId);
      setRoster((r) =>
        r
          ? {
              ...r,
              hands_raised: r.hands_raised.filter((h) => h.participant_id !== participantId),
              participants: r.participants.map((p) =>
                p.id === participantId ? { ...p, hand_raised: false, hand_raised_at: null } : p
              ),
            }
          : r
      );
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not lower hand');
    } finally {
      setLoweringId(null);
    }
  };

  // Parent subscribes and pushes updates down via a global event bus pattern would be
  // overkill here — this component listens directly via the same subscribe prop chain.
  return (
    <div className="space-y-4">
      {roster ? (
        <ConfusionMeter {...roster.confusion} />
      ) : (
        <div className="h-20 animate-pulse rounded-xl bg-gray-900/60" />
      )}

      {roster && roster.hands_raised.length > 0 && (
        <div className="rounded-xl border border-amber-900/40 bg-amber-950/20 p-3">
          <p className="mb-2 flex items-center gap-1.5 text-xs font-medium uppercase tracking-wide text-amber-500">
            <Hand className="h-3.5 w-3.5" />
            Raised hands ({roster.hands_raised.length})
          </p>
          <div className="space-y-1">
            {roster.hands_raised.map((h) => (
              <div
                key={h.participant_id}
                className="flex items-center justify-between gap-2 rounded-lg px-2 py-1.5"
              >
                <span className="truncate text-sm text-gray-200">{h.display_name}</span>
                <button
                  onClick={() => lowerHand(h.participant_id)}
                  disabled={loweringId === h.participant_id}
                  className="shrink-0 rounded-md border border-amber-800 px-2 py-1 text-[11px] font-medium text-amber-400 transition hover:bg-amber-900/40 disabled:opacity-50"
                >
                  Lower
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <DoubtQueue sessionId={sessionId} />

      <div className="space-y-1">
        {roster?.participants.length === 0 && (
          <p className="py-8 text-center text-sm text-gray-500">
            No one has joined yet. Share the join code above.
          </p>
        )}
        {roster?.participants.map((p) => (
          <div
            key={p.id}
            className="group flex items-center gap-3 rounded-lg px-3 py-2 transition hover:bg-gray-900/60"
          >
            <span className="relative flex h-2 w-2 shrink-0">
              {p.is_online && (
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-teal-400 opacity-75" />
              )}
              <span
                className={`relative inline-flex h-2 w-2 rounded-full ${
                  p.is_online ? 'bg-teal-500' : 'bg-gray-700'
                }`}
              />
            </span>
            <span
              className={`flex-1 truncate text-sm ${
                p.is_online ? 'text-gray-200' : 'text-gray-600'
              }`}
            >
              {p.display_name}
            </span>
            {p.hand_raised && p.is_online && (
              <Hand className="h-3.5 w-3.5 shrink-0 text-amber-400" />
            )}
            {p.is_guest && (
              <span className="rounded bg-gray-800 px-1.5 py-0.5 text-[10px] font-medium text-gray-500">
                Guest
              </span>
            )}
            {p.is_confused && p.is_online && (
              <Frown className="h-3.5 w-3.5 shrink-0 text-amber-400" />
            )}
            {p.is_online && (
              <button
                onClick={() => kick(p.id, p.display_name)}
                disabled={kickingId === p.id}
                title={`Remove ${p.display_name}`}
                className="shrink-0 rounded-md p-1 text-gray-700 opacity-0 transition hover:bg-red-950/60 hover:text-red-400 focus-visible:opacity-100 disabled:opacity-50 group-hover:opacity-100"
              >
                <UserX className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/** Reads the quiz questions out of a LectureAsset's loosely-typed config blob — same
 *  cast the presenter's own QuizSlide renderer and the CMS quiz editor already use. */
function quizQuestions(asset: LectureAsset): QuizQuestion[] {
  const config = asset.config as { questions?: QuizQuestion[] } | null;
  return config?.questions ?? [];
}

interface QuizPollLauncherProps {
  sessionId: number;
  quizAssets: ModuleAssetLink[];
  onLaunched: (poll: PollResultsResponse) => void;
}

function QuizPollLauncher({ sessionId, quizAssets, onLaunched }: QuizPollLauncherProps) {
  const [expanded, setExpanded] = useState(false);
  const [assetId, setAssetId] = useState('');
  const [questionIndex, setQuestionIndex] = useState('');
  const [launching, setLaunching] = useState(false);

  const selectedAsset = quizAssets.find((a) => String(a.asset.id) === assetId)?.asset ?? null;
  const questions = selectedAsset ? quizQuestions(selectedAsset) : [];

  const launch = async () => {
    if (!assetId || questionIndex === '') {
      toast.error('Pick a quiz question first');
      return;
    }
    setLaunching(true);
    try {
      const poll = await trainerService.createPollFromQuiz(
        sessionId,
        Number(assetId),
        Number(questionIndex)
      );
      onLaunched(poll);
      toast.success('Poll launched from quiz');
      setExpanded(false);
      setAssetId('');
      setQuestionIndex('');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not launch poll');
    } finally {
      setLaunching(false);
    }
  };

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/40">
      <button
        onClick={() => setExpanded((e) => !e)}
        className="flex w-full items-center justify-between gap-2 px-3 py-2.5 text-left"
      >
        <span className="flex items-center gap-1.5 text-xs font-medium text-gray-300">
          <ListChecks className="h-3.5 w-3.5 text-teal-500" />
          Launch from quiz
        </span>
        <ChevronDown
          className={`h-3.5 w-3.5 text-gray-500 transition-transform ${
            expanded ? 'rotate-180' : ''
          }`}
        />
      </button>
      {expanded && (
        <div className="space-y-2 border-t border-gray-800 p-3">
          <select
            value={assetId}
            onChange={(e) => {
              setAssetId(e.target.value);
              setQuestionIndex('');
            }}
            className="w-full rounded-lg border border-gray-800 bg-gray-900/60 px-2.5 py-1.5 text-xs text-gray-200 outline-none focus:border-teal-600"
          >
            <option value="">Choose a quiz…</option>
            {quizAssets.map((link) => (
              <option key={link.asset.id} value={link.asset.id}>
                {link.asset.title}
              </option>
            ))}
          </select>
          {selectedAsset && (
            <select
              value={questionIndex}
              onChange={(e) => setQuestionIndex(e.target.value)}
              className="w-full rounded-lg border border-gray-800 bg-gray-900/60 px-2.5 py-1.5 text-xs text-gray-200 outline-none focus:border-teal-600"
            >
              <option value="">Choose a question…</option>
              {questions.map((q, i) => (
                <option key={i} value={i}>
                  {q.question.length > 60 ? `${q.question.slice(0, 60)}…` : q.question}
                </option>
              ))}
            </select>
          )}
          <button
            onClick={launch}
            disabled={launching || !assetId || questionIndex === ''}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-teal-600/90 px-3 py-2 text-xs font-medium text-white transition hover:bg-teal-600 disabled:opacity-50"
          >
            <Send className="h-3.5 w-3.5" />
            {launching ? 'Launching…' : 'Launch'}
          </button>
        </div>
      )}
    </div>
  );
}

interface PollTabProps {
  sessionId: number;
  assets: ModuleAssetLink[];
  active: PollResultsResponse | null;
  onActiveChange: (poll: PollResultsResponse | null) => void;
}

function PollTab({ sessionId, assets, active, onActiveChange }: PollTabProps) {
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState(['', '']);
  const [creating, setCreating] = useState(false);
  const [closing, setClosing] = useState(false);

  const quizAssets = assets.filter((a) => a.asset.asset_type === 'quiz');
  const totalVotes = active ? Object.values(active.results).reduce((a, b) => a + b, 0) : 0;

  const addOption = () => {
    if (options.length >= 6) return;
    setOptions([...options, '']);
  };
  const removeOption = (i: number) => {
    if (options.length <= 2) return;
    setOptions(options.filter((_, idx) => idx !== i));
  };

  const launch = async () => {
    const cleaned = options.map((o) => o.trim()).filter(Boolean);
    if (!question.trim() || cleaned.length < 2) {
      toast.error('Add a question and at least 2 options');
      return;
    }
    setCreating(true);
    try {
      const poll = await trainerService.createPoll(sessionId, question.trim(), cleaned);
      onActiveChange(poll);
      setQuestion('');
      setOptions(['', '']);
      toast.success('Poll launched');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not launch poll');
    } finally {
      setCreating(false);
    }
  };

  const close = async () => {
    if (!active) return;
    setClosing(true);
    try {
      onActiveChange(await trainerService.closePoll(sessionId, active.id));
      toast.success('Poll closed');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not close poll');
    } finally {
      setClosing(false);
    }
  };

  if (active) {
    const isOpen = active.status === 'open';
    return (
      <div className="space-y-4">
        <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-4">
          <div className="mb-3 flex items-start justify-between gap-2">
            <p className="text-sm font-medium text-white">{active.question}</p>
            <span
              className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase ${
                isOpen ? 'bg-teal-900/50 text-teal-400' : 'bg-gray-800 text-gray-500'
              }`}
            >
              {isOpen ? 'Live' : 'Closed'}
            </span>
          </div>

          <div className="space-y-2">
            {active.options.map((opt, i) => {
              const count = active.results[i] ?? 0;
              const pct = totalVotes > 0 ? Math.round((count / totalVotes) * 100) : 0;
              const isCorrect = !isOpen && active.correct_option_index === i;
              return (
                <div
                  key={i}
                  className={
                    isCorrect
                      ? 'rounded-lg border border-green-700/60 bg-green-950/20 p-1.5'
                      : undefined
                  }
                >
                  <div className="mb-1 flex items-center justify-between text-xs">
                    <span
                      className={`flex items-center gap-1 ${
                        isCorrect ? 'text-green-300' : 'text-gray-300'
                      }`}
                    >
                      {opt}
                      {isCorrect && <CheckCircle2 className="h-3.5 w-3.5 text-green-400" />}
                    </span>
                    <span className="text-gray-500">
                      {count} · {pct}%
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-gray-800">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ease-out ${
                        isCorrect ? 'bg-green-500' : 'bg-teal-500'
                      }`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          <p className="mt-3 text-xs text-gray-500">{totalVotes} vote{totalVotes === 1 ? '' : 's'}</p>
        </div>

        {isOpen ? (
          <button
            onClick={close}
            disabled={closing}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-red-600/90 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-red-600 disabled:opacity-50"
          >
            <Square className="h-3.5 w-3.5" />
            {closing ? 'Closing…' : 'Close poll'}
          </button>
        ) : (
          <button
            onClick={() => onActiveChange(null)}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-700 px-4 py-2.5 text-sm font-medium text-gray-300 transition hover:bg-gray-800"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            New poll
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {quizAssets.length > 0 && (
        <QuizPollLauncher sessionId={sessionId} quizAssets={quizAssets} onLaunched={onActiveChange} />
      )}

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask the room a question…"
        rows={2}
        className="w-full resize-none rounded-lg border border-gray-800 bg-gray-900/60 px-3 py-2 text-sm text-white placeholder-gray-600 outline-none focus:border-teal-600"
      />
      <div className="space-y-2">
        {options.map((opt, i) => (
          <div key={i} className="flex items-center gap-2">
            <input
              value={opt}
              onChange={(e) =>
                setOptions(options.map((o, idx) => (idx === i ? e.target.value : o)))
              }
              placeholder={`Option ${i + 1}`}
              className="flex-1 rounded-lg border border-gray-800 bg-gray-900/60 px-3 py-2 text-sm text-white placeholder-gray-600 outline-none focus:border-teal-600"
            />
            {options.length > 2 && (
              <button
                onClick={() => removeOption(i)}
                className="shrink-0 rounded-lg p-2 text-gray-600 transition hover:bg-gray-800 hover:text-gray-300"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        ))}
      </div>
      {options.length < 6 && (
        <button
          onClick={addOption}
          className="flex items-center gap-1.5 text-xs font-medium text-teal-500 transition hover:text-teal-400"
        >
          <Plus className="h-3.5 w-3.5" />
          Add option
        </button>
      )}
      <button
        onClick={launch}
        disabled={creating}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-teal-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-teal-700 disabled:opacity-50"
      >
        <Send className="h-3.5 w-3.5" />
        {creating ? 'Launching…' : 'Launch poll'}
      </button>
    </div>
  );
}

function CodeTab({ sessionId }: { sessionId: number }) {
  const [language, setLanguage] = useState('python');
  const [content, setContent] = useState('');
  const [broadcasting, setBroadcasting] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const broadcast = (lang: string, code: string) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      setBroadcasting(true);
      try {
        await trainerService.updateLiveCode(sessionId, lang, code);
      } catch {
        // A missed broadcast tick self-heals on the next keystroke; no need to surface it.
      } finally {
        setBroadcasting(false);
      }
    }, 600);
  };

  return (
    <div className="flex h-full flex-col gap-3">
      <div className="flex items-center justify-between">
        <select
          value={language}
          onChange={(e) => {
            setLanguage(e.target.value);
            broadcast(e.target.value, content);
          }}
          className="rounded-lg border border-gray-800 bg-gray-900/60 px-2.5 py-1.5 text-xs font-medium text-gray-300 outline-none focus:border-teal-600"
        >
          {CODE_LANGUAGES.map((l) => (
            <option key={l} value={l}>
              {l.toUpperCase()}
            </option>
          ))}
        </select>
        <span
          className={`text-[10px] font-medium uppercase tracking-wide transition-opacity ${
            broadcasting ? 'text-teal-400 opacity-100' : 'text-gray-600 opacity-0'
          }`}
        >
          ● broadcasting
        </span>
      </div>
      <div className="min-h-0 flex-1 overflow-auto">
        <CodeEditor
          value={content}
          onChange={(val) => {
            setContent(val);
            broadcast(language, val);
          }}
          language={language}
          height="640px"
        />
      </div>
    </div>
  );
}

function QuestionsTab({ sessionId }: { sessionId: number }) {
  const {
    questions,
    questionsArePublic,
    setQuestions,
    setQuestionsArePublic,
    markQuestionAnswered,
  } = useClassroomStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initial fetch of questions (toggle state should ideally come from the session, 
    // but we can just fetch the session here too)
    const init = async () => {
      try {
        const [qList, session] = await Promise.all([
          trainerService.getQuestions(sessionId),
          trainerService.getSession(sessionId),
        ]);
        setQuestions(qList);
        setQuestionsArePublic(session.questions_are_public ?? false);
      } catch (err) {
        toast.error('Could not load questions');
      } finally {
        setLoading(false);
      }
    };
    void init();
  }, [sessionId, setQuestions, setQuestionsArePublic]);

  const togglePublic = async () => {
    try {
      const updated = await trainerService.setQuestionsArePublic(sessionId, !questionsArePublic);
      setQuestionsArePublic(updated.questions_are_public ?? false);
      toast.success(updated.questions_are_public ? 'Questions are now visible to students' : 'Questions are now hidden from students');
    } catch (err) {
      toast.error('Could not change visibility');
    }
  };

  const markAnswered = async (questionId: number) => {
    try {
      await trainerService.answerQuestion(sessionId, questionId);
      markQuestionAnswered(questionId);
      toast.success('Marked as answered');
    } catch (err) {
      toast.error('Could not mark question as answered');
    }
  };

  if (loading) {
    return <div className="p-4 text-center text-sm text-gray-500">Loading questions...</div>;
  }

  return (
    <div className="flex h-full flex-col gap-4">
      <div className="flex items-center justify-between rounded-xl border border-gray-800 bg-gray-900/40 p-3">
        <div className="flex flex-col">
          <span className="text-sm font-medium text-gray-200">Public Q&A</span>
          <span className="text-xs text-gray-500">Allow students to see and upvote</span>
        </div>
        <button
          onClick={togglePublic}
          className={`relative inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-2 focus-visible:ring-offset-gray-900 ${
            questionsArePublic ? 'bg-teal-500' : 'bg-gray-700'
          }`}
        >
          <span
            className={`inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
              questionsArePublic ? 'translate-x-4' : 'translate-x-0'
            }`}
          />
        </button>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto">
        {questions.length === 0 ? (
          <p className="py-8 text-center text-sm text-gray-500">No questions asked yet.</p>
        ) : (
          questions.map((q) => (
            <div
              key={q.id}
              className={`rounded-xl border border-gray-800 p-3 transition ${
                q.is_answered ? 'bg-gray-900/30 opacity-70' : 'bg-gray-900/60'
              }`}
            >
              <div className="mb-2 flex items-start justify-between gap-3">
                <p className={`text-sm ${q.is_answered ? 'text-gray-400 line-through decoration-gray-600/50' : 'text-gray-200'}`}>
                  {q.question_text}
                </p>
                <div className="flex shrink-0 items-center gap-1 text-xs font-medium text-gray-500">
                  <ThumbsUp className="h-3 w-3" />
                  {q.upvotes}
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">{q.student_name || 'Guest'}</span>
                {!q.is_answered && (
                  <button
                    onClick={() => markAnswered(q.id)}
                    className="flex items-center gap-1.5 rounded-md border border-teal-900/50 bg-teal-950/30 px-2 py-1 text-[11px] font-medium text-teal-400 transition hover:bg-teal-900/40 hover:text-teal-300"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Mark answered
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function formatCountdown(totalSeconds: number): string {
  const clamped = Math.max(0, Math.round(totalSeconds));
  const mins = Math.floor(clamped / 60);
  const secs = clamped % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/** Reads the clock, same as the elapsed-time helper on the session detail page —
 *  pulled out to a named function rather than inlined so the impure Date.now() read
 *  isn't sitting directly in the render body. */
function secondsRemaining(timer: TimerView): number {
  return Math.max(
    0,
    timer.duration_seconds - (Date.now() - new Date(timer.started_at).getTime()) / 1000
  );
}

/** Compact always-visible strip so a trainer running a timed exercise can glance at
 *  the countdown without leaving whichever tab they're on. Owns its own composer state
 *  (duration input, busy flag); the running timer itself is lifted to the parent since
 *  it must survive tab switches and be driven by WS events from any device. */
function TimerStrip({ sessionId, timer }: { sessionId: number; timer: TimerView | null }) {
  const [durationInput, setDurationInput] = useState('5');
  const [busy, setBusy] = useState(false);
  // A tick counter, not the countdown value itself — mirrors the elapsed-time clock on
  // the session detail page. Only ever set from inside the interval callback (an
  // external-system subscription), never synchronously in the effect body, so the
  // actual remaining seconds is derived fresh in the render below instead of stored.
  const [, setTick] = useState(0);

  useEffect(() => {
    if (!timer) return;
    const interval = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(interval);
  }, [timer]);

  const remaining = timer ? secondsRemaining(timer) : 0;

  const start = async () => {
    const mins = Number(durationInput);
    if (!mins || mins <= 0) {
      toast.error('Enter a duration in minutes');
      return;
    }
    setBusy(true);
    try {
      await trainerService.startTimer(sessionId, Math.round(mins * 60));
      // No optimistic local update — the timer_started broadcast (which reaches this
      // same trainer socket too) is the single source of truth for started_at, so the
      // countdown here always matches what students see rather than drifting on clock skew.
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not start timer');
    } finally {
      setBusy(false);
    }
  };

  const cancel = async () => {
    setBusy(true);
    try {
      await trainerService.cancelTimer(sessionId);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not cancel timer');
    } finally {
      setBusy(false);
    }
  };

  const isDone = timer !== null && remaining <= 0;

  return (
    <div className="flex items-center gap-2 border-b border-gray-800 bg-gray-900/30 px-3 py-2">
      <Timer
        className={`h-3.5 w-3.5 shrink-0 ${
          timer ? (isDone ? 'text-red-400' : 'text-teal-400') : 'text-gray-600'
        }`}
      />
      {timer ? (
        <>
          <span
            className={`flex-1 font-mono text-sm font-semibold tabular-nums ${
              isDone ? 'text-red-400' : 'text-white'
            }`}
          >
            {formatCountdown(remaining)}
          </span>
          <button
            onClick={cancel}
            disabled={busy}
            className="shrink-0 rounded-md border border-gray-700 px-2 py-1 text-[11px] font-medium text-gray-400 transition hover:bg-gray-800 hover:text-white disabled:opacity-50"
          >
            Cancel
          </button>
        </>
      ) : (
        <>
          <span className="text-[11px] text-gray-500">Timer</span>
          <input
            type="number"
            min={1}
            value={durationInput}
            onChange={(e) => setDurationInput(e.target.value)}
            className="w-14 rounded-md border border-gray-800 bg-gray-900/60 px-2 py-1 text-xs text-white outline-none focus:border-teal-600"
          />
          <span className="text-[11px] text-gray-500">min</span>
          <button
            onClick={start}
            disabled={busy}
            className="ml-auto shrink-0 rounded-md bg-teal-600 px-2.5 py-1 text-[11px] font-medium text-white transition hover:bg-teal-700 disabled:opacity-50"
          >
            {busy ? 'Starting…' : 'Start'}
          </button>
        </>
      )}
    </div>
  );
}

interface FloatingReaction {
  id: number;
  emoji: string;
  displayName: string;
}

export function ClassroomPanel({ sessionId, connected, subscribe, assets }: Props) {
  const [open, setOpen] = useState(true);
  const [wide, setWide] = useState(false);
  const [tab, setTab] = useState<Tab>('roster');
  const [rosterTick, setRosterTick] = useState(0);
  const [activePoll, setActivePoll] = useState<PollResultsResponse | null>(null);
  const activePollRef = useRef<PollResultsResponse | null>(null);
  const [timer, setTimer] = useState<TimerView | null>(null);
  const [reactions, setReactions] = useState<FloatingReaction[]>([]);
  const reactionIdRef = useRef(0);
  
  const { addQuestion, updateQuestionUpvotes, markQuestionAnswered, setQuestionsArePublic } = useClassroomStore();

  useEffect(() => {
    activePollRef.current = activePoll;
  }, [activePoll]);

  // Seed the timer strip from the REST roster once on mount so a page refresh mid-
  // countdown doesn't lose track of a timer already running — live changes after that
  // come from the timer_started / timer_cancelled WS events below.
  useEffect(() => {
    void trainerService
      .getRoster(sessionId)
      .then((r) => setTimer(r.timer))
      .catch(() => {});
  }, [sessionId]);

  const addReaction = useCallback((emoji: string, displayName: string) => {
    const id = ++reactionIdRef.current;
    setReactions((prev) => [...prev, { id, emoji, displayName }]);
    setTimeout(() => {
      setReactions((prev) => prev.filter((r) => r.id !== id));
    }, 2000);
  }, []);

  useEffect(() => {
    return subscribe((event) => {
      if (event.type === 'roster_changed') {
        setRosterTick((t) => t + 1);
        return;
      }
      if (event.type === 'timer_started') {
        setTimer(event.payload);
        return;
      }
      if (event.type === 'timer_cancelled') {
        setTimer(null);
        return;
      }
      if (event.type === 'reaction') {
        addReaction(event.payload.emoji, event.payload.display_name);
        return;
      }

      const current = activePollRef.current;
      if (event.type === 'poll_vote_cast') {
        if (current && current.status === 'open' && current.id === event.payload.poll_id) {
          void trainerService
            .getPollResults(sessionId, current.id)
            .then(setActivePoll)
            .catch(() => {});
        }
      } else if (event.type === 'poll_closed') {
        if (current && current.id === event.payload.id) {
          setActivePoll({
            ...current,
            status: 'closed',
            results: event.payload.results,
            total_votes: event.payload.total_votes,
          });
        }
      } else if (event.type === 'question_asked') {
        addQuestion(event.payload);
      } else if (event.type === 'question_upvoted') {
        updateQuestionUpvotes(event.payload.question_id, event.payload.upvotes);
      } else if (event.type === 'question_answered') {
        markQuestionAnswered(event.payload.question_id);
      } else if (event.type === 'questions_visibility_changed') {
        setQuestionsArePublic(event.payload.questions_are_public);
      } else if (event.type === 'quiz_attempt_submitted') {
        const { display_name, score, total_questions, passed } = event.payload;
        if (passed) {
          toast.success(`${display_name} passed the quiz: ${score}/${total_questions}`, {
            duration: 4000,
          });
        } else {
          toast(`${display_name} submitted quiz: ${score}/${total_questions}`, {
            duration: 4000,
            icon: '📝',
          });
        }
      } else if (event.type === 'doubt_requested') {
        const { doubt_id, participant_id, display_name } = event.payload;
        useClassroomStore.getState().addDoubtRequest({
          id: doubt_id,
          participant_id,
          display_name,
          status: 'pending',
          requested_at: new Date().toISOString()
        });
      } else if (event.type === 'doubt_approved') {
        useClassroomStore.getState().updateDoubtRequest(event.payload.id, { 
          status: 'approved',
          whep_url: event.payload.whep_url
        });
      } else if (event.type === 'doubt_completed') {
        useClassroomStore.getState().updateDoubtRequest(event.payload.id, { 
          status: 'completed'
        });
      }
      // poll_open / session_ended: the trainer is the one who triggers these, nothing
      // to react to here. slide_change / code_update: broadcast BY the trainer, not
      // received. participant_kicked: only actionable on the student app — the
      // roster_changed broadcast that follows a kick already updates this roster.
    });
  }, [subscribe, sessionId, addReaction]);

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed right-4 top-1/2 z-40 -translate-y-1/2 rounded-l-xl border border-r-0 border-gray-800 bg-gray-900 p-2.5 text-gray-400 shadow-xl transition hover:text-white"
        title="Open classroom panel"
      >
        <PanelRightOpen className="h-5 w-5" />
      </button>
    );
  }

  return (
    <aside
      className={`relative flex shrink-0 flex-col border-l border-gray-800 bg-gray-950 transition-all duration-300 ${
        wide ? 'w-[560px]' : 'w-[380px]'
      }`}
    >
      <AudioMixer />
      <div className="flex items-center justify-between border-b border-gray-800 px-3 py-2.5">
        <div className="flex items-center gap-2">
          {connected ? (
            <Wifi className="h-3.5 w-3.5 text-teal-500" />
          ) : (
            <WifiOff className="h-3.5 w-3.5 animate-pulse text-amber-500" />
          )}
          <span className="text-xs text-gray-500">{connected ? 'Live' : 'Reconnecting…'}</span>
        </div>
        <div className="flex items-center gap-1">
          {tab === 'code' && (
            <button
              onClick={() => setWide((w) => !w)}
              className="rounded-md p-1.5 text-gray-500 transition hover:bg-gray-800 hover:text-gray-300"
              title={wide ? 'Narrow panel' : 'Widen panel'}
            >
              {wide ? <Minimize2 className="h-3.5 w-3.5" /> : <Maximize2 className="h-3.5 w-3.5" />}
            </button>
          )}
          <button
            onClick={() => setOpen(false)}
            className="rounded-md p-1.5 text-gray-500 transition hover:bg-gray-800 hover:text-gray-300"
            title="Close panel"
          >
            <PanelRightClose className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      <TimerStrip sessionId={sessionId} timer={timer} />

      <div className="flex border-b border-gray-800">
        {(
          [
            { id: 'roster' as const, label: 'Roster', icon: Users },
            { id: 'poll' as const, label: 'Poll', icon: BarChart3 },
            { id: 'questions' as const, label: 'Q&A', icon: MessageCircleQuestion },
            { id: 'code' as const, label: 'Code', icon: Code2 },
          ]
        ).map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setTab(id)}
            className={`flex flex-1 items-center justify-center gap-1.5 border-b-2 py-2.5 text-xs font-medium transition ${
              tab === id
                ? 'border-teal-500 text-white'
                : 'border-transparent text-gray-500 hover:text-gray-300'
            }`}
          >
            <Icon className="h-3.5 w-3.5" />
            {label}
          </button>
        ))}
      </div>

      <div className={`min-h-0 flex-1 ${tab === 'code' ? 'flex flex-col p-3' : 'overflow-auto p-4'}`}>
        {tab === 'roster' && <RosterTab key={rosterTick} sessionId={sessionId} />}
        {tab === 'poll' && (
          <PollTab
            sessionId={sessionId}
            assets={assets}
            active={activePoll}
            onActiveChange={setActivePoll}
          />
        )}
        {tab === 'questions' && <QuestionsTab sessionId={sessionId} />}
        {tab === 'code' && <CodeTab sessionId={sessionId} />}
      </div>

      {reactions.length > 0 && (
        <div className="pointer-events-none absolute inset-x-0 bottom-20 z-30 flex flex-col items-center gap-1.5 px-4">
          {reactions.map((r) => (
            <span
              key={r.id}
              className="animate-reaction-float flex items-center gap-1.5 rounded-full bg-gray-900/90 px-3 py-1 text-sm text-white shadow-lg"
            >
              <span className="text-base leading-none">{r.emoji}</span>
              <span className="text-xs text-gray-400">{r.displayName}</span>
            </span>
          ))}
        </div>
      )}
    </aside>
  );
}
