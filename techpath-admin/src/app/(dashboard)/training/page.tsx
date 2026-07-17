'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { DataTable, type Column } from '@/components/tables/DataTable';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { ConfirmModal } from '@/components/ui/Modal';
import { trainingService } from '@/services/training.service';
import type { ContentStatus, TrainingProgram } from '@/types/training';

const STATUS_VARIANT: Record<ContentStatus, 'success' | 'warning' | 'default'> = {
  published: 'success',
  draft: 'warning',
  archived: 'default',
};

export default function TrainingProgramsPage() {
  const router = useRouter();
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<ContentStatus | ''>('');
  const [deleting, setDeleting] = useState<TrainingProgram | null>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);

  const limit = 20;

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await trainingService.listPrograms({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        status: status || undefined,
      });
      setPrograms(result.items);
      setTotal(result.total);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load programmes');
    } finally {
      setLoading(false);
    }
  }, [page, search, status]);

  useEffect(() => {
    const timer = setTimeout(load, search ? 250 : 0);
    return () => clearTimeout(timer);
  }, [load, search]);

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteBusy(true);
    try {
      await trainingService.deleteProgram(deleting.id);
      toast.success('Programme deleted');
      setDeleting(null);
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not delete');
    } finally {
      setDeleteBusy(false);
    }
  };

  const columns: Column<TrainingProgram>[] = [
    {
      key: 'title',
      header: 'Programme',
      render: (p) => (
        <div>
          <p className="font-medium text-gray-900">{p.title}</p>
          <p className="text-xs text-gray-500">/{p.slug}</p>
        </div>
      ),
    },
    {
      key: 'delivery_mode',
      header: 'Delivery',
      render: (p) => <span className="capitalize text-gray-600">{p.delivery_mode}</span>,
    },
    {
      key: 'course_id',
      header: 'Course',
      render: (p) =>
        p.course_id ? (
          <Badge variant="info">Linked</Badge>
        ) : (
          // Not a problem: offline-only training legitimately has no public course.
          <span className="text-xs text-gray-400">Standalone</span>
        ),
    },
    {
      key: 'module_count',
      header: 'Modules',
      render: (p) => <span className="text-gray-600">{p.module_count}</span>,
    },
    {
      key: 'status',
      header: 'Status',
      render: (p) => <Badge variant={STATUS_VARIANT[p.status]}>{p.status}</Badge>,
    },
  ];

  return (
    <div>
      <PageHeader
        title="Training Programs"
        description="Course material organised into modules and reusable lecture assets"
        actions={
          <Button onClick={() => router.push('/training/create')}>
            <Plus className="mr-1 h-4 w-4" />
            New program
          </Button>
        }
      />

      <div className="mb-4 flex gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search programmes…"
            className="pl-9"
          />
        </div>
        <Select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value as ContentStatus | '');
            setPage(1);
          }}
          className="max-w-[170px]"
        >
          <option value="">All statuses</option>
          <option value="draft">Draft</option>
          <option value="published">Published</option>
          <option value="archived">Archived</option>
        </Select>
      </div>

      <DataTable
        columns={columns}
        data={programs}
        loading={loading}
        keyExtractor={(p) => p.id}
        onView={(p) => router.push(`/training/${p.id}`)}
        onEdit={(p) => router.push(`/training/${p.id}`)}
        onDelete={(p) => setDeleting(p)}
        pagination={{ page, limit, total, onPageChange: setPage }}
        emptyMessage="No training programmes yet. Create one to get started."
      />

      <ConfirmModal
        isOpen={!!deleting}
        onClose={() => setDeleting(null)}
        onConfirm={handleDelete}
        title="Delete this programme?"
        description={`"${deleting?.title}" and its ${deleting?.module_count ?? 0} module(s) will be removed. The lecture assets themselves stay in the library and are not deleted.`}
        confirmText="Delete"
        loading={deleteBusy}
      />
    </div>
  );
}
