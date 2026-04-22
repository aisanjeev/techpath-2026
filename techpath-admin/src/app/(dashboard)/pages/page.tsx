'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ExternalLink, Plus, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { DataTable, Column } from '@/components/tables/DataTable';
import { StatusBadge } from '@/components/tables/StatusBadge';
import { ConfirmModal } from '@/components/ui/Modal';
import { pagesService } from '@/services/pages.service';
import { formatDate } from '@/lib/utils/format';
import type { PageListItem } from '@/types/api';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || '';

export default function PagesListPage() {
  const router = useRouter();
  const [items, setItems] = useState<PageListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [deleteModal, setDeleteModal] = useState<{
    open: boolean;
    item: PageListItem | null;
  }>({ open: false, item: null });
  const [deleting, setDeleting] = useState(false);
  const limit = 20;

  const fetchItems = useCallback(async () => {
    setLoading(true);
    try {
      const response = await pagesService.list({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        status: (statusFilter as 'draft' | 'published' | 'archived') || undefined,
      });
      setItems(response.items);
      setTotal(response.total);
    } catch (error) {
      console.error('Error fetching pages:', error);
      toast.error('Failed to load pages');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleDelete = async () => {
    if (!deleteModal.item) return;
    setDeleting(true);
    try {
      await pagesService.delete(deleteModal.item.id);
      toast.success('Page deleted successfully');
      setDeleteModal({ open: false, item: null });
      fetchItems();
    } catch (error) {
      console.error('Error deleting page:', error);
      toast.error('Failed to delete page');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<PageListItem>[] = [
    {
      key: 'title',
      header: 'Title',
      sortable: true,
      render: (item) => (
        <div>
          <div className="font-medium text-gray-900">{item.title}</div>
          <div className="text-xs text-gray-500">/{item.slug}</div>
        </div>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (item) => <StatusBadge status={item.status} />,
    },
    {
      key: 'published_at',
      header: 'Published',
      render: (item) =>
        item.published_at ? formatDate(item.published_at) : '—',
    },
    {
      key: 'updated_at',
      header: 'Updated',
      sortable: true,
      render: (item) => formatDate(item.updated_at),
    },
    {
      key: 'actions_link',
      header: 'Live URL',
      render: (item) =>
        item.status === 'published' ? (
          <a
            href={`${SITE_URL}/${item.slug}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-teal-600 hover:text-teal-700"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="h-3 w-3" />
            View
          </a>
        ) : (
          <span className="text-xs text-gray-400">—</span>
        ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Pages"
        description="Standalone CMS pages served at domain.com/{slug}"
        actions={
          <Button onClick={() => router.push('/pages/create')}>
            <Plus className="h-4 w-4" />
            New Page
          </Button>
        }
      />

      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search pages..."
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

      <DataTable
        columns={columns}
        data={items}
        loading={loading}
        keyExtractor={(item) => item.id}
        onEdit={(item) => router.push(`/pages/${item.slug}`)}
        onDelete={(item) => setDeleteModal({ open: true, item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No pages yet. Create your first page!"
      />

      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, item: null })}
        onConfirm={handleDelete}
        title="Delete Page"
        description={`Are you sure you want to delete "${deleteModal.item?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}
