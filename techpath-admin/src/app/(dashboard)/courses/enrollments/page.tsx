'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Search, Phone, Mail, Calendar, User } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { DataTable, Column } from '@/components/tables/DataTable';
import { ConfirmModal } from '@/components/ui/Modal';
import { courseService } from '@/services/course.service';
import { formatDate, formatRelativeTime } from '@/lib/utils/format';
import type { CourseEnrollment } from '@/types/api';

const statusColors: Record<string, string> = {
  new: 'bg-blue-100 text-blue-800',
  contacted: 'bg-yellow-100 text-yellow-800',
  interested: 'bg-purple-100 text-purple-800',
  enrolled: 'bg-green-100 text-green-800',
  not_interested: 'bg-gray-100 text-gray-800',
  closed: 'bg-red-100 text-red-800',
};

export default function EnrollmentsPage() {
  const router = useRouter();
  const [enrollments, setEnrollments] = useState<CourseEnrollment[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [stats, setStats] = useState<{ total: number; by_status: Record<string, number> } | null>(null);
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; enrollment: CourseEnrollment | null }>({
    open: false,
    enrollment: null,
  });
  const [deleting, setDeleting] = useState(false);
  const limit = 20;

  const fetchEnrollments = useCallback(async () => {
    setLoading(true);
    try {
      const [response, statsData] = await Promise.all([
        courseService.listEnrollments({
          skip: (page - 1) * limit,
          limit,
          status: statusFilter || undefined,
        }),
        courseService.getEnrollmentStats(),
      ]);
      setEnrollments(response.items);
      setTotal(response.total);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching enrollments:', error);
      toast.error('Failed to load enrollments');
    } finally {
      setLoading(false);
    }
  }, [page, statusFilter]);

  useEffect(() => {
    fetchEnrollments();
  }, [fetchEnrollments]);

  const handleDelete = async () => {
    if (!deleteModal.enrollment) return;
    setDeleting(true);
    try {
      await courseService.deleteEnrollment(deleteModal.enrollment.id);
      toast.success('Enrollment deleted successfully');
      setDeleteModal({ open: false, enrollment: null });
      fetchEnrollments();
    } catch (error) {
      console.error('Error deleting enrollment:', error);
      toast.error('Failed to delete enrollment');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<CourseEnrollment>[] = [
    {
      key: 'name',
      header: 'Lead',
      sortable: true,
      render: (item) => (
        <div>
          <div className="font-medium text-gray-900 flex items-center gap-2">
            <User className="h-4 w-4 text-gray-400" />
            {item.name}
          </div>
          <div className="text-xs text-gray-500 flex items-center gap-1 mt-1">
            <Mail className="h-3 w-3" />
            {item.email}
          </div>
          <div className="text-xs text-gray-500 flex items-center gap-1">
            <Phone className="h-3 w-3" />
            {item.phone}
          </div>
        </div>
      ),
    },
    {
      key: 'course',
      header: 'Course Interest',
      render: (item) => (
        item.course ? (
          <span className="text-sm text-gray-900">{item.course.title}</span>
        ) : (
          <span className="text-sm text-gray-400">General Inquiry</span>
        )
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (item) => (
        <span className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${statusColors[item.status]}`}>
          {item.status.replace('_', ' ').charAt(0).toUpperCase() + item.status.slice(1).replace('_', ' ')}
        </span>
      ),
    },
    {
      key: 'source',
      header: 'Source',
      render: (item) => (
        <span className="text-sm text-gray-600">{item.source || '-'}</span>
      ),
    },
    {
      key: 'assigned_to',
      header: 'Assigned To',
      render: (item) => (
        <span className="text-sm text-gray-600">{item.assigned_to || '-'}</span>
      ),
    },
    {
      key: 'next_followup_at',
      header: 'Follow-up',
      render: (item) => (
        item.next_followup_at ? (
          <div className="flex items-center gap-1 text-sm">
            <Calendar className="h-3 w-3 text-gray-400" />
            <span className={new Date(item.next_followup_at) < new Date() ? 'text-red-600 font-medium' : 'text-gray-600'}>
              {formatRelativeTime(item.next_followup_at)}
            </span>
          </div>
        ) : (
          <span className="text-gray-400">-</span>
        )
      ),
    },
    {
      key: 'created_at',
      header: 'Received',
      sortable: true,
      render: (item) => (
        <span className="text-sm text-gray-600">{formatRelativeTime(item.created_at)}</span>
      ),
    },
  ];

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Courses', href: '/courses' },
          { label: 'Enrollments' },
        ]}
      />
      <PageHeader
        title="Course Enrollments"
        description="Manage training inquiries and enrollments"
      />

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-6">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-sm text-gray-500">Total</div>
          </div>
          {Object.entries(stats.by_status).map(([status, count]) => (
            <div key={status} className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="text-2xl font-bold text-gray-900">{count}</div>
              <div className="text-sm text-gray-500 capitalize">{status.replace('_', ' ')}</div>
            </div>
          ))}
        </div>
      )}

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <Select
          value={statusFilter}
          onChange={(e) => {
            setStatusFilter(e.target.value);
            setPage(1);
          }}
          className="w-48"
        >
          <option value="">All Status</option>
          <option value="new">New</option>
          <option value="contacted">Contacted</option>
          <option value="interested">Interested</option>
          <option value="enrolled">Enrolled</option>
          <option value="not_interested">Not Interested</option>
          <option value="closed">Closed</option>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={enrollments}
        loading={loading}
        keyExtractor={(item) => item.id}
        onEdit={(item) => router.push(`/courses/enrollments/${item.id}`)}
        onDelete={(item) => setDeleteModal({ open: true, enrollment: item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No enrollments found."
      />

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, enrollment: null })}
        onConfirm={handleDelete}
        title="Delete Enrollment"
        description={`Are you sure you want to delete the enrollment from "${deleteModal.enrollment?.name}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

