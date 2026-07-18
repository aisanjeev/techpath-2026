'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Users, BarChart3, Activity, CheckCircle2, ListChecks } from 'lucide-react';
import toast from 'react-hot-toast';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { PageLoader } from '@/components/ui/Spinner';
import { trainerService } from '@/services/trainer.service';
import type { TrainingSession } from '@/types/training';
import type {
  AttendanceReportResponse,
  ConfusionTimelineResponse,
  PollHistoryResponse,
  QuizResultsResponse,
  QuizResultSummary,
} from '@/types/classroom';
import { SessionMaterialsModal } from '@/components/SessionMaterialsModal';

function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

/** No charting library — a readable at-a-glance shape of "confusion went up/down"
 *  rendered as a plain filled polyline. No axes/legends/tooltips, just the trend. */
function ConfusionSparkline({ points }: { points: ConfusionTimelineResponse['points'] }) {
  if (points.length === 0) {
    return <p className="text-sm text-gray-500">No confusion data recorded for this session.</p>;
  }

  const width = 600;
  const height = 120;
  const pad = 4;

  const coords = points.map((p, i) => {
    const x =
      points.length === 1 ? width / 2 : (i / (points.length - 1)) * (width - pad * 2) + pad;
    const ratio = Math.min(1, Math.max(0, p.ratio));
    const y = height - pad - ratio * (height - pad * 2);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });

  const areaPath = `M${pad},${height - pad} L${coords.join(' L')} L${width - pad},${height - pad} Z`;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="h-32 w-full" preserveAspectRatio="none">
      <path d={areaPath} fill="rgb(245 158 11 / 0.15)" />
      <polyline points={coords.join(' ')} fill="none" stroke="#f59e0b" strokeWidth={2} />
    </svg>
  );
}

/** One quiz's results: the headline pass rate, who stands where, and which question
 *  the group actually got wrong — that last one is usually what changes what a
 *  trainer does next. */
