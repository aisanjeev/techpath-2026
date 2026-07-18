'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Users, Play, AlertTriangle, Radio } from 'lucide-react';
import toast from 'react-hot-toast';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { PageLoader } from '@/components/ui/Spinner';
import { trainerService } from '@/services/trainer.service';
import type {
  TrainerBatchSummary,
  TrainingModule,
  TrainingSession,
  TrainingStudent,
} from '@/types/training';

export default function TrainerBatchPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const batchId = Number(id);
  const router = useRouter();

  const [batch, setBatch] = useState<TrainerBatchSummary | null>(null);
  const [modules, setModules] = useState<TrainingModule[]>([]);
  const [students, setStudents] = useState<TrainingStudent[]>([]);
  const [sessions, setSessions] = useState<TrainingSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState<number | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [b, m, s, sess] = await Promise.all([
        trainerService.getBatch(batchId),
        trainerService.getBatchModules(batchId),
        trainerService.getBatchStudents(batchId),
        trainerService.getBatchSessions(batchId),
      ]);
      setBatch(b);
      setModules(m);
      setStudents(s);
      setSessions(sess);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load the batch');
      router.push('/trainer');
    } finally {
      setLoading(false);
    }
  }, [batchId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  /** Create a session for this module and go live in one step. */
  const presentModule = async (module: TrainingModule) => {
    setStarting(module.id);
    try {
      const existing = sessions.find(
        (s) => s.module_id === module.id && s.status !== 'ended'
      );
      const session =
        existing ??
        (await trainerService.createSession({
          batch_id: batchId,
          module_id: module.id,
          title: module.title,
        }));

      const live = await trainerService.startSession(session.id, module.id);
      toast.success('Session is live');
      router.push(`/trainer/sessions/${live.id}`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not start the session');
    } finally {
      setStarting(null);
    }
  };

  if (loading || !batch) return <PageLoader />;

  const liveSession = sessions.find((s) => s.status === 'live');

  return (
    <div>
      <Link
        href="/trainer"
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back
      </Link>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{batch.name}</h1>
          <p className="mt-1 text-sm text-gray-500">
            {batch.code} · {students.length} students · {batch.mode}
            {batch.location ? ` · ${batch.location}` : ''}
          </p>
        </div>
        <Badge variant={batch.status === 'running' ? 'success' : 'info'}>{batch.status}</Badge>
      </div>

      {liveSession && (
        <Card className="mb-6 border-teal-500 bg-teal-50/50 p-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Radio className="h-4 w-4 text-teal-600" />
              <div>
                <p className="text-sm font-medium text-teal-900">
                  A session is live: {liveSession.module_title ?? liveSession.title}
                </p>
                <p className="text-xs text-teal-700">
                  Join code <span className="font-mono font-bold">{liveSession.join_code}</span>
                </p>
              </div>
            </div>
            <Link href={`/trainer/sessions/${liveSession.id}`}>
              <Button>Resume</Button>
            </Link>
          </div>
        </Card>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <h2 className="mb-3 text-sm font-semibold text-gray-900">Modules</h2>

          {!batch.program_id ? (
            <Card className="p-10 text-center">
              <AlertTriangle className="mx-auto h-8 w-8 text-amber-400" />
              <p className="mt-3 text-sm font-medium text-gray-900">
                No training program linked
              </p>
              <p className="mx-auto mt-1 max-w-sm text-sm text-gray-500">
                An admin needs to link this batch to a training program before there is
                anything to present.
              </p>
            </Card>
          ) : modules.length === 0 ? (
            <Card className="p-10 text-center">
              <p className="text-sm font-medium text-gray-900">
                {batch.program_title} has no modules yet
              </p>
              <p className="mt-1 text-sm text-gray-500">
                An admin needs to add modules to this program.
              </p>
            </Card>
          ) : (
            <div className="space-y-2">
              {modules.map((module, index) => (
                <Card key={module.id} className="flex items-center gap-4 p-4">
                  <span className="w-6 text-sm font-semibold text-gray-400">{index + 1}</span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-medium text-gray-900">{module.title}</p>
                    <p className="text-xs text-gray-500">
                      {module.asset_count} asset{module.asset_count === 1 ? '' : 's'}
                      {module.estimated_minutes ? ` · ${module.estimated_minutes} min` : ''}
                    </p>
                  </div>
                  <Button
                    onClick={() => presentModule(module)}
                    disabled={starting !== null || module.asset_count === 0}
                    title={
                      module.asset_count === 0
                        ? 'This module has no content to present'
                        : undefined
                    }
                  >
                    <Play className="mr-1 h-4 w-4" />
                    {starting === module.id ? 'Starting…' : 'Present'}
                  </Button>
                </Card>
              ))}
            </div>
          )}
        </div>

        <div>
          <Card className="p-6">
            <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold text-gray-900">
              <Users className="h-4 w-4 text-gray-400" />
              Roster ({students.length})
            </h2>
            {students.length === 0 ? (
              <p className="text-sm text-gray-500">No students on this batch yet.</p>
            ) : (
              <ul className="space-y-2">
                {students.map((s) => (
                  <li key={s.id} className="flex items-center justify-between gap-2">
                    <div className="min-w-0">
                      <p className="truncate text-sm text-gray-900">{s.name}</p>
                      <p className="truncate text-xs text-gray-400">{s.roll_no ?? s.email}</p>
                    </div>
                    {s.status !== 'active' && (
                      <Badge variant={s.status === 'dropped' ? 'error' : 'warning'}>
                        {s.status}
                      </Badge>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
