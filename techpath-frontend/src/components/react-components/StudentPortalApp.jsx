import { useCallback, useEffect, useRef, useState } from 'react';
import { GoogleAuthProvider, onAuthStateChanged, signInWithPopup } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import {
  loginToPortal,
  getMySessions,
  getSessionMaterials,
} from '@/services/studentPortalService';
import ClassroomAssetView from './ClassroomAssetView';

/**
 * The materials portal — durable, Google-authenticated sign-in for a student who
 * attended a published session to come back later (days/weeks) and view/download
 * what the trainer published. A genuinely different identity system from the live
 * classroom (real Firebase accounts, not a join-code + short-lived token), so this
 * intentionally doesn't touch classroomService.ts / useClassroomSocket.ts — see
 * studentPortalService.ts and types/studentPortal.ts for the other half of that split.
 *
 * Structured the same way as ClassroomApp.jsx: one small stage machine, not a router.
 *   loading -> signed-out -> not-on-roster -> list -> materials
 * `?session=<id>` is mirrored into the URL via history.pushState purely so back/
 * forward/refresh work while viewing one session's materials — it's not a real router.
 */

const SESSION_QUERY_PARAM = 'session';
const PAGE_QUERY_PARAM = 'page';

function getSessionIdFromUrl() {
  const raw = new URLSearchParams(window.location.search).get(SESSION_QUERY_PARAM);
  const id = raw ? Number(raw) : NaN;
  return Number.isFinite(id) ? id : null;
}

function getPageFromUrl() {
  const raw = new URLSearchParams(window.location.search).get(PAGE_QUERY_PARAM);
  const page = raw ? Number(raw) : 0;
  return Number.isFinite(page) && page >= 0 ? page : 0;
}

function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return d.toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
}

function formatRelativeTime(iso) {
  if (!iso) return '';
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return '';
  const diffMin = Math.round((Date.now() - then) / 60000);
  if (diffMin < 1) return 'just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.round(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.round(diffHr / 24);
  if (diffDay < 30) return `${diffDay}d ago`;
  const diffMonth = Math.round(diffDay / 30);
  if (diffMonth < 12) return `${diffMonth}mo ago`;
  return `${Math.round(diffMonth / 12)}y ago`;
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

function GoogleIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M17.64 9.2c0-.64-.06-1.25-.16-1.84H9v3.48h4.84a4.14 4.14 0 0 1-1.8 2.72v2.26h2.9c1.7-1.57 2.7-3.88 2.7-6.62z"
      />
      <path
        fill="#34A853"
        d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.9-2.26c-.8.54-1.83.86-3.06.86-2.35 0-4.34-1.59-5.05-3.72H.96v2.33A9 9 0 0 0 9 18z"
      />
      <path
        fill="#FBBC05"
        d="M3.95 10.7A5.4 5.4 0 0 1 3.67 9c0-.59.1-1.17.28-1.7V4.97H.96A9 9 0 0 0 0 9c0 1.45.35 2.83.96 4.03l2.99-2.33z"
      />
      <path
        fill="#EA4335"
        d="M9 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.58C13.46.89 11.43 0 9 0A9 9 0 0 0 .96 4.97l2.99 2.33C4.66 5.17 6.65 3.58 9 3.58z"
      />
    </svg>
  );
}

function SignedOutScreen({ onSignIn, signingIn, error }) {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 text-center shadow-2xl backdrop-blur">
        <h1 className="font-heading text-2xl font-bold text-white">My Learning</h1>
        <p className="mx-auto mt-2 max-w-xs text-sm text-slate-400">
          Sign in with the Google account you used when you attended class to view and
          download your session materials.
        </p>
        <button
          onClick={onSignIn}
          disabled={signingIn}
          className="mt-8 flex w-full items-center justify-center gap-3 rounded-xl border border-slate-700 bg-white py-3.5 font-medium text-slate-900 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {signingIn ? (
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-400 border-t-slate-900" />
          ) : (
            <GoogleIcon />
          )}
          {signingIn ? 'Signing in…' : 'Sign in with Google'}
        </button>
        {error && <p className="mt-4 text-sm text-red-400">{error}</p>}
      </div>
      <p className="mt-6 text-center text-xs text-slate-600">
        <a href="/" className="transition hover:text-slate-400">
          techpath.biz
        </a>
      </p>
    </Shell>
  );
}

