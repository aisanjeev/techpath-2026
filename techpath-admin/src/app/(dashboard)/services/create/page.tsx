'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { ServiceForm } from '@/components/forms/ServiceForm';
import { servicesService } from '@/services/services.service';
import type { ServiceFormData } from '@/lib/validations';

export default function CreateServicePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: ServiceFormData) => {
    setIsLoading(true);
    try {
      await servicesService.create({
        title: data.title,
        slug: data.slug,
        description: data.description,
        short_description: data.short_description || undefined,
        icon: data.icon || undefined,
        image_url: data.image_url || undefined,
        features: data.features || undefined,
        pricing_plans: data.pricing_plans || undefined,
        faqs: data.faqs || undefined,
        price: data.price || undefined,
        cta_text: data.cta_text || undefined,
        cta_url: data.cta_url || undefined,
        featured: data.featured,
        display_order: data.display_order,
        is_active: data.is_active,
        meta_title: data.meta_title || undefined,
        meta_description: data.meta_description || undefined,
        og_image: data.og_image || undefined,
        canonical_url: data.canonical_url || undefined,
        no_index: data.no_index,
      });
      toast.success('Service created successfully');
      router.push('/services');
    } catch (error) {
      console.error('Error creating service:', error);
      toast.error('Failed to create service');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Services', href: '/services' },
          { label: 'Create Service' },
        ]}
      />
      <PageHeader
        title="Create Service"
        description="Add a new service to your offerings"
      />
      <ServiceForm onSubmit={handleSubmit} isLoading={isLoading} />
    </div>
  );
}

