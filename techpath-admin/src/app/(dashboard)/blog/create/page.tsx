'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { BlogPostForm } from '@/components/forms/BlogPostForm';
import { blogService } from '@/services/blog.service';
import type { BlogPostFormData } from '@/lib/validations';

export default function CreateBlogPostPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: BlogPostFormData) => {
    setIsLoading(true);
    try {
      await blogService.create({
        title: data.title,
        slug: data.slug,
        category_id: data.category_id,
        content: data.content,
        content_type: data.content_type,
        excerpt: data.excerpt || undefined,
        featured_image: data.featured_image || undefined,
        status: data.status,
        featured: data.featured,
        reading_time: data.reading_time || undefined,
        meta_title: data.meta_title || undefined,
        meta_description: data.meta_description || undefined,
        published_at: data.published_at || undefined,
        tag_ids: data.tag_ids,
      });
      toast.success('Blog post created successfully');
      router.push('/blog');
    } catch (error) {
      console.error('Error creating post:', error);
      toast.error('Failed to create blog post');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Blog Posts', href: '/blog' },
          { label: 'Create Post' },
        ]}
      />
      <PageHeader
        title="Create Blog Post"
        description="Write a new blog article"
      />
      <BlogPostForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}

