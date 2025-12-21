'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { DataTable, Column } from '@/components/tables/DataTable';
import { StatusBadge, FeaturedBadge } from '@/components/tables/StatusBadge';
import { ConfirmModal } from '@/components/ui/Modal';
import { caseStudiesService } from '@/services/case-studies.service';
import { formatDate } from '@/lib/utils/format';
import type { CaseStudy } from '@/types/api';

export default function CaseStudiesPage() {
  const router = useRouter();
  const [caseStudies, setCaseStudies] = useState<CaseStudy[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; caseStudy: CaseStudy | null }>({
    open: false,
    caseStudy: null,
  });
  const [deleting, setDeleting] = useState(false);
  const limit = 20;

  const fetchCaseStudies = useCallback(async () => {
    setLoading(true);
    try {
      const response = await caseStudiesService.list({
        skip: (page - 1) * limit,
        limit,
        status: statusFilter as 'draft' | 'published' | 'archived' || undefined,
      });
      // Filter by search client-side since backend doesn't support search param
      let filtered = response.items;
      if (search) {
        const searchLower = search.toLowerCase();
        filtered = filtered.filter(
          (cs) =>
            cs.title.toLowerCase().includes(searchLower) ||
            cs.client_name.toLowerCase().includes(searchLower)
        );
      }
      setCaseStudies(filtered);
      setTotal(filtered.length);
    } catch (error) {
      console.error('Error fetching case studies:', error);
      toast.error('Failed to load case studies');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => {
    fetchCaseStudies();
  }, [fetchCaseStudies]);

  const handleDelete = async () => {
    if (!deleteModal.caseStudy) return;
    setDeleting(true);
    try {
      await caseStudiesService.delete(deleteModal.caseStudy.id);
      toast.success('Case study deleted successfully');
      setDeleteModal({ open: false, caseStudy: null });
      fetchCaseStudies();
    } catch (error) {
      console.error('Error deleting case study:', error);
      toast.error('Failed to delete case study');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<CaseStudy>[] = [
    {
      key: 'title',
      header: 'Title',
      sortable: true,
      render: (item) => (
        <div>
          <div className="font-medium text-gray-900">{item.title}</div>
          <div className="text-xs text-gray-500">{item.client_name}</div>
        </div>
      ),
    },
    {
      key: 'industry',
      header: 'Industry',
    },
    {
      key: 'status',
      header: 'Status',
      render: (item) => <StatusBadge status={item.status} />,
    },
    {
      key: 'featured',
      header: 'Featured',
      render: (item) => <FeaturedBadge featured={item.featured} />,
    },
    {
      key: 'created_at',
      header: 'Created',
      sortable: true,
      render: (item) => formatDate(item.created_at),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Case Studies"
        description="Manage your success stories"
        actions={
          <Button onClick={() => router.push('/case-studies/create')}>
            <Plus className="h-4 w-4" />
            Add Case Study
          </Button>
        }
      />

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search case studies..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="pl-10"
          />
        </div>
        <Select
          value={statusFilter}
          onChange={(e) => {
            setStatusFilter(e.target.value);
            setPage(1);
          }}
          className="w-40"
        >
          <option value="">All Status</option>
          <option value="draft">Draft</option>
          <option value="published">Published</option>
          <option value="archived">Archived</option>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={caseStudies}
        loading={loading}
        keyExtractor={(item) => item.id}
        onEdit={(item) => router.push(`/case-studies/${item.slug}`)}
        onDelete={(item) => setDeleteModal({ open: true, caseStudy: item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No case studies found. Create your first success story!"
      />

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, caseStudy: null })}
        onConfirm={handleDelete}
        title="Delete Case Study"
        description={`Are you sure you want to delete "${deleteModal.caseStudy?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