function NotOnRosterScreen({ message, onSignOut }) {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 text-center shadow-2xl backdrop-blur">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-amber-500/10 text-2xl">
          ⚠️
        </div>
        <h1 className="font-heading text-xl font-bold text-white">Couldn't sign you in</h1>
        <p className="mt-2 text-sm text-slate-400">
          {message || "This Google account isn't linked to any TechPath training roster."}
        </p>
        <p className="mt-3 text-sm text-slate-400">
          If you attended TechPath training under a different email, sign out and try
          that Google account instead.
        </p>
        <button
          onClick={onSignOut}
          className="mt-6 inline-block rounded-xl bg-primary-500 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600"
        >
          Sign out &amp; try another account
        </button>
      </div>
    </Shell>
  );
}

function PortalHeader({ title, subtitle, onBack, onSignOut }) {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-3 px-4 py-3">
        <div className="flex min-w-0 items-center gap-2">
          {onBack && (
            <button
              onClick={onBack}
              className="flex shrink-0 items-center gap-1 rounded-lg px-2 py-1.5 text-xs text-slate-500 transition hover:bg-slate-800 hover:text-slate-300"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span className="hidden sm:inline">Back to my sessions</span>
            </button>
          )}
          <div className="min-w-0">
            <p className="truncate font-heading text-sm font-semibold text-white">{title}</p>
            {subtitle && <p className="truncate text-xs text-slate-500">{subtitle}</p>}
          </div>
        </div>
        <button
          onClick={onSignOut}
          className="shrink-0 rounded-lg px-2.5 py-1.5 text-xs text-slate-500 transition hover:bg-slate-800 hover:text-slate-300"
        >
          Sign out
        </button>
      </div>
    </header>
  );
}

function SessionCard({ session, onOpen }) {
  const heading = session.title || session.module_title || 'Session materials';
  const showModuleLine = session.module_title && session.title;
  return (
    <button
      onClick={onOpen}
      className="group flex w-full flex-col items-start rounded-2xl border border-slate-800 bg-slate-900/60 p-5 text-left transition hover:border-primary-500/50 hover:bg-slate-900"
    >
      <p className="text-xs uppercase tracking-wide text-primary-400">{session.batch_name}</p>
      <h3 className="mt-1 font-heading text-lg font-semibold text-white group-hover:text-primary-300">
        {heading}
      </h3>
      {showModuleLine && <p className="mt-0.5 text-sm text-slate-400">{session.module_title}</p>}
      <div className="mt-4 flex w-full items-center justify-between text-xs text-slate-500">
        <span>{formatDate(session.session_date)}</span>
        <span>Published {formatRelativeTime(session.published_at)}</span>
      </div>
    </button>
  );
}

