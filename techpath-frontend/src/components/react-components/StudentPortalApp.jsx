import { useCallback, useEffect, useRef, useState } from 'react';
import { GoogleAuthProvider, onAuthStateChanged, signInWithPopup } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import {
  loginToPortal,
  getMySessions,
  getSessionMaterials,
  getSessionProgress,
  submitQuizAttempt,
  getSelfPacedCourses,
  getSelfPacedCourse,
  getSelfPacedModuleMaterials,
  getSelfPacedModuleProgress,
  submitSelfPacedQuizAttempt,
  updateSelfPacedModuleBookmark,
} from '@/services/studentPortalService';
import ClassroomAssetView from './ClassroomAssetView';

/*
 * Stage machine:
 *   loading -> signed-out -> not-on-roster -> dashboard -> course | session-materials | module-materials
 *
 * URL params:
 *   ?session=<id>&page=<n>         — session materials (existing)
 *   ?course=<id>                   — course detail
 *   ?course=<id>&module=<id>&page= — module materials (self-paced)
 *   (none)                         — dashboard
 */

const QP = { SESSION: 'session', COURSE: 'course', MODULE: 'module', PAGE: 'page' };

function getUrlParams() {
  const sp = new URLSearchParams(window.location.search);
  const num = (key) => { const v = Number(sp.get(key)); return Number.isFinite(v) && v > 0 ? v : null; };
  const page = Number(sp.get(QP.PAGE));
  return {
    session: num(QP.SESSION),
    course: num(QP.COURSE),
    module: num(QP.MODULE),
    page: Number.isFinite(page) && page >= 0 ? page : 0,
  };
}

function pushUrl(params) {
  const sp = new URLSearchParams();
  if (params.session) { sp.set(QP.SESSION, params.session); if (params.page) sp.set(QP.PAGE, params.page); }
  else if (params.course) {
    sp.set(QP.COURSE, params.course);
    if (params.module) { sp.set(QP.MODULE, params.module); if (params.page) sp.set(QP.PAGE, params.page); }
  }
  const qs = sp.toString();
  window.history.pushState({}, '', qs ? `${window.location.pathname}?${qs}` : window.location.pathname);
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

// ---------------------------------------------------------------------------
// Shared primitives
// ---------------------------------------------------------------------------

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

function Spinner({ className = 'h-8 w-8' }) {
  return <span className={`animate-spin rounded-full border-2 border-slate-700 border-t-primary-500 ${className}`} />;
}

function GoogleIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path fill="#4285F4" d="M17.64 9.2c0-.64-.06-1.25-.16-1.84H9v3.48h4.84a4.14 4.14 0 0 1-1.8 2.72v2.26h2.9c1.7-1.57 2.7-3.88 2.7-6.62z" />
      <path fill="#34A853" d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.9-2.26c-.8.54-1.83.86-3.06.86-2.35 0-4.34-1.59-5.05-3.72H.96v2.33A9 9 0 0 0 9 18z" />
      <path fill="#FBBC05" d="M3.95 10.7A5.4 5.4 0 0 1 3.67 9c0-.59.1-1.17.28-1.7V4.97H.96A9 9 0 0 0 0 9c0 1.45.35 2.83.96 4.03l2.99-2.33z" />
      <path fill="#EA4335" d="M9 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.58C13.46.89 11.43 0 9 0A9 9 0 0 0 .96 4.97l2.99 2.33C4.66 5.17 6.65 3.58 9 3.58z" />
    </svg>
  );
}

function BackButton({ onClick, label = 'Back' }) {
  return (
    <button onClick={onClick} className="flex shrink-0 items-center gap-1 rounded-lg px-2 py-1.5 text-xs text-slate-500 transition hover:bg-slate-800 hover:text-slate-300">
      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
      <span className="hidden sm:inline">{label}</span>
    </button>
  );
}

