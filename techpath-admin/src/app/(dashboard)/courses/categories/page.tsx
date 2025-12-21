'use client';

import { useEffect, useState, useCallback } from 'react';
import { Plus, Pencil, Trash2, Folder, ChevronDown, ChevronRight, FolderOpen } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Switch } from '@/components/ui/Switch';
import { Spinner } from '@/components/ui/Spinner';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { FormField } from '@/components/ui/FormField';
import { courseService, type CourseCategoryCreate, type CourseCategoryUpdate } from '@/services/course.service';
import type { CourseCategory, CourseCategoryTree } from '@/types/api';
import { slugify } from '@/lib/utils/format';

interface CategoryNodeProps {
  category: CourseCategoryTree;
  level: number;
  onEdit: (category: CourseCategory) => void;
  onDelete: (category: CourseCategoryTree) => void;
  onAddSubcategory: (parentId: number) => void;
}

const CategoryNode: React.FC<CategoryNodeProps> = ({ category, level, onEdit, onDelete, onAddSubcategory }) => {
  const [isOpen, setIsOpen] = useState(true);

  const paddingLeft = (level * 20) + 16;

  return (
    <div className="border-b border-gray-100 last:border-b-0">
      <div
        className="flex items-center justify-between py-3 pr-4 hover:bg-gray-50 transition-colors"
        style={{ paddingLeft: `${paddingLeft}px` }}
      >
        <div className="flex items-center gap-2">
          {category.children.length > 0 ? (
            <button onClick={() => setIsOpen(!isOpen)} className="text-gray-500 hover:text-gray-700">
              {isOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
            </button>
          ) : (
            <span className="w-4 h-4 inline-block"></span>
          )}
          {category.is_active ? (
            <FolderOpen className="h-4 w-4 text-teal-500" />
          ) : (
            <Folder className="h-4 w-4 text-gray-400" />
          )}
          <div>
            <span className="font-medium text-gray-900">{category.name}</span>
            <span className="ml-2 text-sm text-gray-500">/{category.slug}</span>
            {category.course_count > 0 && (
              <span className="ml-3 px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                {category.course_count} courses
              </span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          {level < 1 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onAddSubcategory(category.id)}
              title="Add Subcategory"
            >
              <Plus className="h-4 w-4" />
            </Button>
          )}
          <Button variant="ghost" size="sm" onClick={() => onEdit(category)} title="Edit Category">
            <Pencil className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(category)}
            title="Delete Category"
            disabled={category.course_count > 0 || category.children.length > 0}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
      {isOpen && category.children.length > 0 && (
        <div className="pl-4">
          {category.children.map((child) => (
            <CategoryNode
              key={child.id}
              category={child}
              level={level + 1}
              onEdit={onEdit}
              onDelete={onDelete}
              onAddSubcategory={onAddSubcategory}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default function CourseCategoriesPage() {
  const [categories, setCategories] = useState<CourseCategoryTree[]>([]);
  const [flatCategories, setFlatCategories] = useState<CourseCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<CourseCategory | null>(null);
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; category: CourseCategoryTree | null }>({
    open: false,
    category: null,
  });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const [formData, setFormData] = useState<CourseCategoryCreate>({
    name: '',
    slug: '',
    description: '',
    icon: '',
    parent_id: null,
    display_order: 0,
    is_active: true,
  });

  const fetchCategories = useCallback(async () => {
    setLoading(true);
    try {
      const [treeData, listData] = await Promise.all([
        courseService.getCategoryTree(false),
        courseService.listCategories(false),
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
      icon: '',
      parent_id: parentId || null,
      display_order: 0,
      is_active: true,
    });
    setModalOpen(true);
  };

  const handleOpenEdit = (category: CourseCategory) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      slug: category.slug,
      description: category.description || '',
      icon: category.icon || '',
      parent_id: category.parent_id || null,
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
        await courseService.updateCategory(editingCategory.id, formData);
        toast.success('Category updated successfully');
      } else {
        await courseService.createCategory(formData);
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
      await courseService.deleteCategory(deleteModal.category.id);
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

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Courses', href: '/courses' },
          { label: 'Categories' },
        ]}
      />
      <PageHeader
        title="Course Categories"
        description="Organize your courses into categories"
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
          <Folder className="h-12 w-12 text-gray-400 mb-4" />
          <p className="text-gray-500">No categories found</p>
          <Button className="mt-4" onClick={() => handleOpenCreate()}>
            <Plus className="mr-2 h-4 w-4" />
            Create First Category
          </Button>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          {categories.map((category) => (
            <CategoryNode
              key={category.id}
              category={category}
              level={0}
              onEdit={handleOpenEdit}
              onDelete={(cat) => setDeleteModal({ open: true, category: cat })}
              onAddSubcategory={handleOpenCreate}
            />
          ))}
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
              placeholder="e.g., Data Science"
              required
            />
          </FormField>

          <FormField label="Slug" htmlFor="slug" description="URL-friendly name">
            <Input
              id="slug"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              placeholder="e.g., data-science"
              pattern="^[a-z0-9-]+$"
              required
            />
          </FormField>

          <FormField label="Description" htmlFor="description">
            <Textarea
              id="description"
              value={formData.description || ''}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Brief description of the category"
              rows={2}
            />
          </FormField>

          <FormField label="Icon" htmlFor="icon" description="Icon name (e.g., chart-bar, cloud, brain)">
            <Input
              id="icon"
              value={formData.icon || ''}
              onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
              placeholder="e.g., chart-bar"
            />
          </FormField>

          <FormField label="Parent Category" htmlFor="parent_id" description="Leave empty for a root category">
            <select
              id="parent_id"
              value={formData.parent_id || ''}
              onChange={(e) => setFormData({ ...formData, parent_id: e.target.value ? Number(e.target.value) : null })}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm"
            >
              <option value="">No Parent (Root Category)</option>
              {flatCategories
                .filter(cat => !editingCategory || cat.id !== editingCategory.id)
                .map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
            </select>
          </FormField>

          <FormField label="Display Order" htmlFor="display_order" description="Lower numbers appear first">
            <Input
              id="display_order"
              type="number"
              value={formData.display_order}
              onChange={(e) => setFormData({ ...formData, display_order: Number(e.target.value) })}
            />
          </FormField>

          <Switch
            checked={formData.is_active ?? true}
            onChange={(checked) => setFormData({ ...formData, is_active: checked })}
            label="Active"
            description="Inactive categories won't show on the frontend"
          />

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" loading={saving}>
              {editingCategory ? 'Update Category' : 'Create Category'}
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
        description={
          deleteModal.category?.course_count && deleteModal.category.course_count > 0
            ? `Cannot delete "${deleteModal.category.name}". It has ${deleteModal.category.course_count} associated courses. Please reassign or delete courses first.`
            : deleteModal.category?.children && deleteModal.category.children.length > 0
            ? `Cannot delete "${deleteModal.category.name}". It has ${deleteModal.category.children.length} subcategories. Please delete subcategories first.`
            : `Are you sure you want to delete "${deleteModal.category?.name}"? This action cannot be undone.`
        }
        confirmText="Delete"
        variant="danger"
        loading={deleting}
        disabled={(deleteModal.category?.course_count ?? 0) > 0 || (deleteModal.category?.children?.length ?? 0) > 0}
      />
    </div>
  );
}

