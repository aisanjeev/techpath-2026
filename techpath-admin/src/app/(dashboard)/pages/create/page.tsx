'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { PageForm } from '@/components/forms/PageForm';
import { pagesService } from '@/services/pages.service';
import type { PageFormData } from '@/lib/validations';

export default function CreatePagePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: PageFormData) => {
    setIsLoading(true);
    try {
      await pagesService.create({
        title: data.title,
        slug: data.slug,
        content: data.content,
        content_type: data.content_type,
        excerpt: data.excerpt || undefined,
        featured_image: data.featured_image || undefined,
        status: data.status,
        meta_title: data.meta_title || undefined,
        meta_description: data.meta_description || undefined,
        published_at: data.published_at || undefined,
      });
      toast.success('Page created successfully');
      router.push('/pages');
    } catch (error) {
      console.error('Error creating page:', error);
      toast.error('Failed to create page');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Pages', href: '/pages' },
          { label: 'Create Page' },
        ]}
      />
      <PageHeader
        title="Create Page"
        description="Publish a new standalone page"
      />
      <PageForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}
