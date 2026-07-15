'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { PageForm } from '@/components/forms/PageForm';
import { PageLoader } from '@/components/ui/Spinner';
import { pagesService } from '@/services/pages.service';
import type { PageFormData } from '@/lib/validations';
import type { Page } from '@/types/api';

export default function EditPagePage() {
  const router = useRouter();
  const params = useParams();
  const [page, setPage] = useState<Page | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Param named 'id' but carries the slug (mirrors blog/[id] pattern)
  const pageSlug = params.id as string;

  useEffect(() => {
    async function fetchPage() {
      try {
        const data = await pagesService.getBySlug(pageSlug);
        setPage(data);
      } catch (error) {
        console.error('Error fetching page:', error);
        toast.error('Page not found');
        router.push('/pages');
      } finally {
        setLoading(false);
      }
    }

    if (pageSlug) {
      fetchPage();
    }
  }, [pageSlug, router]);

  const handleSubmit = async (data: PageFormData) => {
    if (!page) return;
    setIsSubmitting(true);
    try {
      await pagesService.update(page.id, {
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
      toast.success('Page updated successfully');
      router.push('/pages');
    } catch (error) {
      console.error('Error updating page:', error);
      toast.error('Failed to update page');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <PageLoader />;
  }

  if (!page) {
    return null;
  }

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Pages', href: '/pages' },
          { label: page.title },
        ]}
      />
      <PageHeader
        title="Edit Page"
        description={`Editing "${page.title}"`}
      />
      <PageForm
        initialData={page}
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
}
