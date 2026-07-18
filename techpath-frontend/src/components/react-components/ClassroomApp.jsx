import { useCallback, useEffect, useRef, useState } from 'react';
import ClassroomCodeInput from './ClassroomCodeInput';
import ClassroomAssetView from './ClassroomAssetView';
import ClassroomConfusionButton from './ClassroomConfusionButton';
import ClassroomPollSheet from './ClassroomPollSheet';
import ClassroomHandRaiseButton from './ClassroomHandRaiseButton';
import ClassroomReactionsBar from './ClassroomReactionsBar';
import ClassroomTimerBadge from './ClassroomTimerBadge';
import ClassroomVideoTile from './ClassroomVideoTile';
import ClassroomQuestionsPanel from './ClassroomQuestionsPanel';
import { MessageCircleQuestion } from 'lucide-react';
import {
  joinClassroom,
  identify,
  getState,
  setConfusion,
  vote,
  setHandRaised as requestHandRaised,
  sendReaction,
} from '@/services/classroomService';
import { useClassroomSocket } from '@/hooks/useClassroomSocket';

const STORAGE_KEY = 'techpath_classroom_session';

function loadStoredSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function storeSession(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch {
    // Private browsing / storage disabled — the session still works, it just won't
    // survive a page refresh.
  }
}

function clearStoredSession() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // Nothing to clean up if storage was never writable.
  }
}

function Glow() {
  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden">
      <div className="absolute left-1/2 top-0 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary-500/20 blur-[120px]" />
      <div className="absolute bottom-0 right-0 h-[500px] w-[500px] translate-x-1/3 translate-y-1/3 rounded-full bg-secondary-500/15 blur-[120px]" />
    </div>
  );
}

function Shell({ children }) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-950 px-4 py-10">
      <Glow />
      <div className="relative w-full max-w-md">{children}</div>
    </div>
  );
}

function Brand() {
  return (
    <div className="mb-8 flex items-center justify-center gap-2">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 font-heading text-lg font-bold text-white">
        T
      </div>
      <span className="font-heading text-lg font-semibold text-white">TechPath</span>
    </div>
  );
}

function JoinScreen({ code, onCodeChange, onSubmit, joining, error }) {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl backdrop-blur">
        <h1 className="text-center font-heading text-2xl font-bold text-white">
          Join a live class
        </h1>
        <p className="mx-auto mt-2 max-w-xs text-center text-sm text-slate-400">
          Enter the 6-digit code your trainer shared on screen.
        </p>

        <div className="mt-8">
          <ClassroomCodeInput
            value={code}
            onChange={onCodeChange}
            onSubmit={onSubmit}
            disabled={joining}
            error={error}
          />
        </div>

        <button
          onClick={() => onSubmit(code)}
          disabled={code.length !== 6 || joining}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-primary-500 py-3.5 font-medium text-white transition hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {joining ? (
            <>
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
              Checking…
            </>
          ) : (
            'Join classroom'
          )}
        </button>
      </div>
      <p className="mt-6 text-center text-xs text-slate-600">
        <a href="/" className="transition hover:text-slate-400">
          techpath.biz
        </a>
      </p>
    </Shell>
  );
}

