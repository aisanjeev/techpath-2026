'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { ServiceForm } from '@/components/forms/ServiceForm';
import { PageLoader } from '@/components/ui/Spinner';
import { servicesService } from '@/services/services.service';
import type { ServiceFormData } from '@/lib/validations';
import type { Service } from '@/types/api';

export default function EditServicePage() {
  const router = useRouter();
  const params = useParams();
  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Use slug from URL (param is named 'id' but contains slug)
  const serviceSlug = params.id as string;

  useEffect(() => {
    async function fetchService() {
      try {
        const data = await servicesService.getBySlug(serviceSlug);
        setService(data);
      } catch (error) {
        console.error('Error fetching service:', error);
        toast.error('Service not found');
        router.push('/services');
      } finally {
        setLoading(false);
      }
    }

    if (serviceSlug) {
      fetchService();
    }
  }, [serviceSlug, router]);

  const handleSubmit = async (data: ServiceFormData) => {
    if (!service) return;
    setIsSubmitting(true);
    try {
      // Use service.id for update (backend uses ID for PUT)
      await servicesService.update(service.id, {
        title: data.title,
        slug: data.slug,
        description: data.description,
        short_description: data.short_description || undefined,
        icon: data.icon || undefined,
        image_url: data.image_url || undefined,
        features: data.features || undefined,
        price: data.price || undefined,
        cta_text: data.cta_text || undefined,
        cta_url: data.cta_url || undefined,
        featured: data.featured,
        display_order: data.display_order,
        is_active: data.is_active,
      });
      toast.success('Service updated successfully');
      router.push('/services');
    } catch (error) {
      console.error('Error updating service:', error);
      toast.error('Failed to update service');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <PageLoader />;
  }

  if (!service) {
    return null;
  }

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Services', href: '/services' },
          { label: service.title },
        ]}
      />
      <PageHeader
        title="Edit Service"
        description={`Editing "${service.title}"`}
      />
      <ServiceForm
        initialData={service}
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
}

