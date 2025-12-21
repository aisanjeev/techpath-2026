'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { CaseStudyForm } from '@/components/forms/CaseStudyForm';
import { caseStudiesService } from '@/services/case-studies.service';
import type { CaseStudyFormData } from '@/lib/validations';

export default function CreateCaseStudyPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: CaseStudyFormData) => {
    setIsLoading(true);
    try {
      await caseStudiesService.create({
        title: data.title,
        slug: data.slug,
        client_name: data.client_name,
        industry: data.industry,
        challenge: data.challenge,
        solution: data.solution,
        results: data.results,
        content: data.content || undefined,
        excerpt: data.excerpt || undefined,
        featured_image: data.featured_image || undefined,
        stat_value: data.stat_value || undefined,
        stat_label: data.stat_label || undefined,
        testimonial_quote: data.testimonial_quote || undefined,
        testimonial_author: data.testimonial_author || undefined,
        testimonial_role: data.testimonial_role || undefined,
        status: data.status,
        featured: data.featured,
        meta_title: data.meta_title || undefined,
        meta_description: data.meta_description || undefined,
        published_at: data.published_at || undefined,
        tag_ids: data.tag_ids,
      });
      toast.success('Case study created successfully');
      router.push('/case-studies');
    } catch (error) {
      console.error('Error creating case study:', error);
      toast.error('Failed to create case study');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Case Studies', href: '/case-studies' },
          { label: 'Create Case Study' },
        ]}
      />
      <PageHeader
        title="Create Case Study"
        description="Share a new success story"
      />
      <CaseStudyForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}

