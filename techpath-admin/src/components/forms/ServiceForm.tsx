'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { serviceSchema, type ServiceFormData } from '@/lib/validations';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Switch } from '@/components/ui/Switch';
import { FormField } from '@/components/ui/FormField';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { RichTextEditor } from '@/components/editors/RichTextEditor';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { slugify } from '@/lib/utils/format';
import type { Service } from '@/types/api';

interface ServiceFormProps {
  initialData?: Service;
  onSubmit: (data: ServiceFormData) => Promise<void>;
  isLoading?: boolean;
}

export function ServiceForm({ initialData, onSubmit, isLoading }: ServiceFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<ServiceFormData>({
    resolver: zodResolver(serviceSchema),
    defaultValues: {
      title: initialData?.title || '',
      slug: initialData?.slug || '',
      description: initialData?.description || '',
      short_description: initialData?.short_description || '',
      icon: initialData?.icon || '',
      image_url: initialData?.image_url || '',
      features: initialData?.features || [],
      price: initialData?.price || '',
      cta_text: initialData?.cta_text || '',
      cta_url: initialData?.cta_url || '',
      featured: initialData?.featured ?? false,
      display_order: initialData?.display_order ?? 0,
      is_active: initialData?.is_active ?? true,
    },
  });

  const title = watch('title');
  const description = watch('description');
  const isActive = watch('is_active');
  const isFeatured = watch('featured');
  const imageUrl = watch('image_url');

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
                  placeholder="e.g., AI Consulting Services"
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
                  placeholder="ai-consulting-services"
                />
              </FormField>

              <FormField
                label="Short Description"
                htmlFor="short_description"
                error={errors.short_description?.message}
                description="Brief summary (max 500 characters)"
              >
                <Textarea
                  id="short_description"
                  {...register('short_description')}
                  error={!!errors.short_description}
                  placeholder="A brief overview of the service..."
                  rows={3}
                />
              </FormField>

              <FormField
                label="Description"
                htmlFor="description"
                error={errors.description?.message}
                required
              >
                <RichTextEditor
                  content={description}
                  onChange={(content) => setValue('description', content)}
                  error={!!errors.description}
                  placeholder="Detailed description of your service..."
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Media & Appearance</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="Icon"
                htmlFor="icon"
                error={errors.icon?.message}
                description="Icon name or emoji"
              >
                <Input
                  id="icon"
                  {...register('icon')}
                  error={!!errors.icon}
                  placeholder="e.g., 🤖 or icon-name"
                />
              </FormField>

              <FormField
                label="Service Image"
                htmlFor="image_url"
                error={errors.image_url?.message}
              >
                <ImageUpload
                  value={imageUrl}
                  onChange={(url) => setValue('image_url', url)}
                  folder="services"
                  error={!!errors.image_url}
                  placeholder="Upload service image"
                />
              </FormField>

              <FormField
                label="Price"
                htmlFor="price"
                error={errors.price?.message}
              >
                <Input
                  id="price"
                  {...register('price')}
                  error={!!errors.price}
                  placeholder="e.g., Starting at $999"
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Call to Action</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="CTA Text"
                htmlFor="cta_text"
                error={errors.cta_text?.message}
              >
                <Input
                  id="cta_text"
                  {...register('cta_text')}
                  error={!!errors.cta_text}
                  placeholder="e.g., Get Started"
                />
              </FormField>

              <FormField
                label="CTA URL"
                htmlFor="cta_url"
                error={errors.cta_url?.message}
              >
                <Input
                  id="cta_url"
                  {...register('cta_url')}
                  error={!!errors.cta_url}
                  placeholder="https://example.com/contact"
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
              <Switch
                checked={isActive}
                onChange={(checked) => setValue('is_active', checked)}
                label="Active"
              />

              <Switch
                checked={isFeatured}
                onChange={(checked) => setValue('featured', checked)}
                label="Featured"
              />

              <FormField
                label="Display Order"
                htmlFor="display_order"
                error={errors.display_order?.message}
              >
                <Input
                  id="display_order"
                  type="number"
                  {...register('display_order', { valueAsNumber: true })}
                  error={!!errors.display_order}
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Button type="submit" className="w-full" loading={isLoading}>
                {initialData ? 'Update Service' : 'Create Service'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </form>
  );
}