function SessionListScreen({ profile, sessions, loading, error, onOpenSession, onSignOut, onRetry }) {
  return (
    <div className="min-h-screen bg-slate-950">
      <PortalHeader
        title="My Learning"
        subtitle={profile?.display_name ? `Signed in as ${profile.display_name}` : undefined}
        onSignOut={onSignOut}
      />
      <main className="mx-auto max-w-5xl px-4 py-10">
        {loading ? (
          <div className="flex justify-center py-24">
            <span className="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-primary-500" />
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 py-24 text-center">
            <p className="font-medium text-slate-300">Couldn't load your sessions</p>
            <p className="mt-1 text-sm text-slate-500">{error}</p>
            <button
              onClick={onRetry}
              className="mt-4 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600"
            >
              Try again
            </button>
          </div>
        ) : sessions.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 py-24 text-center">
            <div className="mb-3 text-3xl">📭</div>
            <p className="font-medium text-slate-300">No materials yet</p>
            <p className="mx-auto mt-1 max-w-sm text-sm text-slate-500">
              Once you've attended a session and your trainer publishes the materials,
              they'll show up here.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {sessions.map((session) => (
              <SessionCard
                key={session.session_id}
                session={session}
                onOpen={() => onOpenSession(session.session_id)}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

/** The session's recorded replay, if it had live audio/video. Matches spec.md's edge
 *  case for a still-processing replay — a clear waiting state, never an error. */
function RecordingCard({ recording }) {
  if (recording.status === 'ready' && recording.watch_url) {
    return (
      <a
        href={recording.watch_url}
        target="_blank"
        rel="noopener noreferrer"
        className="mb-6 flex items-center gap-3 rounded-2xl border border-primary-500/30 bg-primary-500/10 p-4 transition hover:bg-primary-500/15"
      >
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-500/20 text-lg">
          ▶️
        </div>
        <div className="min-w-0">
          <p className="font-medium text-white">Watch the class recording</p>
          <p className="text-xs text-slate-400">Opens the replay in a new tab</p>
        </div>
      </a>
    );
  }

  if (recording.status === 'failed') {
    return null; // Nothing a student can act on — quietly omit rather than alarm them.
  }

  return (
    <div className="mb-6 flex items-center gap-3 rounded-2xl border border-dashed border-slate-800 bg-slate-900/40 p-4">
      <span className="h-5 w-5 shrink-0 animate-spin rounded-full border-2 border-slate-700 border-t-primary-500" />
      <div>
        <p className="font-medium text-slate-300">Class recording is processing</p>
        <p className="text-xs text-slate-500">Check back soon — this usually doesn't take long.</p>
      </div>
    </div>
  );
}

function MaterialsScreen({ materials, currentPage, onPageChange, loading, notFound, onBack, onSignOut }) {
  return (
    <div className="min-h-screen bg-slate-950">
      <PortalHeader
        title={materials?.title || materials?.module_title || 'Session materials'}
        subtitle={materials?.batch_name}
        onBack={onBack}
        onSignOut={onSignOut}
      />
      <main className="mx-auto max-w-5xl px-4 py-8 pb-24">
        {loading ? (
          <div className="flex justify-center py-24">
            <span className="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-primary-500" />
          </div>
        ) : notFound ? (
          <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 py-24 text-center">
            <div className="mb-3 text-3xl">🔍</div>
            <p className="font-medium text-slate-300">Not found</p>
            <p className="mx-auto mt-1 max-w-sm text-sm text-slate-500">
              This session's materials aren't available — the link may be out of date.
            </p>
            <button
              onClick={onBack}
              className="mt-4 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600"
            >
              Back to my sessions
            </button>
          </div>
        ) : (
          <>
            <div className="mb-6 flex flex-wrap items-center justify-between gap-2">
              <div>
                <p className="text-xs uppercase tracking-wide text-primary-400">{materials.batch_name}</p>
                <h2 className="font-heading text-xl font-bold text-white">
                  {materials.title || materials.module_title || 'Session materials'}
                </h2>
              </div>
              <p className="text-xs text-slate-500">
                Published {formatDate(materials.published_at)} · {formatRelativeTime(materials.published_at)}
              </p>
            </div>
            {materials.recording && <RecordingCard recording={materials.recording} />}
            {materials.assets.length === 0 ? (
              <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 py-24 text-center">
                <p className="font-medium text-slate-300">Nothing published yet</p>
                <p className="mt-1 text-sm text-slate-500">
                  Your trainer hasn't added materials to this session yet.
                </p>
              </div>
            ) : (
              <div className="space-y-8">
                {materials.assets[currentPage] && (
                  <div key={materials.assets[currentPage].id}>
                    <h3 className="mb-3 font-heading text-base font-semibold text-white">
                      {materials.assets[currentPage].title}
                    </h3>
                    <ClassroomAssetView asset={materials.assets[currentPage]} />
                  </div>
                )}
                
                {materials.assets.length > 1 && (
                  <div className="mt-8 flex items-center justify-between border-t border-slate-800 pt-6">
                    <button
                      onClick={() => onPageChange(currentPage - 1)}
                      disabled={currentPage === 0}
                      className="flex items-center gap-2 rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:opacity-50 disabled:hover:bg-slate-800"
                    >
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                      </svg>
                      Previous
                    </button>
                    <span className="text-sm text-slate-400">
                      Page {currentPage + 1} of {materials.assets.length}
                    </span>
                    <button
                      onClick={() => onPageChange(currentPage + 1)}
                      disabled={currentPage === materials.assets.length - 1}
                      className="flex items-center gap-2 rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:opacity-50 disabled:hover:bg-slate-800"
                    >
                      Next
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default function StudentPortalApp() {
  const [stage, setStage] = useState('loading');
  const [profile, setProfile] = useState(null);
  const [notOnRosterMessage, setNotOnRosterMessage] = useState('');
  const [signingIn, setSigningIn] = useState(false);
  const [signInError, setSignInError] = useState('');

  const [sessions, setSessions] = useState([]);
  const [sessionsLoading, setSessionsLoading] = useState(false);
  const [sessionsError, setSessionsError] = useState('');

  const [materials, setMaterials] = useState(null);
  const [materialsLoading, setMaterialsLoading] = useState(false);
  const [materialsNotFound, setMaterialsNotFound] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);

  // Holds a `?session=<id>` and `?page=<num>` seen on first load until the initial auth check resolves,
  // so a bookmarked/refreshed materials URL can jump straight there. Cleared after
  // first use; later navigation goes through openSession/backToList directly. Populated
  // inside the auth effect below (not here) — this page is `client:load`, so Astro
  // server-renders this component on each request, and `window` doesn't exist there.
  const pendingSessionIdRef = useRef(null);
  const pendingPageRef = useRef(0);

  const loadSessions = useCallback(async () => {
    setSessionsLoading(true);
    setSessionsError('');
    const res = await getMySessions();
    setSessionsLoading(false);
    if (res.success && res.data) {
      setSessions(res.data.sessions);
    } else {
      setSessionsError(res.error || 'Something went wrong loading your sessions.');
    }
  }, []);

  const openSession = useCallback(async (sessionId, { pushState = true, page = 0 } = {}) => {
    setStage('materials');
    setMaterials(null);
    setMaterialsNotFound(false);
    setMaterialsLoading(true);
    setCurrentPage(page);
    if (pushState) {
      window.history.pushState({}, '', `${window.location.pathname}?${SESSION_QUERY_PARAM}=${sessionId}&${PAGE_QUERY_PARAM}=${page}`);
    }
    const res = await getSessionMaterials(sessionId);
    setMaterialsLoading(false);
    if (res.success && res.data) {
      setMaterials(res.data);
    } else {
      // The backend deliberately returns the same 404 whether the session doesn't
      // exist, wasn't attended, or isn't published yet — no need to distinguish here.
      setMaterialsNotFound(true);
    }
  }, []);

  const backToList = useCallback(({ pushState = true } = {}) => {
    setStage('list');
    setMaterials(null);
    setMaterialsNotFound(false);
    if (pushState) {
      window.history.pushState({}, '', window.location.pathname);
    }
  }, []);

  useEffect(() => {
    pendingSessionIdRef.current = getSessionIdFromUrl();
    pendingPageRef.current = getPageFromUrl();
    const unsubscribe = onAuthStateChanged(getFirebaseAuth(), async (user) => {
      if (!user) {
        setProfile(null);
        setSessions([]);
        setMaterials(null);
        setStage('signed-out');
        return;
      }

      const loginRes = await loginToPortal();
      if (!loginRes.success || !loginRes.data) {
        setNotOnRosterMessage(loginRes.error || '');
        setStage('not-on-roster');
        return;
      }

      setProfile(loginRes.data);
      await loadSessions();

      const pendingId = pendingSessionIdRef.current;
      const pendingPage = pendingPageRef.current;
      pendingSessionIdRef.current = null;
      if (pendingId) {
        await openSession(pendingId, { pushState: false, page: pendingPage });
      } else {
        setStage('list');
      }
    });
    return unsubscribe;
  }, [loadSessions, openSession]);

  useEffect(() => {
    const onPopState = () => {
      const id = getSessionIdFromUrl();
      const page = getPageFromUrl();
      if (id) {
        if (stage === 'materials' && materials && materials.session_id === id) {
           setCurrentPage(page);
        } else {
           openSession(id, { pushState: false, page });
        }
      } else {
        backToList({ pushState: false });
      }
    };
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, [openSession, backToList, stage, materials]);

  const handleSignIn = async () => {
    setSigningIn(true);
    setSignInError('');
    try {
      await signInWithPopup(getFirebaseAuth(), new GoogleAuthProvider());
      // onAuthStateChanged (above) picks up the new session and drives the rest of
      // the flow (loginToPortal -> loadSessions) — nothing further to do here.
    } catch (err) {
      const code = err?.code || '';
      if (code === 'auth/popup-closed-by-user' || code === 'auth/cancelled-popup-request') {
        // The student dismissed the picker themselves — not a real error.
      } else if (code === 'auth/unauthorized-domain') {
        setSignInError("This site isn't authorized for Google sign-in yet. Contact support.");
      } else {
        setSignInError('Sign-in failed. Please try again.');
      }
    } finally {
      setSigningIn(false);
    }
  };

  const handleSignOut = async () => {
    await getFirebaseAuth().signOut();
    window.history.pushState({}, '', window.location.pathname);
    // onAuthStateChanged fires from signOut() itself and resets everything to
    // 'signed-out' — no need to duplicate that reset here.
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

  if (stage === 'signed-out') {
    return <SignedOutScreen onSignIn={handleSignIn} signingIn={signingIn} error={signInError} />;
  }

  if (stage === 'not-on-roster') {
    return <NotOnRosterScreen message={notOnRosterMessage} onSignOut={handleSignOut} />;
  }

  if (stage === 'materials') {
    return (
      <MaterialsScreen
        materials={materials}
        currentPage={currentPage}
        onPageChange={(newPage) => {
          setCurrentPage(newPage);
          window.history.pushState({}, '', `${window.location.pathname}?${SESSION_QUERY_PARAM}=${materials.session_id}&${PAGE_QUERY_PARAM}=${newPage}`);
        }}
        loading={materialsLoading}
        notFound={materialsNotFound}
        onBack={() => backToList()}
        onSignOut={handleSignOut}
      />
    );
  }

  return (
    <SessionListScreen
      profile={profile}
      sessions={sessions}
      loading={sessionsLoading}
      error={sessionsError}
      onOpenSession={(id) => openSession(id)}
      onSignOut={handleSignOut}
      onRetry={loadSessions}
    />
  );
}
