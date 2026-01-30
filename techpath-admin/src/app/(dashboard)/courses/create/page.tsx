'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { CourseForm } from '@/components/forms/CourseForm';
import { courseService } from '@/services/course.service';
import type { CourseFormData } from '@/lib/validations';

export default function CreateCoursePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: CourseFormData) => {
    setIsLoading(true);
    try {
      const payload = {
        title: data.title,
        slug: data.slug,
        short_description: data.short_description || undefined,
        description: data.description,
        category_id: data.category_id,
        price: data.price,
        original_price: data.original_price || undefined,
        emi_available: data.emi_available,
        emi_amount: data.emi_amount || undefined,
        currency: data.currency || 'INR',
        duration: data.duration,
        duration_hours: data.duration_hours || undefined,
        batch_size: data.batch_size || 20,
        level: data.level,
        rating: data.rating || 0,
        review_count: data.review_count || 0,
        enrollment_count: data.enrollment_count || 0,
        placement_rate: data.placement_rate || undefined,
        featured_image: data.featured_image || undefined,
        video_url: data.video_url || undefined,
        instructor_name: data.instructor_name || undefined,
        instructor_title: data.instructor_title || undefined,
        instructor_bio: data.instructor_bio || undefined,
        instructor_image: data.instructor_image || undefined,
        certification_name: data.certification_name || undefined,
        certification_authority: data.certification_authority || undefined,
        meta_title: data.meta_title || undefined,
        meta_description: data.meta_description || undefined,
        next_batch_date: data.next_batch_date || undefined,
        status: data.status,
        featured: data.featured,
        is_active: data.is_active,
        skill_ids: data.skill_ids,
        learning_outcomes: data.learning_outcomes,
        prerequisites: data.prerequisites,
        curriculum: data.curriculum ?? [],
        projects: data.projects ?? [],
        faqs: data.faqs ?? [],
      };
      await courseService.create(payload);
      toast.success('Course created successfully');
      router.push('/courses');
    } catch (error) {
      console.error('Error creating course:', error);
      toast.error('Failed to create course');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Courses', href: '/courses' },
          { label: 'Create Course' },
        ]}
      />
      <PageHeader
        title="Create Course"
        description="Add a new training course"
      />
      <CourseForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}