function PortalHeader({ title, subtitle, onBack, backLabel, onSignOut }) {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
        <div className="flex min-w-0 items-center gap-2">
          {onBack && <BackButton onClick={onBack} label={backLabel} />}
          <div className="min-w-0">
            <p className="truncate font-heading text-sm font-semibold text-white">{title}</p>
            {subtitle && <p className="truncate text-xs text-slate-500">{subtitle}</p>}
          </div>
        </div>
        <button onClick={onSignOut} className="shrink-0 rounded-lg px-2.5 py-1.5 text-xs text-slate-500 transition hover:bg-slate-800 hover:text-slate-300">
          Sign out
        </button>
      </div>
    </header>
  );
}

function EmptyState({ icon, title, message, action }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 py-20 text-center">
      {icon && <div className="mb-3 text-3xl">{icon}</div>}
      <p className="font-medium text-slate-300">{title}</p>
      {message && <p className="mx-auto mt-1 max-w-sm text-sm text-slate-500">{message}</p>}
      {action}
    </div>
  );
}

function SectionHeading({ children }) {
  return <h2 className="mb-4 font-heading text-lg font-bold text-white">{children}</h2>;
}

// ---------------------------------------------------------------------------
// Auth screens
// ---------------------------------------------------------------------------

function SignedOutScreen({ onSignIn, signingIn, error }) {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 text-center shadow-2xl backdrop-blur">
        <h1 className="font-heading text-2xl font-bold text-white">My Learning</h1>
        <p className="mx-auto mt-2 max-w-xs text-sm text-slate-400">
          Sign in with your Google account to access your courses and session materials.
        </p>
        <button
          onClick={onSignIn}
          disabled={signingIn}
          className="mt-8 flex w-full items-center justify-center gap-3 rounded-xl border border-slate-700 bg-white py-3.5 font-medium text-slate-900 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {signingIn ? <Spinner className="h-4 w-4 border-slate-400 border-t-slate-900" /> : <GoogleIcon />}
          {signingIn ? 'Signing in…' : 'Sign in with Google'}
        </button>
        {error && <p className="mt-4 text-sm text-red-400">{error}</p>}
      </div>
      <p className="mt-6 text-center text-xs text-slate-600">
        <a href="/" className="transition hover:text-slate-400">techpath.biz</a>
      </p>
    </Shell>
  );
}

function NotOnRosterScreen({ message, onSignOut }) {
  return (
    <Shell>
      <Brand />
      <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 text-center shadow-2xl backdrop-blur">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-amber-500/10 text-2xl">!</div>
        <h1 className="font-heading text-xl font-bold text-white">Couldn't sign you in</h1>
        <p className="mt-2 text-sm text-slate-400">{message || "This Google account isn't linked to any TechPath training roster."}</p>
        <p className="mt-3 text-sm text-slate-400">If you attended TechPath training under a different email, sign out and try that account instead.</p>
        <button onClick={onSignOut} className="mt-6 inline-block rounded-xl bg-primary-500 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600">
          Sign out &amp; try another account
        </button>
      </div>
    </Shell>
  );
}

// ---------------------------------------------------------------------------
// Dashboard
// ---------------------------------------------------------------------------

function ProgressBar({ value, max, className = '' }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div className={`h-1.5 overflow-hidden rounded-full bg-slate-800 ${className}`}>
      <div className="h-full rounded-full bg-gradient-to-r from-primary-500 to-emerald-400 transition-all duration-500" style={{ width: `${pct}%` }} />
    </div>
  );
}

function CourseCard({ course, onOpen }) {
  const pct = course.module_count > 0 ? Math.round((course.completed_modules / course.module_count) * 100) : 0;
  return (
    <button onClick={onOpen} className="group flex w-full flex-col items-start overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 text-left transition hover:border-primary-500/40 hover:bg-slate-900">
      <div className="flex h-28 w-full items-center justify-center bg-gradient-to-br from-primary-900/40 to-slate-900">
        <svg className="h-10 w-10 text-primary-400/60" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>
      </div>
      <div className="flex w-full flex-1 flex-col p-5">
        <p className="text-[11px] font-medium uppercase tracking-wider text-primary-400">{course.batch_name}</p>
        <h3 className="mt-1 font-heading text-base font-semibold text-white group-hover:text-primary-300">{course.title}</h3>
        {course.summary && <p className="mt-1 line-clamp-2 text-xs text-slate-400">{course.summary}</p>}
        <div className="mt-auto pt-4">
          <div className="mb-1.5 flex items-center justify-between text-[11px] text-slate-500">
            <span>{course.completed_modules} / {course.module_count} modules</span>
            <span>{pct}%</span>
          </div>
          <ProgressBar value={course.completed_modules} max={course.module_count} />
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {course.level && (
            <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-400">{course.level}</span>
          )}
          {course.duration && (
            <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-400">{course.duration}</span>
          )}
          <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-400">{course.total_assets} materials</span>
        </div>
      </div>
    </button>
  );
}

