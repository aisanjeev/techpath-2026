'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Plus, Search, FolderTree, Tags } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { DataTable, Column } from '@/components/tables/DataTable';
import { StatusBadge, FeaturedBadge } from '@/components/tables/StatusBadge';
import { ConfirmModal } from '@/components/ui/Modal';
import { blogService } from '@/services/blog.service';
import { formatDate } from '@/lib/utils/format';
import type { BlogPost } from '@/types/api';

export default function BlogPage() {
  const router = useRouter();
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; post: BlogPost | null }>({
    open: false,
    post: null,
  });
  const [deleting, setDeleting] = useState(false);
  const limit = 20;

  const fetchPosts = useCallback(async () => {
    setLoading(true);
    try {
      const response = await blogService.list({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        status: statusFilter as 'draft' | 'published' | 'archived' || undefined,
      });
      setPosts(response.items);
      setTotal(response.total);
    } catch (error) {
      console.error('Error fetching posts:', error);
      toast.error('Failed to load blog posts');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const handleDelete = async () => {
    if (!deleteModal.post) return;
    setDeleting(true);
    try {
      await blogService.delete(deleteModal.post.id);
      toast.success('Blog post deleted successfully');
      setDeleteModal({ open: false, post: null });
      fetchPosts();
    } catch (error) {
      console.error('Error deleting post:', error);
      toast.error('Failed to delete blog post');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<BlogPost>[] = [
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
      key: 'category',
      header: 'Category',
      render: (item) => (
        <span className="inline-flex rounded-md bg-teal-50 px-2 py-1 text-xs font-medium text-teal-700">
          {item.category?.name || 'Uncategorized'}
        </span>
      ),
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
      key: 'tags',
      header: 'Tags',
      render: (item) => (
        <div className="flex flex-wrap gap-1">
          {item.tags.slice(0, 2).map((tag) => (
            <span
              key={tag.id}
              className="inline-flex rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
            >
              {tag.name}
            </span>
          ))}
          {item.tags.length > 2 && (
            <span className="text-xs text-gray-500">+{item.tags.length - 2}</span>
          )}
        </div>
      ),
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
        title="Blog Posts"
        description="Manage your blog articles"
        actions={
          <div className="flex items-center gap-2">
            <Link href="/blog/categories">
              <Button variant="secondary">
                <FolderTree className="h-4 w-4" />
                Categories
              </Button>
            </Link>
            <Link href="/blog/tags">
              <Button variant="secondary">
                <Tags className="h-4 w-4" />
                Tags
              </Button>
            </Link>
            <Button onClick={() => router.push('/blog/create')}>
              <Plus className="h-4 w-4" />
              New Post
            </Button>
          </div>
        }
      />

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search posts..."
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
        data={posts}
        loading={loading}
        keyExtractor={(item) => item.id}
        onEdit={(item) => router.push(`/blog/${item.slug}`)}
        onDelete={(item) => setDeleteModal({ open: true, post: item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No blog posts found. Write your first article!"
      />

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, post: null })}
        onConfirm={handleDelete}
        title="Delete Blog Post"
        description={`Are you sure you want to delete "${deleteModal.post?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}
