'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { RefreshCw, Search, Lock, AlertTriangle, CheckCircle2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { DataTable, type Column } from '@/components/tables/DataTable';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { trainingRosterService } from '@/services/training-roster.service';
import type { SyncStatus, TrainingBatch } from '@/types/training';

const STATUS_VARIANT: Record<string, 'success' | 'info' | 'default' | 'error'> = {
  running: 'success',
  upcoming: 'info',
  completed: 'default',
  cancelled: 'error',
};

function relativeTime(iso?: string | null): string {
  if (!iso) return 'never';
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export default function BatchesPage() {
  const router = useRouter();
  const [batches, setBatches] = useState<TrainingBatch[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [syncStatus, setSyncStatus] = useState<SyncStatus | null>(null);
  const [syncing, setSyncing] = useState(false);

  const limit = 20;

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await trainingRosterService.listBatches({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        status: status || undefined,
      });
      setBatches(result.items);
      setTotal(result.total);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load batches');
    } finally {
      setLoading(false);
    }
  }, [page, search, status]);

  const loadSyncStatus = useCallback(async () => {
    try {
      setSyncStatus(await trainingRosterService.syncStatus());
    } catch {
      // A stale mirror is still usable; don't let the status banner break the page.
      setSyncStatus(null);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(load, search ? 250 : 0);
    return () => clearTimeout(timer);
  }, [load, search]);

  useEffect(() => {
    void loadSyncStatus();
  }, [loadSyncStatus]);

  const runSync = async () => {
    setSyncing(true);
    try {
      const result = await trainingRosterService.runSync('all');
      const counts = Object.values(result.results)
        .map((r) => `${r.resource}: ${r.processed}`)
        .join(', ');
      if (result.success) {
        toast.success(`Synced — ${counts}`);
      } else {
        const failure = Object.values(result.results).find((r) => r.error);
        toast.error(failure?.error ?? 'Sync failed');
      }
      await Promise.all([load(), loadSyncStatus()]);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  const batchesState = syncStatus?.resources.find((r) => r.resource === 'batches');

  const columns: Column<TrainingBatch>[] = [
    {
      key: 'name',
      header: 'Batch',
      render: (b) => (
        <div>
          <p className="font-medium text-gray-900">{b.name}</p>
          <p className="text-xs text-gray-500">{b.code ?? b.external_id}</p>
        </div>
      ),
    },
    {
      key: 'trainer_name',
      header: 'Trainer',
      render: (b) => (
        <div>
          <p className="text-gray-700">{b.trainer_name ?? '—'}</p>
          <p className="text-xs text-gray-400">{b.trainer_email ?? ''}</p>
        </div>
      ),
    },
    {
      key: 'program_id',
      header: 'Program',
      render: (b) =>
        b.program_id ? (
          <Badge variant="info">Linked</Badge>
        ) : (
          // Without a linked programme, a trainer has nothing to present.
          <Badge variant="warning">Not linked</Badge>
        ),
    },
    {
      key: 'student_count',
      header: 'Students',
      render: (b) => <span className="text-gray-600">{b.student_count}</span>,
    },
    {
      key: 'mode',
      header: 'Mode',
      render: (b) => <span className="capitalize text-gray-600">{b.mode ?? '—'}</span>,
    },
    {
      key: 'status',
      header: 'Status',
      render: (b) => (
        <Badge variant={STATUS_VARIANT[b.status ?? ''] ?? 'default'}>{b.status ?? '—'}</Badge>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Batches"
        description="Mirrored from the external student system — read-only here"
        actions={
          <Button onClick={runSync} disabled={syncing} variant="outline">
            <RefreshCw className={`mr-1 h-4 w-4 ${syncing ? 'animate-spin' : ''}`} />
            {syncing ? 'Syncing…' : 'Sync now'}
          </Button>
        }
      />

      {/* Freshness is surfaced rather than assumed — this data is a cache. */}
      <Card className="mb-4 flex flex-wrap items-center justify-between gap-3 p-4">
        <div className="flex items-center gap-3">
          {syncStatus?.healthy ? (
            <CheckCircle2 className="h-5 w-5 text-teal-600" />
          ) : (
            <AlertTriangle className="h-5 w-5 text-amber-500" />
          )}
          <div>
            <p className="text-sm font-medium text-gray-900">
              Source: {syncStatus?.provider ?? 'unknown'}
              {syncStatus?.provider === 'mock' && (
                <span className="ml-2 text-xs font-normal text-amber-600">
                  (sample data — the live API is not connected yet)
                </span>
              )}
            </p>
            <p className="text-xs text-gray-500">
              Last synced {relativeTime(batchesState?.last_success_at)}
              {batchesState?.last_status === 'error' && (
                <span className="ml-1 text-red-600">· last run failed</span>
              )}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-gray-500">
          <Lock className="h-3.5 w-3.5" />
          Owned by the external system
        </div>
      </Card>

      {batchesState?.last_error && (
        <Card className="mb-4 border-red-200 bg-red-50 p-4">
          <p className="text-sm font-medium text-red-900">The last sync failed</p>
          <p className="mt-1 break-words text-xs text-red-700">{batchesState.last_error}</p>
        </Card>
      )}

      <div className="mb-4 flex gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search batches…"
            className="pl-9"
          />
        </div>
        <Select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(1);
          }}
          className="max-w-[170px]"
        >
          <option value="">All statuses</option>
          <option value="upcoming">Upcoming</option>
          <option value="running">Running</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </Select>
      </div>

      <DataTable
        columns={columns}
        data={batches}
        loading={loading}
        keyExtractor={(b) => b.id}
        onView={(b) => router.push(`/training/batches/${b.id}`)}
        pagination={{ page, limit, total, onPageChange: setPage }}
        emptyMessage="No batches yet. Run a sync to pull them from the external system."
      />
    </div>
  );
}
