'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { BlogPostForm } from '@/components/forms/BlogPostForm';
import { PageLoader } from '@/components/ui/Spinner';
import { blogService } from '@/services/blog.service';
import type { BlogPostFormData } from '@/lib/validations';
import type { BlogPost } from '@/types/api';

export default function EditBlogPostPage() {
  const router = useRouter();
  const params = useParams();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Use slug from URL (param is named 'id' but contains slug)
  const postSlug = params.id as string;

  useEffect(() => {
    async function fetchPost() {
      try {
        const data = await blogService.getBySlug(postSlug);
        setPost(data);
      } catch (error) {
        console.error('Error fetching post:', error);
        toast.error('Blog post not found');
        router.push('/blog');
      } finally {
        setLoading(false);
      }
    }

    if (postSlug) {
      fetchPost();
    }
  }, [postSlug, router]);

  const handleSubmit = async (data: BlogPostFormData) => {
    if (!post) return;
    setIsSubmitting(true);
    try {
      // Use post.id for update (backend uses ID for PUT)
      await blogService.update(post.id, {
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
      toast.success('Blog post updated successfully');
      router.push('/blog');
    } catch (error) {
      console.error('Error updating post:', error);
      toast.error('Failed to update blog post');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <PageLoader />;
  }

  if (!post) {
    return null;
  }

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Blog Posts', href: '/blog' },
          { label: post.title },
        ]}
      />
      <PageHeader
        title="Edit Blog Post"
        description={`Editing "${post.title}"`}
      />
      <BlogPostForm
        initialData={post}
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
}

