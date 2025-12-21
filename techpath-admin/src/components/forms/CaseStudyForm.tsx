'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { FileText, Code2 } from 'lucide-react';
import { caseStudySchema, type CaseStudyFormData } from '@/lib/validations';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Switch } from '@/components/ui/Switch';
import { FormField } from '@/components/ui/FormField';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { RichTextEditor } from '@/components/editors/RichTextEditor';
import { MarkdownEditor } from '@/components/editors/MarkdownEditor';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { slugify } from '@/lib/utils/format';
import type { CaseStudy } from '@/types/api';

interface CaseStudyFormProps {
  initialData?: CaseStudy;
  onSubmit: (data: CaseStudyFormData) => Promise<void>;
  isLoading?: boolean;
}

export function CaseStudyForm({ initialData, onSubmit, isLoading }: CaseStudyFormProps) {
  const [editorType, setEditorType] = useState<'markdown' | 'richtext'>('markdown');

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<CaseStudyFormData>({
    resolver: zodResolver(caseStudySchema),
    defaultValues: {
      title: initialData?.title || '',
      slug: initialData?.slug || '',
      client_name: initialData?.client_name || '',
      industry: initialData?.industry || '',
      challenge: initialData?.challenge || '',
      solution: initialData?.solution || '',
      results: initialData?.results || '',
      content: initialData?.content || '',
      excerpt: initialData?.excerpt || '',
      featured_image: initialData?.featured_image || '',
      stat_value: initialData?.stat_value || '',
      stat_label: initialData?.stat_label || '',
      testimonial_quote: initialData?.testimonial_quote || '',
      testimonial_author: initialData?.testimonial_author || '',
      testimonial_role: initialData?.testimonial_role || '',
      status: initialData?.status || 'draft',
      featured: initialData?.featured ?? false,
      meta_title: initialData?.meta_title || '',
      meta_description: initialData?.meta_description || '',
      published_at: initialData?.published_at || '',
    },
  });

  const title = watch('title');
  const challenge = watch('challenge');
  const solution = watch('solution');
  const results = watch('results');
  const status = watch('status');
  const isFeatured = watch('featured');
  const featuredImage = watch('featured_image');

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = e.target.value;
    setValue('title', newTitle);
    if (!initialData) {
      setValue('slug', slugify(newTitle));
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
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
                  placeholder="e.g., How TechCorp Increased Revenue by 40%"
                />
              </FormField>

              <FormField
                label="Slug"
                htmlFor="slug"
                error={errors.slug?.message}
              >
                <Input
                  id="slug"
                  {...register('slug')}
                  error={!!errors.slug}
                  placeholder="techcorp-revenue-increase"
                />
              </FormField>

              <div className="grid gap-4 sm:grid-cols-2">
                <FormField
                  label="Client Name"
                  htmlFor="client_name"
                  error={errors.client_name?.message}
                  required
                >
                  <Input
                    id="client_name"
                    {...register('client_name')}
                    error={!!errors.client_name}
                    placeholder="TechCorp Inc."
                  />
                </FormField>

                <FormField
                  label="Industry"
                  htmlFor="industry"
                  error={errors.industry?.message}
                  required
                >
                  <Input
                    id="industry"
                    {...register('industry')}
                    error={!!errors.industry}
                    placeholder="e.g., Financial Services"
                  />
                </FormField>
              </div>

              <FormField
                label="Excerpt"
                htmlFor="excerpt"
                error={errors.excerpt?.message}
                description="Brief summary for previews"
              >
                <Textarea
                  id="excerpt"
                  {...register('excerpt')}
                  error={!!errors.excerpt}
                  placeholder="A brief summary of the case study..."
                  rows={2}
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Case Study Content</CardTitle>
                {/* Editor Type Toggle */}
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
            </CardHeader>
            <CardContent className="space-y-6">
              <FormField
                label="Challenge"
                htmlFor="challenge"
                error={errors.challenge?.message}
                required
              >
                {editorType === 'markdown' ? (
                  <MarkdownEditor
                    content={challenge}
                    onChange={(c) => setValue('challenge', c)}
                    error={!!errors.challenge}
                    placeholder="## The Challenge

Describe the client's challenge here...

- Key pain point 1
- Key pain point 2"
                    minHeight="200px"
                  />
                ) : (
                  <RichTextEditor
                    content={challenge}
                    onChange={(c) => setValue('challenge', c)}
                    error={!!errors.challenge}
                    placeholder="Describe the client's challenge..."
                  />
                )}
              </FormField>

              <FormField
                label="Solution"
                htmlFor="solution"
                error={errors.solution?.message}
                required
              >
                {editorType === 'markdown' ? (
                  <MarkdownEditor
                    content={solution}
                    onChange={(c) => setValue('solution', c)}
                    error={!!errors.solution}
                    placeholder="## Our Solution

Describe the solution provided...

1. Step one
2. Step two
3. Step three"
                    minHeight="200px"
                  />
                ) : (
                  <RichTextEditor
                    content={solution}
                    onChange={(c) => setValue('solution', c)}
                    error={!!errors.solution}
                    placeholder="Describe the solution provided..."
                  />
                )}
              </FormField>

              <FormField
                label="Results"
                htmlFor="results"
                error={errors.results?.message}
                required
              >
                {editorType === 'markdown' ? (
                  <MarkdownEditor
                    content={results}
                    onChange={(c) => setValue('results', c)}
                    error={!!errors.results}
                    placeholder="## Results Achieved

Describe the results achieved...

- **40%** increase in revenue
- **50%** reduction in costs
- **99.9%** uptime achieved"
                    minHeight="200px"
                  />
                ) : (
                  <RichTextEditor
                    content={results}
                    onChange={(c) => setValue('results', c)}
                    error={!!errors.results}
                    placeholder="Describe the results achieved..."
                  />
                )}
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Statistics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <FormField
                  label="Stat Value"
                  htmlFor="stat_value"
                  error={errors.stat_value?.message}
                  description="e.g., 40%"
                >
                  <Input
                    id="stat_value"
                    {...register('stat_value')}
                    error={!!errors.stat_value}
                    placeholder="40%"
                  />
                </FormField>

                <FormField
                  label="Stat Label"
                  htmlFor="stat_label"
                  error={errors.stat_label?.message}
                  description="e.g., Revenue Increase"
                >
                  <Input
                    id="stat_label"
                    {...register('stat_label')}
                    error={!!errors.stat_label}
                    placeholder="Revenue Increase"
                  />
                </FormField>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Testimonial</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="Quote"
                htmlFor="testimonial_quote"
                error={errors.testimonial_quote?.message}
              >
                <Textarea
                  id="testimonial_quote"
                  {...register('testimonial_quote')}
                  error={!!errors.testimonial_quote}
                  placeholder="Client testimonial quote..."
                  rows={3}
                />
              </FormField>

              <div className="grid gap-4 sm:grid-cols-2">
                <FormField
                  label="Author"
                  htmlFor="testimonial_author"
                  error={errors.testimonial_author?.message}
                >
                  <Input
                    id="testimonial_author"
                    {...register('testimonial_author')}
                    error={!!errors.testimonial_author}
                    placeholder="John Smith"
                  />
                </FormField>

                <FormField
                  label="Role"
                  htmlFor="testimonial_role"
                  error={errors.testimonial_role?.message}
                >
                  <Input
                    id="testimonial_role"
                    {...register('testimonial_role')}
                    error={!!errors.testimonial_role}
                    placeholder="CEO, TechCorp Inc."
                  />
                </FormField>
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
                label="Featured Case Study"
              />
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
                folder="case-studies"
                error={!!errors.featured_image}
                placeholder="Upload featured image"
              />
              {errors.featured_image?.message && (
                <p className="mt-1 text-sm text-red-500">{errors.featured_image.message}</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Button type="submit" className="w-full" loading={isLoading}>
                {initialData ? 'Update Case Study' : 'Create Case Study'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </form>
  );
}

