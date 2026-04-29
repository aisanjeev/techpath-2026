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
import { Select } from '@/components/ui/Select';
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
      pricing_plans: initialData?.pricing_plans || [],
      faqs: initialData?.faqs || [],
      price: initialData?.price || '',
      cta_text: initialData?.cta_text || '',
      cta_url: initialData?.cta_url || '',
      featured: initialData?.featured ?? false,
      display_order: initialData?.display_order ?? 0,
      is_active: initialData?.is_active ?? true,
      meta_title: initialData?.meta_title || '',
      meta_description: initialData?.meta_description || '',
      og_image: initialData?.og_image || '',
      canonical_url: initialData?.canonical_url || '',
      no_index: initialData?.no_index ?? false,
    },
  });

  const title = watch('title');
  const description = watch('description');
  const isActive = watch('is_active');
  const isFeatured = watch('featured');
  const imageUrl = watch('image_url');
  const features = watch('features') || [];
  const faqs = watch('faqs') || [];
  const pricingPlans = watch('pricing_plans') || [];
  const ogImage = watch('og_image');
  const noIndex = watch('no_index');

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
                description="Icon shown on the service card"
              >
                <Select id="icon" {...register('icon')} error={!!errors.icon}>
                  <option value="">Default</option>
                  <option value="brain">Brain (AI / ML)</option>
                  <option value="cloud">Cloud</option>
                  <option value="code">Code (Development)</option>
                  <option value="chart">Chart (Analytics)</option>
                  <option value="shield">Shield (Security)</option>
                  <option value="transform">Transform (Digital)</option>
                </Select>
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
            </CardContent>
          </Card>

          <FormField label="Feature bullets (on service card)" error={errors.features?.message}>
            <div className="space-y-2">
              {features.map((_, i) => (
                <div key={i} className="flex gap-2">
                  <Input
                    value={features[i] ?? ''}
                    onChange={(e) => {
                      const next = [...features];
                      next[i] = e.target.value;
                      setValue('features', next);
                    }}
                    placeholder={`Feature ${i + 1}`}
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setValue('features', features.filter((_, j) => j !== i))}
                  >
                    Remove
                  </Button>
                </div>
              ))}
              <Button
                type="button"
                variant="outline"
                onClick={() => setValue('features', [...features, ''])}
              >
                Add feature
              </Button>
            </div>
          </FormField>

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

          <Card>
            <CardHeader>
              <CardTitle>Pricing Plans</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {pricingPlans.map((_, i) => (
                <div key={i} className="space-y-2 rounded-lg border border-slate-700 bg-slate-950/50 p-4">
                  <div className="grid gap-3 md:grid-cols-2">
                    <FormField label={`Plan ${i + 1} Name`} htmlFor={`plan-name-${i}`}>
                      <Input
                        id={`plan-name-${i}`}
                        value={pricingPlans[i]?.name || ''}
                        onChange={(e) => {
                          const next = [...pricingPlans];
                          next[i] = { ...next[i], name: e.target.value };
                          setValue('pricing_plans', next);
                        }}
                        placeholder="e.g., Starter"
                      />
                    </FormField>
                    <FormField label="Price" htmlFor={`plan-price-${i}`}>
                      <Input
                        id={`plan-price-${i}`}
                        value={pricingPlans[i]?.price || ''}
                        onChange={(e) => {
                          const next = [...pricingPlans];
                          next[i] = { ...next[i], price: e.target.value };
                          setValue('pricing_plans', next);
                        }}
                        placeholder="e.g., $499"
                      />
                    </FormField>
                    <FormField label="Period" htmlFor={`plan-period-${i}`}>
                      <Input
                        id={`plan-period-${i}`}
                        value={pricingPlans[i]?.period || ''}
                        onChange={(e) => {
                          const next = [...pricingPlans];
                          next[i] = { ...next[i], period: e.target.value };
                          setValue('pricing_plans', next);
                        }}
                        placeholder="e.g., per month"
                      />
                    </FormField>
                    <FormField label="CTA Label" htmlFor={`plan-cta-${i}`}>
                      <Input
                        id={`plan-cta-${i}`}
                        value={pricingPlans[i]?.cta || ''}
                        onChange={(e) => {
                          const next = [...pricingPlans];
                          next[i] = { ...next[i], cta: e.target.value };
                          setValue('pricing_plans', next);
                        }}
                        placeholder="e.g., Get started"
                      />
                    </FormField>
                  </div>
                  <FormField label="Description" htmlFor={`plan-desc-${i}`}>
                    <Textarea
                      id={`plan-desc-${i}`}
                      value={pricingPlans[i]?.description || ''}
                      onChange={(e) => {
                        const next = [...pricingPlans];
                        next[i] = { ...next[i], description: e.target.value };
                        setValue('pricing_plans', next);
                      }}
                      placeholder="Short description of what's included"
                      rows={2}
                    />
                  </FormField>
                  <FormField label="Features (one per line)" htmlFor={`plan-feats-${i}`}>
                    <Textarea
                      id={`plan-feats-${i}`}
                      value={(pricingPlans[i]?.features || []).join('\n')}
                      onChange={(e) => {
                        const next = [...pricingPlans];
                        next[i] = {
                          ...next[i],
                          features: e.target.value
                            .split('\n')
                            .map((f) => f.trim())
                            .filter(Boolean),
                        };
                        setValue('pricing_plans', next);
                      }}
                      placeholder={'Feature one\nFeature two\nFeature three'}
                      rows={4}
                    />
                  </FormField>
                  <Switch
                    checked={!!pricingPlans[i]?.highlighted}
                    onChange={(checked) => {
                      const next = [...pricingPlans];
                      next[i] = { ...next[i], highlighted: checked };
                      setValue('pricing_plans', next);
                    }}
                    label="Highlighted plan"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => setValue('pricing_plans', pricingPlans.filter((_, j) => j !== i))}
                  >
                    Remove plan
                  </Button>
                </div>
              ))}
              <Button
                type="button"
                variant="outline"
                onClick={() =>
                  setValue('pricing_plans', [
                    ...pricingPlans,
                    { name: '', description: '', price: '', period: '', features: [], cta: '', highlighted: false },
                  ])
                }
              >
                Add pricing plan
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>FAQs</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {faqs.map((_, i) => (
                <div key={i} className="space-y-2 rounded-lg border border-slate-700 bg-slate-950/50 p-4">
                  <FormField
                    label={`Question ${i + 1}`}
                    htmlFor={`faq-question-${i}`}
                    error={errors.faqs?.[i]?.question?.message}
                  >
                    <Input
                      id={`faq-question-${i}`}
                      value={faqs[i]?.question || ''}
                      onChange={(e) => {
                        const next = [...faqs];
                        next[i] = { ...next[i], question: e.target.value, answer: next[i]?.answer || '' };
                        setValue('faqs', next);
                      }}
                      placeholder="e.g., How long does implementation take?"
                    />
                  </FormField>
                  <FormField
                    label="Answer"
                    htmlFor={`faq-answer-${i}`}
                    error={errors.faqs?.[i]?.answer?.message}
                  >
                    <Textarea
                      id={`faq-answer-${i}`}
                      value={faqs[i]?.answer || ''}
                      onChange={(e) => {
                        const next = [...faqs];
                        next[i] = { ...next[i], question: next[i]?.question || '', answer: e.target.value };
                        setValue('faqs', next);
                      }}
                      placeholder="Detailed answer..."
                      rows={3}
                    />
                  </FormField>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => setValue('faqs', faqs.filter((_, j) => j !== i))}
                  >
                    Remove FAQ
                  </Button>
                </div>
              ))}
              <Button
                type="button"
                variant="outline"
                onClick={() => setValue('faqs', [...faqs, { question: '', answer: '' }])}
              >
                Add FAQ
              </Button>
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
            <CardHeader>
              <CardTitle>SEO Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                label="Meta Title"
                htmlFor="meta_title"
                error={errors.meta_title?.message}
                description="Custom title for search engines (max 70 chars)"
              >
                <Input
                  id="meta_title"
                  {...register('meta_title')}
                  error={!!errors.meta_title}
                  placeholder="Leave blank to use service title"
                  maxLength={70}
                />
              </FormField>

              <FormField
                label="Meta Description"
                htmlFor="meta_description"
                error={errors.meta_description?.message}
                description="Search result description (max 160 chars)"
              >
                <Textarea
                  id="meta_description"
                  {...register('meta_description')}
                  error={!!errors.meta_description}
                  placeholder="Brief description for search results"
                  rows={3}
                  maxLength={160}
                />
              </FormField>

              <FormField
                label="OG Image"
                htmlFor="og_image"
                error={errors.og_image?.message}
                description="Image for social media sharing"
              >
                <ImageUpload
                  value={ogImage}
                  onChange={(url) => setValue('og_image', url)}
                  folder="services/og"
                  error={!!errors.og_image}
                  placeholder="Upload OG image (1200x630px recommended)"
                />
              </FormField>

              <FormField
                label="Canonical URL"
                htmlFor="canonical_url"
                error={errors.canonical_url?.message}
                description="Preferred URL if multiple versions exist"
              >
                <Input
                  id="canonical_url"
                  {...register('canonical_url')}
                  error={!!errors.canonical_url}
                  placeholder="https://example.com/services/..."
                />
              </FormField>

              <Switch
                checked={noIndex}
                onChange={(checked) => setValue('no_index', checked)}
                label="No Index (hide from search engines)"
              />
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

