'use client';

import { useEffect, useState, useCallback } from 'react';
import { Plus, Pencil, Trash2, ChevronRight, FolderTree } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Switch } from '@/components/ui/Switch';
import { Spinner } from '@/components/ui/Spinner';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { FormField } from '@/components/ui/FormField';
import { categoryService, type BlogCategory, type BlogCategoryTree } from '@/services/category.service';
import { slugify } from '@/lib/utils/format';
import { cn } from '@/lib/utils/cn';

export default function CategoriesPage() {
  const [categories, setCategories] = useState<BlogCategoryTree[]>([]);
  const [flatCategories, setFlatCategories] = useState<BlogCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<BlogCategory | null>(null);
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; category: BlogCategory | null }>({
    open: false,
    category: null,
  });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    description: '',
    parent_id: null as number | null,
    display_order: 0,
    is_active: true,
  });

  const fetchCategories = useCallback(async () => {
    setLoading(true);
    try {
      const [treeData, listData] = await Promise.all([
        categoryService.getTree(false),
        categoryService.list(false),
      ]);
      setCategories(treeData);
      setFlatCategories(listData);
    } catch (error) {
      console.error('Error fetching categories:', error);
      toast.error('Failed to load categories');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  const handleOpenCreate = (parentId?: number) => {
    setEditingCategory(null);
    setFormData({
      name: '',
      slug: '',
      description: '',
      parent_id: parentId || null,
      display_order: 0,
      is_active: true,
    });
    setModalOpen(true);
  };

  const handleOpenEdit = (category: BlogCategory) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      slug: category.slug,
      description: category.description || '',
      parent_id: category.parent_id,
      display_order: category.display_order,
      is_active: category.is_active,
    });
    setModalOpen(true);
  };

  const handleNameChange = (name: string) => {
    setFormData((prev) => ({
      ...prev,
      name,
      slug: !editingCategory ? slugify(name) : prev.slug,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      if (editingCategory) {
        await categoryService.update(editingCategory.id, formData);
        toast.success('Category updated successfully');
      } else {
        await categoryService.create(formData);
        toast.success('Category created successfully');
      }
      setModalOpen(false);
      fetchCategories();
    } catch (error: any) {
      console.error('Error saving category:', error);
      toast.error(error.message || 'Failed to save category');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteModal.category) return;
    setDeleting(true);

    try {
      await categoryService.delete(deleteModal.category.id);
      toast.success('Category deleted successfully');
      setDeleteModal({ open: false, category: null });
      fetchCategories();
    } catch (error: any) {
      console.error('Error deleting category:', error);
      toast.error(error.message || 'Failed to delete category');
    } finally {
      setDeleting(false);
    }
  };

  const renderCategoryItem = (category: BlogCategoryTree, level: number = 0) => {
    const hasChildren = category.children && category.children.length > 0;

    return (
      <div key={category.id}>
        <div
          className={cn(
            'flex items-center justify-between p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors',
            level > 0 && 'bg-gray-25'
          )}
          style={{ paddingLeft: `${12 + level * 24}px` }}
        >
          <div className="flex items-center gap-3">
            {level > 0 && (
              <ChevronRight className="h-4 w-4 text-gray-400" />
            )}
            <div>
              <div className="flex items-center gap-2">
                <span className="font-medium text-gray-900">{category.name}</span>
                {!category.is_active && (
                  <span className="text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded">
                    Inactive
                  </span>
                )}
              </div>
              <div className="text-sm text-gray-500">
                /{category.slug} • {category.post_count} posts
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {level < 2 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleOpenCreate(category.id)}
                title="Add subcategory"
              >
                <Plus className="h-4 w-4" />
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleOpenEdit(category)}
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setDeleteModal({ open: true, category })}
              disabled={category.post_count > 0 || category.slug === 'uncategorized'}
              title={
                category.slug === 'uncategorized'
                  ? 'Cannot delete default category'
                  : category.post_count > 0
                  ? 'Cannot delete category with posts'
                  : 'Delete'
              }
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
        {hasChildren &&
          category.children.map((child) => renderCategoryItem(child, level + 1))}
      </div>
    );
  };

  // Get available parent options (exclude self and descendants)
  const getParentOptions = () => {
    if (!editingCategory) {
      return flatCategories.filter((c) => c.parent_id === null || flatCategories.find((p) => p.id === c.parent_id)?.parent_id === null);
    }
    
    // When editing, exclude self and any descendants
    const excludeIds = new Set<number>([editingCategory.id]);
    const addDescendants = (parentId: number) => {
      flatCategories.forEach((c) => {
        if (c.parent_id === parentId) {
          excludeIds.add(c.id);
          addDescendants(c.id);
        }
      });
    };
    addDescendants(editingCategory.id);
    
    return flatCategories.filter((c) => !excludeIds.has(c.id) && (c.parent_id === null || flatCategories.find((p) => p.id === c.parent_id)?.parent_id === null));
  };

  return (
    <div>
      <PageHeader
        title="Blog Categories"
        description="Organize your blog posts into categories"
        actions={
          <Button onClick={() => handleOpenCreate()}>
            <Plus className="mr-2 h-4 w-4" />
            Add Category
          </Button>
        }
      />

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : categories.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center bg-white rounded-lg border border-gray-200">
          <FolderTree className="h-12 w-12 text-gray-400 mb-4" />
          <p className="text-gray-500">No categories found</p>
          <Button className="mt-4" onClick={() => handleOpenCreate()}>
            <Plus className="mr-2 h-4 w-4" />
            Create First Category
          </Button>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {categories.map((category) => renderCategoryItem(category))}
        </div>
      )}

      {/* Create/Edit Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingCategory ? 'Edit Category' : 'Create Category'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <FormField label="Name" htmlFor="name" required>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => handleNameChange(e.target.value)}
              placeholder="e.g., Technology"
              required
            />
          </FormField>

          <FormField label="Slug" htmlFor="slug" description="URL-friendly name">
            <Input
              id="slug"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              placeholder="e.g., technology"
              pattern="^[a-z0-9-]+$"
              required
            />
          </FormField>

          <FormField label="Description" htmlFor="description">
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Brief description of this category"
              rows={2}
            />
          </FormField>

          <FormField label="Parent Category" htmlFor="parent_id">
            <Select
              id="parent_id"
              value={formData.parent_id?.toString() || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  parent_id: e.target.value ? parseInt(e.target.value) : null,
                })
              }
            >
              <option value="">None (Root Category)</option>
              {getParentOptions().map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.parent_id ? `— ${cat.name}` : cat.name}
                </option>
              ))}
            </Select>
          </FormField>

          <FormField label="Display Order" htmlFor="display_order">
            <Input
              id="display_order"
              type="number"
              value={formData.display_order}
              onChange={(e) =>
                setFormData({ ...formData, display_order: parseInt(e.target.value) || 0 })
              }
              min={0}
            />
          </FormField>

          <Switch
            checked={formData.is_active}
            onChange={(checked) => setFormData({ ...formData, is_active: checked })}
            label="Active"
          />

          <div className="flex justify-end gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setModalOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit" loading={saving}>
              {editingCategory ? 'Update' : 'Create'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, category: null })}
        onConfirm={handleDelete}
        title="Delete Category"
        description={`Are you sure you want to delete "${deleteModal.category?.name}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

