'use client';

import { use, useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Lock, Link2, UserCheck, BookOpen } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { FormField } from '@/components/ui/FormField';
import { PageLoader } from '@/components/ui/Spinner';
import { Switch } from '@/components/ui/Switch';
import { DataTable, type Column } from '@/components/tables/DataTable';
import { trainingRosterService } from '@/services/training-roster.service';
import { trainingService } from '@/services/training.service';
import { usersService } from '@/services/users.service';
import type { AdminUser } from '@/types/api';
import type { TrainingBatch, TrainingProgram, TrainingStudent } from '@/types/training';

export default function BatchDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const batchId = Number(id);

  const [batch, setBatch] = useState<TrainingBatch | null>(null);
  const [students, setStudents] = useState<TrainingStudent[]>([]);
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [trainers, setTrainers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [linking, setLinking] = useState(false);
  const [programId, setProgramId] = useState<string>('');
  const [trainerEmail, setTrainerEmail] = useState<string>('');
  const [isSelfPaced, setIsSelfPaced] = useState(false);
  const [assigningTrainer, setAssigningTrainer] = useState(false);
  const [togglingMode, setTogglingMode] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [b, s, p, t] = await Promise.all([
        trainingRosterService.getBatch(batchId),
        trainingRosterService.getBatchStudents(batchId),
        trainingService.listPrograms({ limit: 100 }),
        usersService.list({ role: 'trainer', limit: 100 }),
      ]);
      setBatch(b);
      setStudents(s);
      setPrograms(p.items);
      setTrainers(t.items);
      setProgramId(b.program_id != null ? String(b.program_id) : '');
      setTrainerEmail(b.trainer_email ?? '');
      setIsSelfPaced(b.is_self_paced ?? false);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load the batch');
    } finally {
      setLoading(false);
    }
  }, [batchId]);

  useEffect(() => {
    void load();
  }, [load]);

  const saveLink = async () => {
    setLinking(true);
    try {
      const updated = await trainingRosterService.linkProgram(
        batchId,
        programId ? Number(programId) : null
      );
      setBatch(updated);
      toast.success(programId ? 'Program linked' : 'Program unlinked');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not link the programme');
    } finally {
      setLinking(false);
    }
  };

  const saveTrainer = async () => {
    setAssigningTrainer(true);
    try {
      const updated = await trainingRosterService.assignTrainer(
        batchId,
        trainerEmail || null
      );
      setBatch(updated);
      toast.success(trainerEmail ? 'Trainer assigned' : 'Trainer unassigned');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not assign trainer');
    } finally {
      setAssigningTrainer(false);
    }
  };

  const toggleSelfPaced = async (val: boolean) => {
    setTogglingMode(true);
    try {
      const updated = await trainingRosterService.setSelfPaced(batchId, val);
      setBatch(updated);
      setIsSelfPaced(updated.is_self_paced);
      toast.success(val ? 'Self-paced mode enabled' : 'Instructor-led mode enabled');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not change mode');
    } finally {
      setTogglingMode(false);
    }
  };

  if (loading || !batch) return <PageLoader />;

  const columns: Column<TrainingStudent>[] = [
    {
      key: 'name',
      header: 'Student',
      render: (s) => (
        <div>
          <p className="font-medium text-gray-900">{s.name}</p>
          <p className="text-xs text-gray-500">{s.roll_no ?? s.external_id}</p>
        </div>
      ),
    },
    { key: 'email', header: 'Email', render: (s) => <span className="text-gray-600">{s.email ?? '—'}</span> },
    { key: 'phone', header: 'Phone', render: (s) => <span className="text-gray-600">{s.phone ?? '—'}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (s) => (
        <Badge variant={s.status === 'active' ? 'success' : s.status === 'dropped' ? 'error' : 'warning'}>
          {s.status ?? '—'}
        </Badge>
      ),
    },
  ];

  return (
    <div>
      <Link
        href="/training/batches"
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to batches
      </Link>

      <PageHeader
        title={batch.name}
        description={batch.code ?? batch.external_id}
        actions={<Badge variant="info">{batch.status ?? 'unknown'}</Badge>}
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <Card className="p-6">
            <h2 className="mb-4 text-sm font-semibold text-gray-900">
              Students ({students.length})
            </h2>
            <DataTable
              columns={columns}
              data={students}
              keyExtractor={(s) => s.id}
              emptyMessage="No students on this batch's roster."
            />
          </Card>
        </div>

        <div className="space-y-6">
          {/* The one thing that is ours to set on a mirrored batch. */}
          <Card className="p-6">
            <div className="mb-1 flex items-center gap-2">
              <Link2 className="h-4 w-4 text-teal-600" />
              <h2 className="text-sm font-semibold text-gray-900">Training program</h2>
            </div>
            <p className="mb-4 text-xs text-gray-500">
              Decides what the trainer can present to this batch. This is ours — syncing
              never overwrites it.
            </p>
            <FormField label="Program">
              <Select value={programId} onChange={(e) => setProgramId(e.target.value)}>
                <option value="">Not linked</option>
                {programs.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.title}
                  </option>
                ))}
              </Select>
            </FormField>
            <Button onClick={saveLink} disabled={linking} className="mt-4 w-full">
              {linking ? 'Saving…' : 'Save link'}
            </Button>
          </Card>

          <Card className="p-6">
            <div className="mb-1 flex items-center gap-2">
              <UserCheck className="h-4 w-4 text-teal-600" />
              <h2 className="text-sm font-semibold text-gray-900">Assigned trainer</h2>
            </div>
            <p className="mb-4 text-xs text-gray-500">
              The trainer whose dashboard shows this batch. Syncing preserves
              this when the external system doesn't provide it.
            </p>
            <FormField label="Trainer">
              <Select value={trainerEmail} onChange={(e) => setTrainerEmail(e.target.value)}>
                <option value="">Not assigned</option>
                {trainers.map((t) => (
                  <option key={t.id} value={t.email}>
                    {t.name} ({t.email})
                  </option>
                ))}
              </Select>
            </FormField>
            <Button onClick={saveTrainer} disabled={assigningTrainer} className="mt-4 w-full">
              {assigningTrainer ? 'Saving…' : 'Save trainer'}
            </Button>
          </Card>

          <Card className="p-6">
            <div className="mb-1 flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-teal-600" />
              <h2 className="text-sm font-semibold text-gray-900">Delivery mode</h2>
            </div>
            <p className="mb-4 text-xs text-gray-500">
              Self-paced courses give students direct access to all published modules in the portal without needing a live session.
            </p>
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
              <Switch
                checked={isSelfPaced}
                onChange={toggleSelfPaced}
                disabled={togglingMode}
                label="Self-paced mode"
                description="Enable if this batch is studying independently"
              />
            </div>
          </Card>

          <Card className="p-6">
            <div className="mb-3 flex items-center gap-2">
              <Lock className="h-3.5 w-3.5 text-gray-400" />
              <h2 className="text-sm font-semibold text-gray-900">Batch details</h2>
            </div>
            <p className="mb-4 text-xs text-gray-500">
              Owned by the external system and read-only here.
            </p>
            <dl className="space-y-3 text-sm">
              {[
                ['Trainer', batch.trainer_name ?? '—'],
                ['Trainer email', batch.trainer_email ?? '—'],
                ['Mode', batch.mode ?? '—'],
                ['Location', batch.location ?? '—'],
                ['Starts', batch.start_date ?? '—'],
                ['Ends', batch.end_date ?? '—'],
                ['Timezone', batch.timezone ?? '—'],
                ['External ID', batch.external_id],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between gap-3">
                  <dt className="shrink-0 text-gray-500">{label}</dt>
                  <dd className="truncate text-right text-gray-900">{value}</dd>
                </div>
              ))}
              {batch.schedule?.days && (
                <div className="flex justify-between gap-3">
                  <dt className="shrink-0 text-gray-500">Schedule</dt>
                  <dd className="text-right text-gray-900">
                    {batch.schedule.days.join(', ')}
                    {batch.schedule.start_time && (
                      <span className="block text-xs text-gray-500">
                        {batch.schedule.start_time}–{batch.schedule.end_time}
                      </span>
                    )}
                  </dd>
                </div>
              )}
            </dl>
          </Card>
        </div>
      </div>
    </div>
  );
}
