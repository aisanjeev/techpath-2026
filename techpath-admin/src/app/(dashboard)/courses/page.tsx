'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Search, Folder, Users, GraduationCap } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { DataTable, Column } from '@/components/tables/DataTable';
import { StatusBadge, FeaturedBadge } from '@/components/tables/StatusBadge';
import { ConfirmModal } from '@/components/ui/Modal';
import { courseService } from '@/services/course.service';
import { formatDate, formatCurrency } from '@/lib/utils/format';
import type { Course } from '@/types/api';

export default function CoursesPage() {
  const router = useRouter();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [levelFilter, setLevelFilter] = useState<string>('');
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; course: Course | null }>({
    open: false,
    course: null,
  });
  const [deleting, setDeleting] = useState(false);
  const limit = 20;

  const fetchCourses = useCallback(async () => {
    setLoading(true);
    try {
      const response = await courseService.list({
        skip: (page - 1) * limit,
        limit,
        status: statusFilter as 'draft' | 'published' | 'archived' || undefined,
        level: levelFilter || undefined,
      });
      setCourses(response.items);
      setTotal(response.total);
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast.error('Failed to load courses');
    } finally {
      setLoading(false);
    }
  }, [page, statusFilter, levelFilter]);

  useEffect(() => {
    fetchCourses();
  }, [fetchCourses]);

  const handleDelete = async () => {
    if (!deleteModal.course) return;
    setDeleting(true);
    try {
      await courseService.delete(deleteModal.course.id);
      toast.success('Course deleted successfully');
      setDeleteModal({ open: false, course: null });
      fetchCourses();
    } catch (error) {
      console.error('Error deleting course:', error);
      toast.error('Failed to delete course');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<Course>[] = [
    {
      key: 'title',
      header: 'Course',
      sortable: true,
      render: (item) => (
        <div className="flex items-center gap-3">
          {item.featured_image ? (
            <img
              src={item.featured_image}
              alt={item.title}
              className="h-10 w-16 rounded object-cover"
            />
          ) : (
            <div className="h-10 w-16 rounded bg-gray-100 flex items-center justify-center">
              <GraduationCap className="h-5 w-5 text-gray-400" />
            </div>
          )}
          <div>
            <div className="font-medium text-gray-900">{item.title}</div>
            <div className="text-xs text-gray-500">/{item.slug}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Category',
      render: (item) => (
        <span className="inline-flex rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800">
          {item.category.name}
        </span>
      ),
    },
    {
      key: 'price',
      header: 'Price',
      render: (item) => (
        <div>
          <span className="font-medium">{formatCurrency(item.price, item.currency)}</span>
          {item.original_price && item.original_price > item.price && (
            <span className="ml-2 text-xs text-gray-500 line-through">
              {formatCurrency(item.original_price, item.currency)}
            </span>
          )}
        </div>
      ),
    },
    {
      key: 'level',
      header: 'Level',
      render: (item) => (
        <span
          className={`inline-flex rounded-full px-2 py-0.5 text-xs ${
            item.level === 'beginner'
              ? 'bg-green-100 text-green-800'
              : item.level === 'intermediate'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-red-100 text-red-800'
          }`}
        >
          {item.level.charAt(0).toUpperCase() + item.level.slice(1)}
        </span>
      ),
    },
    {
      key: 'duration',
      header: 'Duration',
      render: (item) => item.duration,
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
        title="Courses"
        description="Manage your training courses"
        actions={
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => router.push('/courses/categories')}>
              <Folder className="h-4 w-4 mr-2" />
              Categories
            </Button>
            <Button variant="outline" onClick={() => router.push('/courses/enrollments')}>
              <Users className="h-4 w-4 mr-2" />
              Enrollments
            </Button>
            <Button onClick={() => router.push('/courses/create')}>
              <Plus className="h-4 w-4" />
              New Course
            </Button>
          </div>
        }
      />

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search courses..."
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
        <Select
          value={levelFilter}
          onChange={(e) => {
            setLevelFilter(e.target.value);
            setPage(1);
          }}
          className="w-40"
        >
          <option value="">All Levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={courses}
        loading={loading}
        keyExtractor={(item) => item.id}
        onEdit={(item) => router.push(`/courses/${item.slug}`)}
        onDelete={(item) => setDeleteModal({ open: true, course: item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No courses found. Create your first course!"
      />

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, course: null })}
        onConfirm={handleDelete}
        title="Delete Course"
        description={`Are you sure you want to delete "${deleteModal.course?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

