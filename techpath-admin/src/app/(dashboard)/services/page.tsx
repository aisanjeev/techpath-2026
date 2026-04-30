'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { DataTable, Column } from '@/components/tables/DataTable';
import { ActiveBadge, FeaturedBadge } from '@/components/tables/StatusBadge';
import { ConfirmModal } from '@/components/ui/Modal';
import { servicesService } from '@/services/services.service';
import { formatDate } from '@/lib/utils/format';
import type { Service } from '@/types/api';

export default function ServicesPage() {
  const router = useRouter();
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; service: Service | null }>({
    open: false,
    service: null,
  });
  const [deleting, setDeleting] = useState(false);
  const limit = 20;

  const fetchServices = useCallback(async () => {
    setLoading(true);
    try {
      const response = await servicesService.list({
        skip: (page - 1) * limit,
        limit,
      });
      // Filter by search client-side since backend doesn't support search param
      let filtered = response.items;
      if (search) {
        const searchLower = search.toLowerCase();
        filtered = filtered.filter(
          (s) =>
            s.title.toLowerCase().includes(searchLower) ||
            s.slug.toLowerCase().includes(searchLower)
        );
      }
      setServices(filtered);
      setTotal(filtered.length);
    } catch (error) {
      console.error('Error fetching services:', error);
      toast.error('Failed to load services');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    fetchServices();
  }, [fetchServices]);

  const handleDelete = async () => {
    if (!deleteModal.service) return;
    setDeleting(true);
    try {
      await servicesService.delete(deleteModal.service.id);
      toast.success('Service deleted successfully');
      setDeleteModal({ open: false, service: null });
      fetchServices();
    } catch (error) {
      console.error('Error deleting service:', error);
      toast.error('Failed to delete service');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<Service>[] = [
    {
      key: 'title',
      header: 'Title',
      sortable: true,
      render: (item) => (
        <div>
          <div className="font-medium text-gray-900">{item.title}</div>
          <div className="text-xs text-gray-500">{item.slug}</div>
        </div>
      ),
    },
    {
      key: 'is_active',
      header: 'Status',
      render: (item) => <ActiveBadge active={item.is_active} />,
    },
    {
      key: 'featured',
      header: 'Featured',
      render: (item) => <FeaturedBadge featured={item.featured} />,
    },
    {
      key: 'layout_size',
      header: 'Layout',
      render: (item) => {
        const cls =
          item.layout_size === 'large'
            ? 'bg-indigo-100 text-indigo-700'
            : item.layout_size === 'wide'
            ? 'bg-amber-100 text-amber-700'
            : 'bg-slate-100 text-slate-700';
        return (
          <span className={`inline-flex rounded px-2 py-0.5 text-xs font-medium capitalize ${cls}`}>
            {item.layout_size}
          </span>
        );
      },
    },
    {
      key: 'display_order',
      header: 'Order',
      sortable: true,
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
        title="Services"
        description="Manage your service offerings"
        actions={
          <Button onClick={() => router.push('/services/create')}>
            <Plus className="h-4 w-4" />
            Add Service
          </Button>
        }
      />

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search services..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="pl-10"
          />
        </div>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={services}
        loading={loading}
        keyExtractor={(item) => item.id}
        onEdit={(item) => router.push(`/services/${item.slug}`)}
        onDelete={(item) => setDeleteModal({ open: true, service: item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No services found. Create your first service!"
      />

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, service: null })}
        onConfirm={handleDelete}
        title="Delete Service"
        description={`Are you sure you want to delete "${deleteModal.service?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