function QuizResultBlock({ quiz }: { quiz: QuizResultSummary }) {
  const notAttempted = quiz.roster_size - quiz.attempted_count;
  // Sorted worst-first: the students who need attention are the reason to open this.
  const students = [...quiz.students].sort((a, b) => {
    if (a.passed !== b.passed) return a.passed ? 1 : -1;
    if (a.attempt_count === 0 !== (b.attempt_count === 0)) return a.attempt_count === 0 ? -1 : 1;
    return (a.best_score ?? -1) - (b.best_score ?? -1);
  });

  return (
    <div className="rounded-lg border border-gray-200">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-gray-200 bg-gray-50 px-4 py-3">
        <div>
          <p className="text-sm font-medium text-gray-900">{quiz.title}</p>
          <p className="mt-0.5 text-xs text-gray-500">
            {quiz.total_questions} question{quiz.total_questions === 1 ? '' : 's'} ·{' '}
            {Math.round(quiz.pass_mark * 100)}% to pass
          </p>
        </div>
        <div className="flex items-center gap-4 text-xs">
          <span className="font-medium text-green-700">{quiz.passed_count} passed</span>
          <span className="text-amber-700">
            {quiz.attempted_count - quiz.passed_count} attempted, not passed
          </span>
          <span className="text-gray-500">{notAttempted} not attempted</span>
        </div>
      </div>

      {quiz.question_stats.length > 0 && (
        <div className="border-b border-gray-200 px-4 py-3">
          <p className="mb-2 text-xs font-medium uppercase tracking-wide text-gray-500">
            Where the group struggled
          </p>
          <div className="space-y-1.5">
            {quiz.question_stats.map((stat) => {
              const pct =
                stat.attempted_count > 0
                  ? Math.round((stat.correct_count / stat.attempted_count) * 100)
                  : 0;
              return (
                <div key={stat.index} className="flex items-center gap-3 text-xs">
                  <span className="w-6 shrink-0 text-gray-400">Q{stat.index + 1}</span>
                  <span className="min-w-0 flex-1 truncate text-gray-700" title={stat.question}>
                    {stat.question}
                  </span>
                  <div className="h-1.5 w-24 shrink-0 overflow-hidden rounded-full bg-gray-200">
                    <div
                      className={`h-full rounded-full ${
                        pct >= 70 ? 'bg-green-500' : pct >= 40 ? 'bg-amber-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <span className="w-16 shrink-0 text-right text-gray-500">
                    {stat.correct_count}/{stat.attempted_count} right
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="max-h-80 overflow-auto">
        <table className="w-full text-left text-xs">
          <thead className="sticky top-0 bg-white">
            <tr className="border-b border-gray-200 text-gray-500">
              <th className="px-4 py-2 font-medium">Student</th>
              <th className="px-4 py-2 font-medium">Attempts</th>
              <th className="px-4 py-2 font-medium">Best</th>
              <th className="px-4 py-2 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.student_id} className="border-b border-gray-100 last:border-0">
                <td className="px-4 py-2">
                  <span className="text-gray-900">{s.name}</span>
                  {s.is_stale && (
                    <span
                      className="ml-2 rounded bg-gray-100 px-1.5 py-0.5 text-[10px] text-gray-600"
                      title="Graded against an earlier version of this quiz — the score was not recalculated"
                    >
                      earlier version
                    </span>
                  )}
                </td>
                <td className="px-4 py-2 text-gray-600">{s.attempt_count || '—'}</td>
                <td className="px-4 py-2 text-gray-600">
                  {s.best_score != null ? `${s.best_score}/${s.total_questions}` : '—'}
                </td>
                <td className="px-4 py-2">
                  {s.attempt_count === 0 ? (
                    <span className="text-gray-400">Not attempted</span>
                  ) : s.passed ? (
                    <span className="font-medium text-green-700">Passed</span>
                  ) : (
                    <span className="font-medium text-amber-700">Not passed</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function SessionReportPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const sessionId = Number(id);
  const router = useRouter();

  const [session, setSession] = useState<TrainingSession | null>(null);
  const [attendance, setAttendance] = useState<AttendanceReportResponse | null>(null);
  const [pollHistory, setPollHistory] = useState<PollHistoryResponse | null>(null);
  const [timeline, setTimeline] = useState<ConfusionTimelineResponse | null>(null);
  const [quizResults, setQuizResults] = useState<QuizResultsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setSession(await trainerService.getSession(sessionId));
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load the session');
      router.push(`/trainer/sessions/${sessionId}`);
      setLoading(false);
      return;
    }

    // Each report section is fetched independently and degrades on its own — one
    // endpoint having a bad day (or, as observed against the live dev backend, a route
    // that 422s) shouldn't blank out the sections that loaded fine.
    const [attResult, pollResult, confResult, quizResult] = await Promise.allSettled([
      trainerService.getAttendanceReport(sessionId),
      trainerService.getPollHistory(sessionId),
      trainerService.getConfusionTimeline(sessionId),
      trainerService.getQuizResults(sessionId),
    ]);
    setAttendance(attResult.status === 'fulfilled' ? attResult.value : null);
    setPollHistory(pollResult.status === 'fulfilled' ? pollResult.value : null);
    setTimeline(confResult.status === 'fulfilled' ? confResult.value : null);
    setQuizResults(quizResult.status === 'fulfilled' ? quizResult.value : null);
    if (
      attResult.status === 'rejected' ||
      pollResult.status === 'rejected' ||
      confResult.status === 'rejected' ||
      quizResult.status === 'rejected'
    ) {
      toast.error('Some parts of this report could not be loaded');
    }
    setLoading(false);
  }, [sessionId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  if (loading || !session) {
    return <PageLoader />;
  }

  return (
    <div>
      <Link
        href={`/trainer/sessions/${sessionId}`}
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to session
      </Link>

      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {attendance?.session_title || session.title || session.module_title || 'Session report'}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            {session.batch_name}
            {attendance &&
              ` · ${attendance.total_participants} participant${
                attendance.total_participants === 1 ? '' : 's'
              }`}
          </p>
        </div>
        
        {session.module_id && (
          <SessionMaterialsModal moduleId={session.module_id} />
        )}
      </div>

      <div className="space-y-6">
        {/* Attendance */}
        <Card className="p-6">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold text-gray-900">
            <Users className="h-4 w-4 text-teal-600" />
            Attendance
          </h2>
          {!attendance ? (
            <p className="text-sm text-red-500">Could not load attendance data.</p>
          ) : attendance.rows.length === 0 ? (
            <p className="text-sm text-gray-500">No one joined this session.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-gray-200 text-xs uppercase tracking-wide text-gray-500">
                    <th className="py-2 pr-4 font-medium">Participant</th>
                    <th className="py-2 pr-4 font-medium">Joined</th>
                    <th className="py-2 pr-4 font-medium">Duration</th>
                    <th className="py-2 pr-4 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {attendance.rows.map((row) => (
                    <tr key={row.participant_id}>
                      <td className="py-2.5 pr-4">
                        <span className="font-medium text-gray-900">{row.display_name}</span>
                        {row.is_guest && (
                          <Badge variant="default" className="ml-2">
                            Guest
                          </Badge>
                        )}
                      </td>
                      <td className="py-2.5 pr-4 text-gray-600">
                        {formatDateTime(row.first_joined_at)}
                      </td>
                      <td className="py-2.5 pr-4 text-gray-600">{row.duration_minutes} min</td>
                      <td className="py-2.5 pr-4">
                        <Badge variant={row.is_online ? 'success' : 'default'}>
                          {row.is_online ? 'Online' : 'Offline'}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>

        {/* Poll history */}
        <Card className="p-6">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold text-gray-900">
            <BarChart3 className="h-4 w-4 text-teal-600" />
            Poll history
          </h2>
          {!pollHistory ? (
            <p className="text-sm text-red-500">Could not load poll history.</p>
          ) : pollHistory.polls.length === 0 ? (
            <p className="text-sm text-gray-500">No polls were run in this session.</p>
          ) : (
            <div className="space-y-4">
              {pollHistory.polls.map((poll) => (
                <div key={poll.id} className="rounded-lg border border-gray-200 p-4">
                  <div className="mb-3 flex items-start justify-between gap-2">
                    <p className="text-sm font-medium text-gray-900">{poll.question}</p>
                    <Badge variant={poll.status === 'open' ? 'success' : 'default'}>
                      {poll.status}
                    </Badge>
                  </div>
                  <div className="space-y-2">
                    {poll.options.map((opt, i) => {
                      const count = poll.results[i] ?? 0;
                      const pct =
                        poll.total_votes > 0 ? Math.round((count / poll.total_votes) * 100) : 0;
                      const isCorrect = poll.correct_option_index === i;
                      return (
                        <div key={i}>
                          <div className="mb-1 flex items-center justify-between text-xs">
                            <span
                              className={`flex items-center gap-1 ${
                                isCorrect ? 'font-medium text-green-700' : 'text-gray-700'
                              }`}
                            >
                              {opt}
                              {isCorrect && <CheckCircle2 className="h-3.5 w-3.5 text-green-600" />}
                            </span>
                            <span className="text-gray-500">
                              {count} · {pct}%
                            </span>
                          </div>
                          <div className="h-2 w-full overflow-hidden rounded-full bg-gray-100">
                            <div
                              className={`h-full rounded-full ${
                                isCorrect ? 'bg-green-500' : 'bg-teal-500'
                              }`}
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <p className="mt-3 text-xs text-gray-500">
                    {poll.total_votes} vote{poll.total_votes === 1 ? '' : 's'} ·{' '}
                    {formatDateTime(poll.created_at)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Quiz results */}
        {quizResults && quizResults.quizzes.length > 0 && (
          <Card className="p-6">
            <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold text-gray-900">
              <ListChecks className="h-4 w-4 text-teal-600" />
              Quiz results
            </h2>
            <div className="space-y-8">
              {quizResults.quizzes.map((quiz) => (
                <QuizResultBlock key={quiz.asset_id} quiz={quiz} />
              ))}
            </div>
          </Card>
        )}

        {/* Confusion timeline */}
        <Card className="p-6">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold text-gray-900">
            <Activity className="h-4 w-4 text-teal-600" />
            Confusion over time
          </h2>
          {timeline ? (
            <ConfusionSparkline points={timeline.points} />
          ) : (
            <p className="text-sm text-red-500">Could not load the confusion timeline.</p>
          )}
        </Card>
      </div>
    </div>
  );
}
