'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Users, BarChart3, Activity, CheckCircle2 } from 'lucide-react';
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
} from '@/types/classroom';

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

export default function SessionReportPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const sessionId = Number(id);
  const router = useRouter();

  const [session, setSession] = useState<TrainingSession | null>(null);
  const [attendance, setAttendance] = useState<AttendanceReportResponse | null>(null);
  const [pollHistory, setPollHistory] = useState<PollHistoryResponse | null>(null);
  const [timeline, setTimeline] = useState<ConfusionTimelineResponse | null>(null);
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
    const [attResult, pollResult, confResult] = await Promise.allSettled([
      trainerService.getAttendanceReport(sessionId),
      trainerService.getPollHistory(sessionId),
      trainerService.getConfusionTimeline(sessionId),
    ]);
    setAttendance(attResult.status === 'fulfilled' ? attResult.value : null);
    setPollHistory(pollResult.status === 'fulfilled' ? pollResult.value : null);
    setTimeline(confResult.status === 'fulfilled' ? confResult.value : null);
    if (attResult.status === 'rejected' || pollResult.status === 'rejected' || confResult.status === 'rejected') {
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

      <div className="mb-6">
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
