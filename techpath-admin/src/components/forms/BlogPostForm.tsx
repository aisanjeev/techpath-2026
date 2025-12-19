'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { blogPostSchema, type BlogPostFormData } from '@/lib/validations';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Switch } from '@/components/ui/Switch';
import { FormField } from '@/components/ui/FormField';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { MarkdownEditor } from '@/components/editors/MarkdownEditor';
import { RichTextEditor } from '@/components/editors/RichTextEditor';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { FileText, Code2, Plus } from 'lucide-react';
import Link from 'next/link';
import { slugify, calculateReadingTime } from '@/lib/utils/format';
import { blogService } from '@/services/blog.service';
import { categoryService, type BlogCategoryTree } from '@/services/category.service';
import type { BlogPost, BlogTag } from '@/types/api';

interface BlogPostFormProps {
  initialData?: BlogPost;
  onSubmit: (data: BlogPostFormData) => Promise<void>;
  isLoading?: boolean;
}

export function BlogPostForm({ initialData, onSubmit, isLoading }: BlogPostFormProps) {
  const [tags, setTags] = useState<BlogTag[]>([]);
  const [categories, setCategories] = useState<BlogCategoryTree[]>([]);
  const [flatCategories, setFlatCategories] = useState<Array<{ id: number; name: string; level: number }>>([]);
  const [selectedTags, setSelectedTags] = useState<number[]>(
    initialData?.tags.map((t) => t.id) || []
  );
  const [editorType, setEditorType] = useState<'markdown' | 'richtext'>('markdown');

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<BlogPostFormData>({
    resolver: zodResolver(blogPostSchema),
    defaultValues: {
      title: initialData?.title || '',
      slug: initialData?.slug || '',
      category_id: initialData?.category_id || 0,
      content: initialData?.content || '',
      content_type: initialData?.content_type || 'markdown',
      excerpt: initialData?.excerpt || '',
      featured_image: initialData?.featured_image || '',
      status: initialData?.status || 'draft',
      featured: initialData?.featured ?? false,
      reading_time: initialData?.reading_time || undefined,
      meta_title: initialData?.meta_title || '',
      meta_description: initialData?.meta_description || '',
      published_at: initialData?.published_at || '',
      tag_ids: initialData?.tags.map((t) => t.id) || [],
    },
  });

  const title = watch('title');
  const content = watch('content');
  const status = watch('status');
  const isFeatured = watch('featured');
  const featuredImage = watch('featured_image');
  const categoryId = watch('category_id');

  const readingTime = content ? calculateReadingTime(content) : 0;

  useEffect(() => {
    async function fetchData() {
      try {
        const [tagsData, categoriesData] = await Promise.all([
          blogService.listTags(),
          categoryService.getTree(true),
        ]);
        setTags(tagsData);
        setCategories(categoriesData);
        
        // Flatten categories for select dropdown
        const flattened = categoryService.flattenTree(categoriesData);
        setFlatCategories(flattened.map((c) => ({ id: c.id, name: c.fullPath, level: c.level })));
        
        // Set default category if creating new post and categories exist
        if (!initialData && categoriesData.length > 0) {
          // Find "Uncategorized" or use first category
          const uncategorized = flattened.find((c) => c.slug === 'uncategorized');
          setValue('category_id', uncategorized?.id || flattened[0].id);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    fetchData();
  }, [initialData, setValue]);

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = e.target.value;
    setValue('title', newTitle);
    if (!initialData) {
      setValue('slug', slugify(newTitle));
    }
  };

  const handleTagToggle = (tagId: number) => {
    const newTags = selectedTags.includes(tagId)
      ? selectedTags.filter((id) => id !== tagId)
      : [...selectedTags, tagId];
    setSelectedTags(newTags);
    setValue('tag_ids', newTags);
  };

  const handleFormSubmit = async (data: BlogPostFormData) => {
    await onSubmit({
      ...data,
      content_type: editorType === 'markdown' ? 'markdown' : 'html',
      tag_ids: selectedTags,
    });
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Post Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="Title"
                htmlFor="title"
                error={errors.title?.message}
                required
              >
                <Input
                  id="title"
                  {...register('title')}
                  onChange={handleTitleChange}
                  error={!!errors.title}
                  placeholder="Enter post title..."
                />
              </FormField>

              <FormField
                label="Slug"
                htmlFor="slug"
                error={errors.slug?.message}
                description="URL-friendly version of the title"
              >
                <Input
                  id="slug"
                  {...register('slug')}
                  error={!!errors.slug}
                  placeholder="post-url-slug"
                />
              </FormField>

              <FormField
                label="Category"
                htmlFor="category_id"
                error={errors.category_id?.message}
                required
              >
                <Select
                  id="category_id"
                  value={categoryId?.toString() || ''}
                  onChange={(e) => setValue('category_id', parseInt(e.target.value))}
                  error={!!errors.category_id}
                >
                  <option value="">Select a category</option>
                  {flatCategories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </Select>
              </FormField>

              <FormField
                label="Excerpt"
                htmlFor="excerpt"
                error={errors.excerpt?.message}
                description="Brief summary for previews (max 500 characters)"
              >
                <Textarea
                  id="excerpt"
                  {...register('excerpt')}
                  error={!!errors.excerpt}
                  placeholder="A brief summary of your post..."
                  rows={3}
                />
              </FormField>

              <FormField
                label="Content"
                htmlFor="content"
                error={errors.content?.message}
                required
              >
                {/* Editor Type Toggle */}
                <div className="mb-3 flex items-center justify-between">
                  <span className="text-sm text-gray-500">
                    {editorType === 'markdown' ? 'Markdown mode' : 'Rich Text mode'}
                  </span>
                  <div className="flex items-center gap-1 rounded-lg bg-gray-100 p-1">
                    <button
                      type="button"
                      onClick={() => setEditorType('markdown')}
                      className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                        editorType === 'markdown'
                          ? 'bg-white text-gray-900 shadow-sm'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <Code2 className="h-4 w-4" />
                      Markdown
                    </button>
                    <button
                      type="button"
                      onClick={() => setEditorType('richtext')}
                      className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                        editorType === 'richtext'
                          ? 'bg-white text-gray-900 shadow-sm'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      <FileText className="h-4 w-4" />
                      Rich Text
                    </button>
                  </div>
                </div>

                {/* Markdown Editor */}
                {editorType === 'markdown' && (
                  <MarkdownEditor
                    content={content}
                    onChange={(c) => setValue('content', c)}
                    error={!!errors.content}
                    placeholder="# Your Blog Post Title

Write your content here using **Markdown** syntax...

## Introduction
Start with an engaging introduction.

## Main Content
- Point one
- Point two

```javascript
const hello = 'world';
```"
                    minHeight="450px"
                  />
                )}

                {/* Rich Text Editor */}
                {editorType === 'richtext' && (
                  <RichTextEditor
                    content={content}
                    onChange={(c) => setValue('content', c)}
                    error={!!errors.content}
                    placeholder="Write your blog post content..."
                    className="min-h-[450px]"
                  />
                )}
              </FormField>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Publish Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="Status"
                htmlFor="status"
                error={errors.status?.message}
              >
                <Select
                  id="status"
                  {...register('status')}
                  error={!!errors.status}
                >
                  <option value="draft">Draft</option>
                  <option value="published">Published</option>
                  <option value="archived">Archived</option>
                </Select>
              </FormField>

              <Switch
                checked={isFeatured}
                onChange={(checked) => setValue('featured', checked)}
                label="Featured Post"
              />

              <div className="rounded-lg bg-gray-50 p-3">
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Reading time:</span>{' '}
                  {readingTime} min read
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Featured Image</CardTitle>
            </CardHeader>
            <CardContent>
              <ImageUpload
                value={featuredImage}
                onChange={(url) => setValue('featured_image', url)}
                folder="blog"
                error={!!errors.featured_image}
                placeholder="Upload featured image"
              />
              {errors.featured_image?.message && (
                <p className="mt-1 text-sm text-red-500">{errors.featured_image.message}</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle>Tags</CardTitle>
              <Link href="/blog/tags" className="text-xs text-teal-600 hover:text-teal-700">
                <Plus className="inline h-3 w-3" /> Manage Tags
              </Link>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {tags.map((tag) => (
                  <button
                    key={tag.id}
                    type="button"
                    onClick={() => handleTagToggle(tag.id)}
                    className={`rounded-full px-3 py-1 text-sm transition-colors ${
                      selectedTags.includes(tag.id)
                        ? 'bg-teal-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {tag.name}
                  </button>
                ))}
                {tags.length === 0 && (
                  <div className="text-center py-2">
                    <p className="text-sm text-gray-500">No tags available</p>
                    <Link href="/blog/tags" className="text-xs text-teal-600 hover:underline">
                      Create your first tag →
                    </Link>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>SEO Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="Meta Title"
                htmlFor="meta_title"
                error={errors.meta_title?.message}
                description="Max 70 characters"
              >
                <Input
                  id="meta_title"
                  {...register('meta_title')}
                  error={!!errors.meta_title}
                  placeholder="SEO title for search engines"
                />
              </FormField>

              <FormField
                label="Meta Description"
                htmlFor="meta_description"
                error={errors.meta_description?.message}
                description="Max 160 characters"
              >
                <Textarea
                  id="meta_description"
                  {...register('meta_description')}
                  error={!!errors.meta_description}
                  placeholder="SEO description for search engines"
                  rows={3}
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Button type="submit" className="w-full" loading={isLoading}>
                {initialData ? 'Update Post' : 'Create Post'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </form>
  );
}
