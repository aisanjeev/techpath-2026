'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { CourseForm } from '@/components/forms/CourseForm';
import { PageLoader } from '@/components/ui/Spinner';
import { courseService } from '@/services/course.service';
import type { CourseFormData } from '@/lib/validations';
import type { Course } from '@/types/api';

export default function EditCoursePage() {
  const router = useRouter();
  const params = useParams();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const courseSlug = params.id as string;

  useEffect(() => {
    async function fetchCourse() {
      try {
        const data = await courseService.getBySlug(courseSlug);
        setCourse(data);
      } catch (error) {
        console.error('Error fetching course:', error);
        toast.error('Course not found');
        router.push('/courses');
      } finally {
        setLoading(false);
      }
    }

    if (courseSlug) {
      fetchCourse();
    }
  }, [courseSlug, router]);

  const handleSubmit = async (data: CourseFormData) => {
    if (!course) return;
    setIsSubmitting(true);
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
      await courseService.update(course.id, payload);
      toast.success('Course updated successfully');
      router.push('/courses');
    } catch (error) {
      console.error('Error updating course:', error);
      toast.error('Failed to update course');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <PageLoader />;
  }

  if (!course) {
    return null;
  }

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Courses', href: '/courses' },
          { label: course.title },
        ]}
      />
      <PageHeader
        title="Edit Course"
        description={`Editing "${course.title}"`}
      />
      <CourseForm
        initialData={course}
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
}