function SessionCard({ session, onOpen }) {
  const heading = session.title || session.module_title || 'Session materials';
  return (
    <button onClick={onOpen} className="group flex w-full flex-col items-start rounded-2xl border border-slate-800 bg-slate-900/60 p-5 text-left transition hover:border-primary-500/40 hover:bg-slate-900">
      <p className="text-[11px] font-medium uppercase tracking-wider text-primary-400">{session.batch_name}</p>
      <h3 className="mt-1 font-heading text-base font-semibold text-white group-hover:text-primary-300">{heading}</h3>
      {session.module_title && session.title && <p className="mt-0.5 text-xs text-slate-400">{session.module_title}</p>}
      <div className="mt-4 flex w-full items-center justify-between text-[11px] text-slate-500">
        <span>{formatDate(session.session_date)}</span>
        <span>Published {formatRelativeTime(session.published_at)}</span>
      </div>
    </button>
  );
}

function DashboardScreen({ profile, courses, sessions, loading, error, onOpenCourse, onOpenSession, onSignOut, onRetry }) {
  const hasCourses = courses.length > 0;
  const hasSessions = sessions.length > 0;
  const hasNothing = !hasCourses && !hasSessions;

  return (
    <div className="min-h-screen bg-slate-950">
      <PortalHeader
        title="My Learning"
        subtitle={profile?.display_name ? `Signed in as ${profile.display_name}` : undefined}
        onSignOut={onSignOut}
      />
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        {loading ? (
          <div className="flex justify-center py-24"><Spinner /></div>
        ) : error ? (
          <EmptyState
            title="Couldn't load your learning"
            message={error}
            action={<button onClick={onRetry} className="mt-4 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600">Try again</button>}
          />
        ) : hasNothing ? (
          <EmptyState
            icon="📚"
            title="Nothing here yet"
            message="Once you're enrolled in a course or your trainer publishes session materials, they'll appear here."
          />
        ) : (
          <div className="space-y-10">
            {hasCourses && (
              <section>
                <SectionHeading>My Courses</SectionHeading>
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                  {courses.map((c) => (
                    <CourseCard key={c.program_id} course={c} onOpen={() => onOpenCourse(c.program_id)} />
                  ))}
                </div>
              </section>
            )}
            {hasSessions && (
              <section>
                <SectionHeading>Class Materials</SectionHeading>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {sessions.map((s) => (
                    <SessionCard key={s.session_id} session={s} onOpen={() => onOpenSession(s.session_id)} />
                  ))}
                </div>
              </section>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Course detail (module list)
// ---------------------------------------------------------------------------

function ModuleCard({ module, index, onOpen }) {
  const statusColor = module.completed
    ? 'border-emerald-500/40 bg-emerald-500/5'
    : module.started
      ? 'border-primary-500/30 bg-primary-500/5'
      : 'border-slate-800 bg-slate-900/60';

  const statusBadge = module.completed
    ? <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400">Completed</span>
    : module.started
      ? <span className="rounded-full bg-primary-500/10 px-2 py-0.5 text-[10px] font-medium text-primary-400">In progress</span>
      : <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-500">Not started</span>;

  return (
    <button onClick={onOpen} className={`group flex w-full items-start gap-4 rounded-xl border p-4 text-left transition hover:border-primary-500/40 ${statusColor}`}>
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-800/80 font-heading text-sm font-bold text-slate-400 group-hover:text-primary-400">
        {String(index + 1).padStart(2, '0')}
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-heading text-sm font-semibold text-white group-hover:text-primary-300">{module.title}</h3>
          {statusBadge}
        </div>
        {module.description && <p className="mt-1 line-clamp-2 text-xs text-slate-400">{module.description}</p>}
        <div className="mt-2 flex flex-wrap gap-3 text-[11px] text-slate-500">
          <span>{module.asset_count} materials</span>
          {module.quiz_count > 0 && <span>{module.quiz_count} {module.quiz_count === 1 ? 'quiz' : 'quizzes'}</span>}
          {module.estimated_minutes && <span>~{module.estimated_minutes} min</span>}
        </div>
      </div>
      <svg className="mt-1 h-5 w-5 shrink-0 text-slate-600 group-hover:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
      </svg>
    </button>
  );
}

function CourseDetailScreen({ course, loading, notFound, onOpenModule, onBack, onSignOut }) {
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950">
        <PortalHeader title="Loading..." onBack={onBack} backLabel="Back" onSignOut={onSignOut} />
        <div className="flex justify-center py-24"><Spinner /></div>
      </div>
    );
  }

  if (notFound || !course) {
    return (
      <div className="min-h-screen bg-slate-950">
        <PortalHeader title="Course" onBack={onBack} backLabel="Back" onSignOut={onSignOut} />
        <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
          <EmptyState icon="🔍" title="Course not found" message="This course may no longer be available." action={<button onClick={onBack} className="mt-4 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600">Back to dashboard</button>} />
        </main>
      </div>
    );
  }

  const completedCount = course.modules.filter((m) => m.completed).length;
  const pct = course.modules.length > 0 ? Math.round((completedCount / course.modules.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-slate-950">
      <PortalHeader title={course.title} subtitle={course.batch_name} onBack={onBack} backLabel="Dashboard" onSignOut={onSignOut} />
      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6">
        {/* Course header */}
        <div className="mb-8 rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <p className="text-[11px] font-medium uppercase tracking-wider text-primary-400">{course.batch_name}</p>
              <h1 className="mt-1 font-heading text-2xl font-bold text-white">{course.title}</h1>
              {course.summary && <p className="mt-2 text-sm text-slate-400">{course.summary}</p>}
              <div className="mt-3 flex flex-wrap gap-2">
                {course.level && <span className="rounded-full bg-slate-800 px-2.5 py-1 text-xs font-medium text-slate-400">{course.level}</span>}
                {course.duration && <span className="rounded-full bg-slate-800 px-2.5 py-1 text-xs font-medium text-slate-400">{course.duration}</span>}
                <span className="rounded-full bg-slate-800 px-2.5 py-1 text-xs font-medium text-slate-400">{course.modules.length} modules</span>
              </div>
            </div>
            <div className="flex flex-col items-end gap-1">
              <span className="font-heading text-3xl font-bold text-white">{pct}%</span>
              <span className="text-xs text-slate-500">complete</span>
            </div>
          </div>
          <ProgressBar value={completedCount} max={course.modules.length} className="mt-5" />
        </div>

        {/* Module list */}
        <SectionHeading>Modules</SectionHeading>
        <div className="space-y-3">
          {course.modules.map((m, i) => (
            <ModuleCard key={m.module_id} module={m} index={i} onOpen={() => onOpenModule(m.module_id, m.last_asset_index)} />
          ))}
        </div>
      </main>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Asset viewer (shared between session materials and self-paced modules)
// ---------------------------------------------------------------------------

function RecordingCard({ recording }) {
  if (recording.status === 'ready' && recording.watch_url) {
    return (
      <a href={recording.watch_url} target="_blank" rel="noopener noreferrer" className="mb-6 flex items-center gap-3 rounded-2xl border border-primary-500/30 bg-primary-500/10 p-4 transition hover:bg-primary-500/15">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-500/20 text-lg">&#9654;&#65039;</div>
        <div className="min-w-0">
          <p className="font-medium text-white">Watch the class recording</p>
          <p className="text-xs text-slate-400">Opens the replay in a new tab</p>
        </div>
      </a>
    );
  }
  if (recording.status === 'failed') return null;
  return (
    <div className="mb-6 flex items-center gap-3 rounded-2xl border border-dashed border-slate-800 bg-slate-900/40 p-4">
      <Spinner className="h-5 w-5" />
      <div>
        <p className="font-medium text-slate-300">Class recording is processing</p>
        <p className="text-xs text-slate-500">Check back soon.</p>
      </div>
    </div>
  );
}

function ProgressTrack({ items, currentPage }) {
  return (
    <div className="flex flex-wrap items-center gap-1.5 border-t border-slate-800 pt-5">
      {items.map((item) => {
        const isCurrent = item.index === currentPage;
        let tone = 'bg-slate-700';
        let label = item.title;
        if (item.locked) { tone = 'bg-slate-800 ring-1 ring-slate-700'; label += ' — locked'; }
        else if (item.isQuiz && item.passed) { tone = 'bg-emerald-500'; label += ' — passed'; }
        else if (item.isQuiz) { tone = 'bg-amber-500'; label += ' — quiz not passed'; }
        return (
          <span key={item.id} title={label} className={`h-1.5 rounded-full transition-all ${tone} ${isCurrent ? 'w-8 ring-2 ring-primary-400/60' : 'w-5'}`} />
        );
      })}
    </div>
  );
}

function AssetPager({ assets, progress, quizResults, onQuizSubmit, currentPage, onPageChange, recording, headerExtra }) {
  const firstLocked = progress?.first_locked_index ?? Infinity;
  const isNextBlocked = currentPage >= firstLocked;
  const progressTrack = (assets || []).map((asset, i) => {
    const item = progress?.items?.find((p) => p.asset_id === asset.id);
    return { id: asset.id, index: i, title: asset.title, isQuiz: item?.is_quiz ?? asset.asset_type === 'quiz', passed: item?.passed ?? null, locked: item?.locked ?? false };
  });

  return (
    <>
      {headerExtra}
      {recording && <RecordingCard recording={recording} />}
      {assets.length === 0 ? (
        <EmptyState title="No materials yet" message="Content hasn't been added to this module yet." />
      ) : (
        <div className="space-y-8">
          {assets[currentPage] && (
            <div key={assets[currentPage].id}>
              <h3 className="mb-3 font-heading text-base font-semibold text-white">{assets[currentPage].title}</h3>
              <ClassroomAssetView
                asset={assets[currentPage]}
                quizResult={quizResults?.[assets[currentPage].id]}
                onQuizSubmit={onQuizSubmit ? (answers) => onQuizSubmit(assets[currentPage].id, answers) : undefined}
              />
            </div>
          )}
          {progressTrack.length > 1 && <ProgressTrack items={progressTrack} currentPage={currentPage} />}
          {isNextBlocked && (
            <p className="rounded-xl border border-amber-800/60 bg-amber-950/30 px-4 py-3 text-sm text-amber-200">
              Pass the quiz above to continue. You can retake it as many times as you need.
            </p>
          )}
          {assets.length > 1 && (
            <div className="mt-8 flex items-center justify-between border-t border-slate-800 pt-6">
              <button onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 0} className="flex items-center gap-2 rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:opacity-50">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
                Previous
              </button>
              <span className="text-sm text-slate-400">{currentPage + 1} / {assets.length}</span>
              <button
                onClick={() => onPageChange(currentPage + 1)}
                disabled={currentPage === assets.length - 1 || isNextBlocked}
                title={isNextBlocked ? 'Pass the quiz to continue' : undefined}
                className="flex items-center gap-2 rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:opacity-50"
              >
                {isNextBlocked ? 'Locked' : 'Next'}
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  {isNextBlocked
                    ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />}
                </svg>
              </button>
            </div>
          )}
        </div>
      )}
    </>
  );
}

// ---------------------------------------------------------------------------
// Main app
// ---------------------------------------------------------------------------

export default function StudentPortalApp() {
  const [stage, setStage] = useState('loading');
  const [profile, setProfile] = useState(null);
  const [notOnRosterMessage, setNotOnRosterMessage] = useState('');
  const [signingIn, setSigningIn] = useState(false);
  const [signInError, setSignInError] = useState('');

  // Dashboard
  const [courses, setCourses] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [dashLoading, setDashLoading] = useState(false);
  const [dashError, setDashError] = useState('');

  // Course detail
  const [courseDetail, setCourseDetail] = useState(null);
  const [courseLoading, setCourseLoading] = useState(false);
  const [courseNotFound, setCourseNotFound] = useState(false);

  // Materials viewer (shared state for both session and self-paced)
  const [materials, setMaterials] = useState(null);
  const [materialsLoading, setMaterialsLoading] = useState(false);
  const [materialsNotFound, setMaterialsNotFound] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);
  const [progress, setProgress] = useState(null);
  const [quizResults, setQuizResults] = useState({});

  // Context for materials: which session or which course/module
  const [materialsContext, setMaterialsContext] = useState(null);

  const pendingParamsRef = useRef(null);

  // ---------------------------------------------------------------------------
  // Data loading
  // ---------------------------------------------------------------------------

  const loadDashboard = useCallback(async () => {
    setDashLoading(true);
    setDashError('');
    const [sessionsRes, coursesRes] = await Promise.all([
      getMySessions(),
      getSelfPacedCourses(),
    ]);
    setDashLoading(false);
    if (sessionsRes.success && sessionsRes.data) setSessions(sessionsRes.data.sessions);
    if (coursesRes.success && coursesRes.data) setCourses(coursesRes.data.courses);
    if (!sessionsRes.success && !coursesRes.success) {
      setDashError(sessionsRes.error || coursesRes.error || 'Something went wrong.');
    }
  }, []);

  const openCourse = useCallback(async (programId, { pushState = true } = {}) => {
    setStage('course');
    setCourseDetail(null);
    setCourseNotFound(false);
    setCourseLoading(true);
    if (pushState) pushUrl({ course: programId });
    const res = await getSelfPacedCourse(programId);
    setCourseLoading(false);
    if (res.success && res.data) {
      setCourseDetail(res.data);
    } else {
      setCourseNotFound(true);
    }
  }, []);

  const openModuleMaterials = useCallback(async (programId, moduleId, { pushState = true, page = 0 } = {}) => {
    setStage('module-materials');
    setMaterials(null);
    setMaterialsNotFound(false);
    setMaterialsLoading(true);
    setCurrentPage(page);
    setQuizResults({});
    setMaterialsContext({ type: 'module', programId, moduleId });
    if (pushState) pushUrl({ course: programId, module: moduleId, page });
    const [matRes, progRes] = await Promise.all([
      getSelfPacedModuleMaterials(programId, moduleId),
      getSelfPacedModuleProgress(programId, moduleId),
    ]);
    setMaterialsLoading(false);
    if (matRes.success && matRes.data) {
      setMaterials(matRes.data);
      const loadedProgress = progRes.success ? progRes.data : null;
      setProgress(loadedProgress);
      if (loadedProgress && page > loadedProgress.first_locked_index) {
        setCurrentPage(loadedProgress.first_locked_index);
      }
    } else {
      setMaterialsNotFound(true);
    }
  }, []);

  const openSessionMaterials = useCallback(async (sessionId, { pushState = true, page = 0 } = {}) => {
    setStage('session-materials');
    setMaterials(null);
    setMaterialsNotFound(false);
    setMaterialsLoading(true);
    setCurrentPage(page);
    setQuizResults({});
    setMaterialsContext({ type: 'session', sessionId });
    if (pushState) pushUrl({ session: sessionId, page });
    const [res, progressRes] = await Promise.all([
      getSessionMaterials(sessionId),
      getSessionProgress(sessionId),
    ]);
    setMaterialsLoading(false);
    if (res.success && res.data) {
      setMaterials(res.data);
      const loadedProgress = progressRes.success ? progressRes.data : null;
      setProgress(loadedProgress);
      if (loadedProgress && page > loadedProgress.first_locked_index) {
        setCurrentPage(loadedProgress.first_locked_index);
      }
    } else {
      setMaterialsNotFound(true);
    }
  }, []);

  const handleQuizSubmit = useCallback(async (assetId, answers) => {
    if (!materialsContext) return { success: false, error: 'No context' };
    let res;
    if (materialsContext.type === 'session') {
      res = await submitQuizAttempt(materialsContext.sessionId, assetId, answers);
    } else {
      res = await submitSelfPacedQuizAttempt(materialsContext.programId, materialsContext.moduleId, assetId, answers);
    }
    if (!res.success || !res.data) {
      return { success: false, error: res.error || 'Could not submit your answers.' };
    }
    setQuizResults((prev) => ({ ...prev, [assetId]: res.data }));
    if (res.data.passed) {
      let progressRes;
      if (materialsContext.type === 'session') {
        progressRes = await getSessionProgress(materialsContext.sessionId);
      } else {
        progressRes = await getSelfPacedModuleProgress(materialsContext.programId, materialsContext.moduleId);
      }
      if (progressRes.success) setProgress(progressRes.data);
    }
    return res.data;
  }, [materialsContext]);

  const backToDashboard = useCallback(({ pushState = true } = {}) => {
    setStage('dashboard');
    setMaterials(null);
    setMaterialsNotFound(false);
    setCourseDetail(null);
    setCourseNotFound(false);
    setMaterialsContext(null);
    if (pushState) pushUrl({});
  }, []);

  const backToCourse = useCallback(({ pushState = true } = {}) => {
    if (materialsContext?.type === 'module' && materialsContext.programId) {
      openCourse(materialsContext.programId, { pushState });
    } else {
      backToDashboard({ pushState });
    }
  }, [materialsContext, openCourse, backToDashboard]);

  // ---------------------------------------------------------------------------
  // Auth + initial routing
  // ---------------------------------------------------------------------------

  useEffect(() => {
    pendingParamsRef.current = getUrlParams();
    const unsubscribe = onAuthStateChanged(getFirebaseAuth(), async (user) => {
      if (!user) {
        setProfile(null);
        setSessions([]);
        setCourses([]);
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
      await loadDashboard();

      const p = pendingParamsRef.current;
      pendingParamsRef.current = null;
      if (p?.session) {
        await openSessionMaterials(p.session, { pushState: false, page: p.page });
      } else if (p?.course && p?.module) {
        await openModuleMaterials(p.course, p.module, { pushState: false, page: p.page });
      } else if (p?.course) {
        await openCourse(p.course, { pushState: false });
      } else {
        setStage('dashboard');
      }
    });
    return unsubscribe;
  }, [loadDashboard, openSessionMaterials, openModuleMaterials, openCourse]);

  // Browser back/forward
  useEffect(() => {
    const onPopState = () => {
      const p = getUrlParams();
      if (p.session) {
        openSessionMaterials(p.session, { pushState: false, page: p.page });
      } else if (p.course && p.module) {
        openModuleMaterials(p.course, p.module, { pushState: false, page: p.page });
      } else if (p.course) {
        openCourse(p.course, { pushState: false });
      } else {
        backToDashboard({ pushState: false });
      }
    };
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, [openSessionMaterials, openModuleMaterials, openCourse, backToDashboard]);

  // ---------------------------------------------------------------------------
  // Auth handlers
  // ---------------------------------------------------------------------------

  const handleSignIn = async () => {
    setSigningIn(true);
    setSignInError('');
    try {
      await signInWithPopup(getFirebaseAuth(), new GoogleAuthProvider());
    } catch (err) {
      const code = err?.code || '';
      if (code === 'auth/popup-closed-by-user' || code === 'auth/cancelled-popup-request') { /* user dismissed */ }
      else if (code === 'auth/unauthorized-domain') setSignInError("This site isn't authorized for Google sign-in yet. Contact support.");
      else setSignInError('Sign-in failed. Please try again.');
    } finally {
      setSigningIn(false);
    }
  };

  const handleSignOut = async () => {
    await getFirebaseAuth().signOut();
    pushUrl({});
  };

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------

  if (stage === 'loading') {
    return <Shell><div className="flex justify-center"><Spinner /></div></Shell>;
  }
  if (stage === 'signed-out') {
    return <SignedOutScreen onSignIn={handleSignIn} signingIn={signingIn} error={signInError} />;
  }
  if (stage === 'not-on-roster') {
    return <NotOnRosterScreen message={notOnRosterMessage} onSignOut={handleSignOut} />;
  }

  if (stage === 'course') {
    return (
      <CourseDetailScreen
        course={courseDetail}
        loading={courseLoading}
        notFound={courseNotFound}
        onOpenModule={(moduleId, lastIndex) =>
          openModuleMaterials(courseDetail?.program_id, moduleId, { page: lastIndex || 0 })
        }
        onBack={() => backToDashboard()}
        onSignOut={handleSignOut}
      />
    );
  }

  if (stage === 'module-materials') {
    return (
      <div className="min-h-screen bg-slate-950">
        <PortalHeader
          title={materials?.module_title || 'Module'}
          subtitle={materials?.program_title}
          onBack={() => backToCourse()}
          backLabel="Back to course"
          onSignOut={handleSignOut}
        />
        <main className="mx-auto max-w-5xl px-4 py-8 pb-24 sm:px-6">
          {materialsLoading ? (
            <div className="flex justify-center py-24"><Spinner /></div>
          ) : materialsNotFound ? (
            <EmptyState
              icon="🔍"
              title="Module not found"
              action={<button onClick={() => backToCourse()} className="mt-4 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600">Back to course</button>}
            />
          ) : (
            <AssetPager
              assets={materials?.assets || []}
              progress={progress}
              quizResults={quizResults}
              onQuizSubmit={handleQuizSubmit}
              currentPage={currentPage}
              onPageChange={(p) => {
                setCurrentPage(p);
                if (materialsContext) {
                  pushUrl({ course: materialsContext.programId, module: materialsContext.moduleId, page: p });
                  updateSelfPacedModuleBookmark(materialsContext.programId, materialsContext.moduleId, p).then(res => {
                    if (res.success) {
                      // refresh progress to update the progress bar on Dashboard and Course Detail
                      getSelfPacedModuleProgress(materialsContext.programId, materialsContext.moduleId).then(progRes => {
                        if (progRes.success) setProgress(progRes.data);
                      });
                    }
                  });
                }
              }}
              headerExtra={
                <div className="mb-6">
                  <p className="text-[11px] font-medium uppercase tracking-wider text-primary-400">{materials?.batch_name}</p>
                  <h2 className="mt-1 font-heading text-xl font-bold text-white">{materials?.module_title}</h2>
                </div>
              }
            />
          )}
        </main>
      </div>
    );
  }

  if (stage === 'session-materials') {
    return (
      <div className="min-h-screen bg-slate-950">
        <PortalHeader
          title={materials?.title || materials?.module_title || 'Session materials'}
          subtitle={materials?.batch_name}
          onBack={() => backToDashboard()}
          backLabel="Dashboard"
          onSignOut={handleSignOut}
        />
        <main className="mx-auto max-w-5xl px-4 py-8 pb-24 sm:px-6">
          {materialsLoading ? (
            <div className="flex justify-center py-24"><Spinner /></div>
          ) : materialsNotFound ? (
            <EmptyState
              icon="🔍"
              title="Not found"
              message="This session's materials aren't available — the link may be out of date."
              action={<button onClick={() => backToDashboard()} className="mt-4 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600">Back to dashboard</button>}
            />
          ) : (
            <AssetPager
              assets={materials?.assets || []}
              progress={progress}
              quizResults={quizResults}
              onQuizSubmit={handleQuizSubmit}
              currentPage={currentPage}
              onPageChange={(p) => {
                setCurrentPage(p);
                if (materialsContext) pushUrl({ session: materialsContext.sessionId, page: p });
              }}
              recording={materials?.recording}
              headerExtra={
                <div className="mb-6 flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <p className="text-[11px] font-medium uppercase tracking-wider text-primary-400">{materials?.batch_name}</p>
                    <h2 className="mt-1 font-heading text-xl font-bold text-white">{materials?.title || materials?.module_title || 'Session materials'}</h2>
                  </div>
                  {materials?.published_at && (
                    <p className="text-xs text-slate-500">Published {formatDate(materials.published_at)} &middot; {formatRelativeTime(materials.published_at)}</p>
                  )}
                </div>
              }
            />
          )}
        </main>
      </div>
    );
  }

  // Default: dashboard
  return (
    <DashboardScreen
      profile={profile}
      courses={courses}
      sessions={sessions}
      loading={dashLoading}
      error={dashError}
      onOpenCourse={(id) => openCourse(id)}
      onOpenSession={(id) => openSessionMaterials(id)}
      onSignOut={handleSignOut}
      onRetry={loadDashboard}
    />
  );
}
