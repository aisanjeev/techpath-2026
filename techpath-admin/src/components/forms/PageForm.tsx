'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { pageSchema, type PageFormData } from '@/lib/validations';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { FormField } from '@/components/ui/FormField';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { MarkdownEditor } from '@/components/editors/MarkdownEditor';
import { RichTextEditor } from '@/components/editors/RichTextEditor';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { FileText, Code2 } from 'lucide-react';
import { slugify } from '@/lib/utils/format';
import type { Page } from '@/types/api';

interface PageFormProps {
  initialData?: Page;
  onSubmit: (data: PageFormData) => Promise<void>;
  isLoading?: boolean;
}

function utcToLocalDatetimeInput(utcStr: string | null | undefined): string {
  if (!utcStr) return '';
  const d = new Date(utcStr);
  if (isNaN(d.getTime())) return '';
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function PageForm({ initialData, onSubmit, isLoading }: PageFormProps) {
  const [editorType, setEditorType] = useState<'markdown' | 'richtext'>(
    initialData?.content_type === 'markdown' ? 'markdown' : 'richtext'
  );

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<PageFormData>({
    resolver: zodResolver(pageSchema),
    defaultValues: {
      title: initialData?.title || '',
      slug: initialData?.slug || '',
      content: initialData?.content || '',
      content_type: initialData?.content_type || 'html',
      excerpt: initialData?.excerpt || '',
      featured_image: initialData?.featured_image || '',
      status: initialData?.status || 'draft',
      meta_title: initialData?.meta_title || '',
      meta_description: initialData?.meta_description || '',
      published_at: utcToLocalDatetimeInput(initialData?.published_at),
    },
  });

  const content = watch('content');
  const featuredImage = watch('featured_image');
  const slug = watch('slug');

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = e.target.value;
    setValue('title', newTitle);
    if (!initialData) {
      setValue('slug', slugify(newTitle));
    }
  };

  const handleFormSubmit = async (data: PageFormData) => {
    let published_at = data.published_at;
    if (published_at) {
      // datetime-local gives local time; convert to UTC ISO string for backend
      published_at = new Date(published_at).toISOString();
    }
    await onSubmit({
      ...data,
      published_at,
      content_type: editorType === 'markdown' ? 'markdown' : 'html',
    });
  };

  const previewUrl =
    slug && !errors.slug
      ? `/${slug}`
      : '';

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Page Details</CardTitle>
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
                  placeholder="Enter page title..."
                />
              </FormField>

              <FormField
                label="Slug"
                htmlFor="slug"
                error={errors.slug?.message}
                description={
                  previewUrl
                    ? `Will be available at: ${previewUrl}`
                    : 'URL path the page will be served at (e.g. our-story)'
                }
              >
                <Input
                  id="slug"
                  {...register('slug')}
                  error={!!errors.slug}
                  placeholder="page-url-slug"
                />
              </FormField>

              <FormField
                label="Excerpt"
                htmlFor="excerpt"
                error={errors.excerpt?.message}
                description="Short summary for previews and social cards (max 500 chars)"
              >
                <Textarea
                  id="excerpt"
                  {...register('excerpt')}
                  error={!!errors.excerpt}
                  placeholder="A brief summary of this page..."
                  rows={3}
                />
              </FormField>

              <FormField
                label="Content"
                htmlFor="content"
                error={errors.content?.message}
                required
              >
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

                {editorType === 'markdown' && (
                  <MarkdownEditor
                    content={content}
                    onChange={(c) => setValue('content', c)}
                    error={!!errors.content}
                    placeholder="# Page Heading

Write your page content here using **Markdown** syntax..."
                    minHeight="450px"
                  />
                )}

                {editorType === 'richtext' && (
                  <RichTextEditor
                    content={content}
                    onChange={(c) => setValue('content', c)}
                    error={!!errors.content}
                    placeholder="Write your page content..."
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

              <FormField
                label="Publish date"
                htmlFor="published_at"
                error={errors.published_at?.message}
                description="Leave blank to publish immediately. Future dates delay visibility."
              >
                <Input
                  id="published_at"
                  type="datetime-local"
                  {...register('published_at')}
                  error={!!errors.published_at}
                />
              </FormField>
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
                folder="pages"
                error={!!errors.featured_image}
                placeholder="Upload featured image"
              />
              {errors.featured_image?.message && (
                <p className="mt-1 text-sm text-red-500">{errors.featured_image.message}</p>
              )}
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
                {initialData ? 'Update Page' : 'Create Page'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </form>
  );
}