function IdentifyScreen({
  sessionInfo,
  email,
  onEmailChange,
  onEmailSubmit,
  guestName,
  onGuestNameChange,
  onGuestSubmit,
  needsGuestName,
  onSkipToGuest,
  identifying,
  error,
}) {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl backdrop-blur">
        <div className="mb-6 rounded-xl border border-primary-500/20 bg-primary-500/5 p-4 text-center">
          <p className="text-xs uppercase tracking-wide text-primary-400">You're joining</p>
          <p className="mt-1 font-heading font-semibold text-white">{sessionInfo.batch_name}</p>
          {sessionInfo.session_title && (
            <p className="text-sm text-slate-400">{sessionInfo.session_title}</p>
          )}
        </div>

        {!needsGuestName ? (
          <>
            <h2 className="text-center text-lg font-semibold text-white">What's your email?</h2>
            <p className="mt-1 text-center text-sm text-slate-400">
              We'll match you against the class roster.
            </p>
            <input
              type="email"
              value={email}
              onChange={(e) => onEmailChange(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onEmailSubmit()}
              placeholder="you@example.com"
              className="mt-5 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white placeholder-slate-600 outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/30"
              autoFocus
            />
            {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
            <button
              onClick={onEmailSubmit}
              disabled={!email.trim() || identifying}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-primary-500 py-3.5 font-medium text-white transition hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {identifying ? 'Checking…' : 'Continue'}
            </button>
            <button
              onClick={onSkipToGuest}
              className="mt-3 w-full text-center text-sm text-slate-500 transition hover:text-slate-300"
            >
              Continue as a guest instead
            </button>
          </>
        ) : (
          <>
            <h2 className="text-center text-lg font-semibold text-white">
              What should we call you?
            </h2>
            <p className="mt-1 text-center text-sm text-slate-400">
              We couldn't match that email to the roster — no problem, join as a guest.
            </p>
            <input
              type="text"
              value={guestName}
              onChange={(e) => onGuestNameChange(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onGuestSubmit()}
              placeholder="Your name"
              className="mt-5 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-white placeholder-slate-600 outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/30"
              autoFocus
            />
            {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
            <button
              onClick={onGuestSubmit}
              disabled={identifying}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-primary-500 py-3.5 font-medium text-white transition hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {identifying ? 'Joining…' : 'Join classroom'}
            </button>
          </>
        )}
      </div>
    </Shell>
  );
}

function EndedScreen() {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-10 text-center shadow-2xl backdrop-blur">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-accent-500/10 text-2xl">
          👋
        </div>
        <h1 className="font-heading text-xl font-bold text-white">Session ended</h1>
        <p className="mt-2 text-sm text-slate-400">
          Thanks for joining! Your trainer has wrapped up this class.
        </p>
        <a
          href="/"
          className="mt-6 inline-block rounded-xl bg-primary-500 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600"
        >
          Back to techpath.biz
        </a>
      </div>
    </Shell>
  );
}

function RemovedScreen() {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-10 text-center shadow-2xl backdrop-blur">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-red-500/10 text-2xl">
          🚫
        </div>
        <h1 className="font-heading text-xl font-bold text-white">You've been removed</h1>
        <p className="mt-2 text-sm text-slate-400">
          Your trainer removed you from this session. If you think that's a mistake,
          reach out to them directly.
        </p>
        <a
          href="/"
          className="mt-6 inline-block rounded-xl bg-primary-500 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600"
        >
          Back to techpath.biz
        </a>
      </div>
    </Shell>
  );
}

function LiveCodeView({ code }) {
  return (
    <div className="flex flex-col h-[calc(100vh-160px)] overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
      <div className="flex shrink-0 items-center gap-2 border-b border-slate-800 bg-slate-800/60 px-4 py-2.5">
        <span className="h-3 w-3 rounded-full bg-red-500/80" />
        <span className="h-3 w-3 rounded-full bg-yellow-500/80" />
        <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
        <span className="ml-3 rounded bg-slate-700/60 px-2 py-0.5 font-mono text-xs text-slate-300">
          {code.language}
        </span>
        <span className="ml-auto flex items-center gap-1.5 text-[10px] font-medium uppercase tracking-wide text-primary-400">
          <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-primary-400" />
          live
        </span>
      </div>
      <pre className="flex-1 overflow-auto p-5 text-sm leading-relaxed">
        <code className="font-mono text-slate-100">{code.content || '// waiting for code…'}</code>
      </pre>
    </div>
  );
}

function LiveScreen({
  liveState,
  connected,
  contentTab,
  onTabChange,
  onConfusionToggle,
  onVote,
  onLeave,
  handRaised,
  onHandRaiseToggle,
  floatingReactions,
  onSendReaction,
  qaOpen,
  setQaOpen,
  questions,
  setQuestions,
  sessionInfo,
  session,
}) {
  const hasCode = !!liveState.code?.content;
  const asset = liveState.current_asset;
  const hasMedia = !!liveState.media?.whep_url;
  // Offset the sticky video so it parks just under the (also-sticky) header. The header
  // is taller when the Slide/Code tab row is present, so clear the correct amount.
  const stickyTop = hasCode ? 'top-[104px]' : 'top-[68px]';

  const contentBlock =
    contentTab === 'code' && hasCode ? (
      <LiveCodeView code={liveState.code} />
    ) : asset ? (
      <>
        <div className="mb-4">
          <p className="text-xs font-medium uppercase tracking-wide text-primary-400">
            Now presenting
          </p>
          <h2 className="mt-0.5 font-heading text-xl font-bold text-white">{asset.title}</h2>
        </div>
        <ClassroomAssetView asset={asset} />
      </>
    ) : (
      <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 py-24 text-center">
        <div className="mb-3 text-3xl">⏳</div>
        <p className="font-medium text-slate-300">Waiting for your trainer</p>
        <p className="mt-1 text-sm text-slate-500">
          Content will appear here as soon as they start presenting.
        </p>
      </div>
    );

  return (
    <div className="min-h-screen bg-slate-950">
      <header className="sticky top-0 z-30 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div className="min-w-0">
            <p className="truncate font-heading text-sm font-semibold text-white">
              {liveState.title || liveState.module_title || liveState.batch_name}
            </p>
            <p className="truncate text-xs text-slate-500">{liveState.batch_name}</p>
          </div>
          <div className="flex shrink-0 items-center gap-3">
            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <span
                className={`h-1.5 w-1.5 rounded-full ${connected ? 'bg-accent-400' : 'animate-pulse bg-amber-400'}`}
              />
              {liveState.presence.online} online
            </span>
            <ClassroomTimerBadge timer={liveState.timer} />
            <button
              onClick={onLeave}
              className="rounded-lg px-2.5 py-1.5 text-xs text-slate-500 transition hover:bg-slate-800 hover:text-slate-300"
            >
              Leave
            </button>
          </div>
        </div>

        {hasCode && (
          <div className="mx-auto flex max-w-6xl gap-1 px-4 pb-2">
            <button
              onClick={() => onTabChange('slide')}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                contentTab === 'slide'
                  ? 'bg-primary-500/15 text-primary-300'
                  : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              📄 Slide
            </button>
            <button
              onClick={() => onTabChange('code')}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                contentTab === 'code'
                  ? 'bg-primary-500/15 text-primary-300'
                  : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              💻 Live code
            </button>
          </div>
        )}
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6 pb-28">
        {hasMedia ? (
          // Two-pane on desktop: the live video is the hero and stays pinned (sticky) as
          // the lecture content scrolls beside it. On mobile it stacks and the video
          // pins to the top so it never scrolls out of view — see stickyTop above.
          <div className="grid gap-6 lg:grid-cols-5">
            <div className={`sticky ${stickyTop} z-10 self-start lg:col-span-3`}>
              <ClassroomVideoTile media={liveState.media} />
            </div>
            <div className="min-w-0 lg:col-span-2">{contentBlock}</div>
          </div>
        ) : (
          <div className="mx-auto max-w-3xl">{contentBlock}</div>
        )}
      </main>

      {/* z-50: an open poll sheet is z-40 and can grow tall enough to span this whole
          corner (confirmed by measuring a real session) — these two controls need to
          stay reachable even then, unlike the confusion button below, which the poll
          sheet is already known to cover (existing, accepted tradeoff, left as-is). */}
      <div className="fixed bottom-24 right-4 z-50 flex items-center gap-2 sm:right-6">
        {liveState?.questions_are_public && (
          <button
            onClick={() => setQaOpen(true)}
            className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-800 text-slate-300 shadow-xl transition hover:bg-slate-700 hover:text-white"
            title="Q&A"
          >
            <MessageCircleQuestion className="h-5 w-5" />
          </button>
        )}
        <ClassroomHandRaiseButton raised={handRaised} onToggle={onHandRaiseToggle} />
        <ClassroomReactionsBar onSend={onSendReaction} floating={floatingReactions} />
      </div>
      <ClassroomConfusionButton confused={liveState.my_confusion} onToggle={onConfusionToggle} />
      <ClassroomPollSheet key={liveState.open_poll?.id ?? 'none'} poll={liveState.open_poll} onVote={onVote} />
      <ClassroomQuestionsPanel
        sessionId={session?.sessionId}
        token={session?.token}
        isOpen={qaOpen}
        onClose={() => setQaOpen(false)}
        questions={questions}
        setQuestions={setQuestions}
      />
    </div>
  );
}

export default function ClassroomApp() {
  const [stage, setStage] = useState('loading');

  const [joinCode, setJoinCode] = useState('');
  const [joining, setJoining] = useState(false);
  const [joinError, setJoinError] = useState('');
  const [sessionInfo, setSessionInfo] = useState(null);

  const [email, setEmail] = useState('');
  const [guestName, setGuestName] = useState('');
  const [needsGuestName, setNeedsGuestName] = useState(false);
  const [identifying, setIdentifying] = useState(false);
  const [identifyError, setIdentifyError] = useState('');

  const [session, setSession] = useState(null);
  const [liveState, setLiveState] = useState(null);
  const [contentTab, setContentTab] = useState('slide');

  // Not part of SessionStateResponse (backend gap — see hand-raise handler below), so
  // this is tracked as plain optimistic local state rather than derived from liveState.
  // A page refresh mid-session will visually reset this even if the trainer's roster
  // still shows the hand raised — known, acceptable limitation.
  const [handRaised, setHandRaisedFlag] = useState(false);
  const [floatingReactions, setFloatingReactions] = useState([]);
  const reactionIdRef = useRef(0);

  const [qaOpen, setQaOpen] = useState(false);
  const [questions, setQuestions] = useState([]);

  const { connected, subscribe, kicked } = useClassroomSocket(
    session?.sessionId ?? null,
    session?.token ?? null,
    stage === 'live'
  );

  useEffect(() => {
    const stored = loadStoredSession();
    if (!stored) {
      setStage('join');
      return;
    }
    (async () => {
      const res = await getState(stored.sessionId, stored.token);
      if (res.success && res.data) {
        setSession(stored);
        setLiveState(res.data);
        setStage(res.data.status === 'ended' ? 'ended' : 'live');
      } else {
        clearStoredSession();
        setStage('join');
      }
    })();
  }, []);

  useEffect(() => {
    if (!kicked) return;
    // Same pattern as the session_ended WS event below — the socket hook already
    // stopped reconnecting once it saw the 4403 close, this just moves the UI to a
    // terminal screen instead of leaving the student staring at a dead connection.
    clearStoredSession();
    setStage('removed');
  }, [kicked]);

  useEffect(() => {
    if (stage !== 'live') return undefined;
    return subscribe((event) => {
      if (event.type === 'slide_change') {
        setLiveState((s) => (s ? { ...s, current_asset: event.payload.asset } : s));
      } else if (event.type === 'media_state_changed') {
        // Only ever fires once media already exists on liveState (the trainer can't
        // toggle mute/camera/screen-share before publishing) — merge onto the existing
        // block rather than replacing it, so whep_url/hls_url are untouched.
        setLiveState((s) => (s && s.media ? { ...s, media: { ...s.media, ...event.payload } } : s));
      } else if (event.type === 'code_update') {
        setLiveState((s) => (s ? { ...s, code: event.payload } : s));
      } else if (event.type === 'poll_open') {
        setLiveState((s) =>
          s
            ? {
                ...s,
                open_poll: {
                  id: event.payload.id,
                  question: event.payload.question,
                  options: event.payload.options,
                  status: 'open',
                  my_vote: null,
                  results: null,
                },
              }
            : s
        );
      } else if (event.type === 'poll_closed') {
        setLiveState((s) =>
          s && s.open_poll && s.open_poll.id === event.payload.id
            ? {
                ...s,
                open_poll: {
                  ...s.open_poll,
                  status: 'closed',
                  results: event.payload.results,
                  correct_option_index: event.payload.correct_option_index ?? null,
                },
              }
            : s
        );
      } else if (event.type === 'timer_started') {
        setLiveState((s) => (s ? { ...s, timer: event.payload } : s));
      } else if (event.type === 'timer_cancelled') {
        setLiveState((s) => (s ? { ...s, timer: null } : s));
      } else if (event.type === 'reaction') {
        reactionIdRef.current += 1;
        const id = reactionIdRef.current;
        setFloatingReactions((list) => {
          const next = [
            ...list,
            { id, emoji: event.payload.emoji, display_name: event.payload.display_name },
          ];
          // Cap concurrent bubbles so a reaction-spam moment can't leak memory or clutter
          // the screen — drop the oldest once there are more than a handful in flight.
          return next.length > 5 ? next.slice(next.length - 5) : next;
        });
        window.setTimeout(() => {
          setFloatingReactions((list) => list.filter((r) => r.id !== id));
        }, 2000);
      } else if (event.type === 'session_ended') {
        clearStoredSession();
        setStage('ended');
      } else if (event.type === 'question_asked') {
        setQuestions((list) => [event.payload, ...list]);
      } else if (event.type === 'question_upvoted') {
        setQuestions((list) =>
          list.map((q) => (q.id === event.payload.question_id ? { ...q, upvotes: event.payload.upvotes } : q))
        );
      } else if (event.type === 'question_answered') {
        setQuestions((list) =>
          list.map((q) => (q.id === event.payload.question_id ? { ...q, is_answered: true } : q))
        );
      } else if (event.type === 'questions_visibility_changed') {
        setLiveState((s) => (s ? { ...s, questions_are_public: event.payload.questions_are_public } : s));
      }
      // `participant_kicked` is a broadcast about someone else being removed — this app
      // has no roster view to update. This student's own removal arrives as the socket
      // closing with code 4403, handled by the `kicked` effect above instead.
    });
  }, [stage, subscribe]);

  const handleJoin = useCallback(
    async (explicitCode) => {
      // ClassroomCodeInput passes the just-assembled code directly when auto-submitting
      // on the 6th digit — at that point setJoinCode(joined) hasn't flushed yet, so
      // reading joinCode from this closure would still see the stale, pre-update value.
      const code = typeof explicitCode === 'string' ? explicitCode : joinCode;
      if (code.length !== 6 || joining) return;
      setJoining(true);
      setJoinError('');
      const res = await joinClassroom(code);
      setJoining(false);
      if (res.success && res.data) {
        setSessionInfo(res.data);
        setStage('identify');
      } else {
        setJoinError(res.error || "That code isn't valid right now.");
      }
    },
    [joinCode, joining]
  );

  const completeIdentify = async (params) => {
    setIdentifying(true);
    setIdentifyError('');
    const res = await identify({ sessionId: sessionInfo.session_id, ...params });
    setIdentifying(false);
    if (!res.success || !res.data) {
      setIdentifyError(res.error || 'Something went wrong. Try again.');
      return;
    }
    if (res.data.token) {
      const stored = {
        sessionId: sessionInfo.session_id,
        token: res.data.token,
        displayName: res.data.display_name,
      };
      storeSession(stored);
      setSession(stored);
      const stateRes = await getState(stored.sessionId, stored.token);
      if (stateRes.success && stateRes.data) {
        setLiveState(stateRes.data);
        setStage('live');
      }
    } else {
      setNeedsGuestName(true);
    }
  };

  const handleConfusionToggle = async (confused) => {
    if (!session) return;
    setLiveState((s) => (s ? { ...s, my_confusion: confused } : s));
    await setConfusion(session.sessionId, session.token, confused);
  };

  const handleVote = async (optionIndex) => {
    if (!session || !liveState?.open_poll) return;
    const res = await vote(session.sessionId, session.token, liveState.open_poll.id, optionIndex);
    if (res.success && res.data) setLiveState(res.data);
  };

  const handleHandRaiseToggle = async (raised) => {
    if (!session) return;
    setHandRaisedFlag(raised);
    // The response is the same SessionStateResponse bootstrap shape as setConfusion,
    // but it doesn't report hand-raised state back (backend gap) — nothing useful to do
    // with it here, same fire-and-forget as handleConfusionToggle above.
    await requestHandRaised(session.sessionId, session.token, raised);
  };

  const handleSendReaction = async (emoji) => {
    if (!session) return;
    // A cooldown rejection from the server is a soft no-op by design (see
    // ClassroomReactionsBar) — nothing to update either way, so the result is ignored.
    await sendReaction(session.sessionId, session.token, emoji);
  };

  const handleLeave = () => {
    clearStoredSession();
    setSession(null);
    setLiveState(null);
    setSessionInfo(null);
    setJoinCode('');
    setHandRaisedFlag(false);
    setStage('join');
  };

  if (stage === 'loading') {
    return (
      <Shell>
        <div className="flex justify-center">
          <span className="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-primary-500" />
        </div>
      </Shell>
    );
  }

  if (stage === 'join') {
    return (
      <JoinScreen
        code={joinCode}
        onCodeChange={setJoinCode}
        onSubmit={handleJoin}
        joining={joining}
        error={joinError}
      />
    );
  }

  if (stage === 'identify') {
    return (
      <IdentifyScreen
        sessionInfo={sessionInfo}
        email={email}
        onEmailChange={setEmail}
        onEmailSubmit={() => completeIdentify({ email: email.trim() })}
        guestName={guestName}
        onGuestNameChange={setGuestName}
        onGuestSubmit={() => completeIdentify({ guestName: guestName.trim() || 'Guest' })}
        needsGuestName={needsGuestName}
        onSkipToGuest={() => setNeedsGuestName(true)}
        identifying={identifying}
        error={identifyError}
      />
    );
  }

  if (stage === 'ended') {
    return <EndedScreen />;
  }

  if (stage === 'removed') {
    return <RemovedScreen />;
  }

  return (
    <LiveScreen
      liveState={liveState}
      connected={connected}
      contentTab={contentTab}
      onTabChange={setContentTab}
      onConfusionToggle={handleConfusionToggle}
      onVote={handleVote}
      onLeave={handleLeave}
      handRaised={handRaised}
      onHandRaiseToggle={handleHandRaiseToggle}
      floatingReactions={floatingReactions}
      onSendReaction={handleSendReaction}
      qaOpen={qaOpen}
      setQaOpen={setQaOpen}
      questions={questions}
      setQuestions={setQuestions}
      sessionInfo={sessionInfo}
      session={session}
    />
  );
}
