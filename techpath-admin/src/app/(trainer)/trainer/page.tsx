'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import {
  CalendarDays,
  Users,
  MapPin,
  Radio,
  ChevronRight,
  Presentation,
  AlertTriangle,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { PageLoader } from '@/components/ui/Spinner';
import { trainerService } from '@/services/trainer.service';
import { useAuthStore } from '@/store/auth.store';
import type { TrainerBatchSummary, TrainingSession } from '@/types/training';

function formatTime(iso?: string | null): string {
  if (!iso) return '';
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function TrainerHomePage() {
  const { user } = useAuthStore();
  const [batches, setBatches] = useState<TrainerBatchSummary[]>([]);
  const [sessions, setSessions] = useState<TrainingSession[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [b, s] = await Promise.all([
        trainerService.myBatches(),
        trainerService.sessionsToday(),
      ]);
      setBatches(b);
      setSessions(s);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load your batches');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  if (loading) return <PageLoader />;

  const active = batches.filter((b) => b.status === 'running' || b.status === 'upcoming');

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Hello{user?.name ? `, ${user.name.split(' ')[0]}` : ''}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          {sessions.length > 0
            ? `You have ${sessions.length} session${sessions.length === 1 ? '' : 's'} today.`
            : 'Nothing scheduled today.'}
        </p>
      </div>

      {/* Today comes first — it's the reason a trainer opens this page. */}
      {sessions.length > 0 && (
        <section>
          <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold text-gray-900">
            <CalendarDays className="h-4 w-4 text-gray-400" />
            Today
          </h2>
          <div className="space-y-2">
            {sessions.map((session) => (
              <Card
                key={session.id}
                className={
                  session.status === 'live'
                    ? 'border-teal-500 bg-teal-50/50 p-4'
                    : 'p-4'
                }
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="truncate font-medium text-gray-900">
                        {session.title || session.module_title || 'Untitled session'}
                      </p>
                      {session.status === 'live' && (
                        <Badge variant="success">
                          <Radio className="mr-1 inline h-3 w-3" />
                          Live
                        </Badge>
                      )}
                    </div>
                    <p className="mt-0.5 text-xs text-gray-500">
                      {session.batch_name}
                      {session.scheduled_start && ` · ${formatTime(session.scheduled_start)}`}
                      {session.module_title && ` · ${session.module_title}`}
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    {session.status === 'live' && session.join_code && (
                      <div className="text-right">
                        <p className="text-[10px] uppercase tracking-wide text-gray-500">
                          Join code
                        </p>
                        <p className="font-mono text-lg font-bold tracking-widest text-teal-700">
                          {session.join_code}
                        </p>
                      </div>
                    )}
                    <Link href={`/trainer/sessions/${session.id}`}>
                      <Button variant={session.status === 'live' ? 'default' : 'outline'}>
                        {session.status === 'live' ? 'Resume' : 'Open'}
                        <ChevronRight className="ml-1 h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold text-gray-900">
          <Users className="h-4 w-4 text-gray-400" />
          My batches
        </h2>

        {batches.length === 0 ? (
          <Card className="p-12 text-center">
            <Presentation className="mx-auto h-10 w-10 text-gray-300" />
            <p className="mt-3 text-sm font-medium text-gray-900">No batches assigned</p>
            <p className="mx-auto mt-1 max-w-md text-sm text-gray-500">
              Batches are assigned in the student system using your email address
              {user?.email ? ` (${user.email})` : ''}. If you expect to see something here,
              ask an admin to check that address matches.
            </p>
          </Card>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {(active.length > 0 ? active : batches).map((batch) => (
              <Link key={batch.id} href={`/trainer/batches/${batch.id}`}>
                <Card className="h-full p-5 transition-colors hover:border-teal-400">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate font-medium text-gray-900">{batch.name}</p>
                      <p className="text-xs text-gray-500">{batch.code}</p>
                    </div>
                    <Badge variant={batch.status === 'running' ? 'success' : 'info'}>
                      {batch.status}
                    </Badge>
                  </div>

                  <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <Users className="h-3.5 w-3.5" />
                      {batch.student_count} students
                    </span>
                    {batch.location && (
                      <span className="flex items-center gap-1">
                        <MapPin className="h-3.5 w-3.5" />
                        {batch.location}
                      </span>
                    )}
                    <span className="capitalize">{batch.mode}</span>
                  </div>

                  {/* Without a linked programme there is nothing to teach from, and
                      that's an admin fix — so say so plainly rather than showing an
                      empty module list later. */}
                  {batch.program_id ? (
                    <p className="mt-3 text-xs text-gray-600">
                      {batch.program_title} · {batch.module_count} module
                      {batch.module_count === 1 ? '' : 's'}
                    </p>
                  ) : (
                    <p className="mt-3 flex items-center gap-1 text-xs text-amber-600">
                      <AlertTriangle className="h-3.5 w-3.5" />
                      No training program linked yet
                    </p>
                  )}
                </Card>
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
