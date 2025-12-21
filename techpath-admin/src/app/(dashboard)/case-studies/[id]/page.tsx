'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { CaseStudyForm } from '@/components/forms/CaseStudyForm';
import { PageLoader } from '@/components/ui/Spinner';
import { caseStudiesService } from '@/services/case-studies.service';
import type { CaseStudyFormData } from '@/lib/validations';
import type { CaseStudy } from '@/types/api';

export default function EditCaseStudyPage() {
  const router = useRouter();
  const params = useParams();
  const [caseStudy, setCaseStudy] = useState<CaseStudy | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Use slug from URL (param is named 'id' but contains slug)
  const caseStudySlug = params.id as string;

  useEffect(() => {
    async function fetchCaseStudy() {
      try {
        const data = await caseStudiesService.getBySlug(caseStudySlug);
        setCaseStudy(data);
      } catch (error) {
        console.error('Error fetching case study:', error);
        toast.error('Case study not found');
        router.push('/case-studies');
      } finally {
        setLoading(false);
      }
    }

    if (caseStudySlug) {
      fetchCaseStudy();
    }
  }, [caseStudySlug, router]);

  const handleSubmit = async (data: CaseStudyFormData) => {
    if (!caseStudy) return;
    setIsSubmitting(true);
    try {
      // Use caseStudy.id for update (backend uses ID for PUT)
      await caseStudiesService.update(caseStudy.id, {
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
      toast.success('Case study updated successfully');
      router.push('/case-studies');
    } catch (error) {
      console.error('Error updating case study:', error);
      toast.error('Failed to update case study');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <PageLoader />;
  }

  if (!caseStudy) {
    return null;
  }

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Case Studies', href: '/case-studies' },
          { label: caseStudy.title },
        ]}
      />
      <PageHeader
        title="Edit Case Study"
        description={`Editing "${caseStudy.title}"`}
      />
      <CaseStudyForm
        initialData={caseStudy}
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
}

