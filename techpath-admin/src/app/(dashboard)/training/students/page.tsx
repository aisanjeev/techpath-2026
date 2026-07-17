'use client';

import { useCallback, useEffect, useState } from 'react';
import { Search, Lock } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { DataTable, type Column } from '@/components/tables/DataTable';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { trainingRosterService } from '@/services/training-roster.service';
import type { TrainingStudent } from '@/types/training';

const STATUS_VARIANT: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  on_hold: 'warning',
  dropped: 'error',
  completed: 'default',
};

export default function StudentsPage() {
  const [students, setStudents] = useState<TrainingStudent[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');

  const limit = 20;

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await trainingRosterService.listStudents({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        status: status || undefined,
      });
      setStudents(result.items);
      setTotal(result.total);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load students');
    } finally {
      setLoading(false);
    }
  }, [page, search, status]);

  useEffect(() => {
    const timer = setTimeout(load, search ? 250 : 0);
    return () => clearTimeout(timer);
  }, [load, search]);

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
      key: 'enrolled_on',
      header: 'Enrolled',
      render: (s) => <span className="text-gray-600">{s.enrolled_on ?? '—'}</span>,
    },
    {
      key: 'status',
      header: 'Status',
      render: (s) => (
        <Badge variant={STATUS_VARIANT[s.status ?? ''] ?? 'default'}>{s.status ?? '—'}</Badge>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Students"
        description="Mirrored from the external student system — read-only here"
      />

      <Card className="mb-4 flex items-center gap-2 p-3 text-xs text-gray-500">
        <Lock className="h-3.5 w-3.5" />
        Student records are owned by the external system. To change one, change it there
        and sync.
      </Card>

      <div className="mb-4 flex gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search by name, email or roll no…"
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
          <option value="active">Active</option>
          <option value="on_hold">On hold</option>
          <option value="completed">Completed</option>
          <option value="dropped">Dropped</option>
        </Select>
      </div>

      <DataTable
        columns={columns}
        data={students}
        loading={loading}
        keyExtractor={(s) => s.id}
        pagination={{ page, limit, total, onPageChange: setPage }}
        emptyMessage="No students yet. Sync from the Batches page to pull them in."
      />
    </div>
  );
}
