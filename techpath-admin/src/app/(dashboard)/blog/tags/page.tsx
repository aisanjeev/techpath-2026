'use client';

import { useEffect, useState, useCallback } from 'react';
import { Plus, Pencil, Trash2, Tag } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { FormField } from '@/components/ui/FormField';
import { blogService } from '@/services/blog.service';
import { slugify } from '@/lib/utils/format';
import type { BlogTag } from '@/types/api';

export default function TagsPage() {
  const [tags, setTags] = useState<BlogTag[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingTag, setEditingTag] = useState<BlogTag | null>(null);
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; tag: BlogTag | null }>({
    open: false,
    tag: null,
  });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
  });

  const fetchTags = useCallback(async () => {
    setLoading(true);
    try {
      const data = await blogService.listTags();
      setTags(data);
    } catch (error) {
      console.error('Error fetching tags:', error);
      toast.error('Failed to load tags');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTags();
  }, [fetchTags]);

  const handleOpenCreate = () => {
    setEditingTag(null);
    setFormData({
      name: '',
      slug: '',
    });
    setModalOpen(true);
  };

  const handleOpenEdit = (tag: BlogTag) => {
    setEditingTag(tag);
    setFormData({
      name: tag.name,
      slug: tag.slug,
    });
    setModalOpen(true);
  };

  const handleNameChange = (name: string) => {
    setFormData((prev) => ({
      ...prev,
      name,
      slug: !editingTag ? slugify(name) : prev.slug,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      if (editingTag) {
        // Note: API currently doesn't support tag update, just create/delete
        toast.error('Tag editing is not supported. Delete and create a new tag instead.');
      } else {
        await blogService.createTag(formData);
        toast.success('Tag created successfully');
      }
      setModalOpen(false);
      fetchTags();
    } catch (error: any) {
      console.error('Error saving tag:', error);
      toast.error(error.message || 'Failed to save tag');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteModal.tag) return;
    setDeleting(true);

    try {
      await blogService.deleteTag(deleteModal.tag.id);
      toast.success('Tag deleted successfully');
      setDeleteModal({ open: false, tag: null });
      fetchTags();
    } catch (error: any) {
      console.error('Error deleting tag:', error);
      toast.error(error.message || 'Failed to delete tag');
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Blog Tags"
        description="Manage tags for your blog posts"
        actions={
          <Button onClick={handleOpenCreate}>
            <Plus className="mr-2 h-4 w-4" />
            Add Tag
          </Button>
        }
      />

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : tags.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center bg-white rounded-lg border border-gray-200">
          <Tag className="h-12 w-12 text-gray-400 mb-4" />
          <p className="text-gray-500">No tags found</p>
          <Button className="mt-4" onClick={handleOpenCreate}>
            <Plus className="mr-2 h-4 w-4" />
            Create First Tag
          </Button>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="grid gap-2 p-4">
            {tags.map((tag) => (
              <div
                key={tag.id}
                className="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <Tag className="h-4 w-4 text-gray-400" />
                  <div>
                    <span className="font-medium text-gray-900">{tag.name}</span>
                    <span className="ml-2 text-sm text-gray-500">/{tag.slug}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setDeleteModal({ open: true, tag })}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Create Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Create Tag"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <FormField label="Name" htmlFor="name" required>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => handleNameChange(e.target.value)}
              placeholder="e.g., AI"
              required
            />
          </FormField>

          <FormField label="Slug" htmlFor="slug" description="URL-friendly name">
            <Input
              id="slug"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              placeholder="e.g., ai"
              pattern="^[a-z0-9-]+$"
              required
            />
          </FormField>

          <div className="flex justify-end gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setModalOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit" loading={saving}>
              Create
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, tag: null })}
        onConfirm={handleDelete}
        title="Delete Tag"
        description={`Are you sure you want to delete "${deleteModal.tag?.name}"? This will remove the tag from all posts. This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

