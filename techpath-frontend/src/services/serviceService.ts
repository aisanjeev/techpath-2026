/**
 * Public API for services (list and by slug).
 * Used by services index and service detail pages.
 */

const API_BASE =
  typeof import.meta.env !== 'undefined' && import.meta.env.PUBLIC_API_URL
    ? import.meta.env.PUBLIC_API_URL
    : 'http://localhost:8000';

export interface ServicePricingPlanItem {
  name: string;
  description: string;
  price: string;
  period: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

export interface ServiceItem {
  id: number;
  title: string;
  slug: string;
  description: string;
  short_description?: string | null;
  icon?: string | null;
  image_url?: string | null;
  features?: string[] | null;
  pricing_plans?: ServicePricingPlanItem[] | null;
  faqs?: { question: string; answer: string }[] | null;
  price?: string | null;
  cta_text: string;
  cta_url?: string | null;
  featured: boolean;
  display_order: number;
  is_active: boolean;
  meta_title?: string | null;
  meta_description?: string | null;
  og_image?: string | null;
  canonical_url?: string | null;
  no_index?: boolean;
  // Bento layout
  layout_size?: 'large' | 'small' | 'wide';
  badge_label?: string | null;
  tags?: string[] | null;
  stat_label?: string | null;
  stat_value?: string | null;
  accent_color?: 'purple' | 'cyan' | 'green' | 'amber' | 'blue';
  graphic_variant?: 'orbital' | 'code-window' | 'bar-chart' | 'none';
  created_at: string;
  updated_at: string;
}

export async function fetchServices(): Promise<ServiceItem[]> {
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/services/?active_only=true&limit=50`,
      { headers: { Accept: 'application/json' } }
    );
    if (!res.ok) return [];
    const data = (await res.json()) as ServiceItem[];
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

export async function fetchServiceBySlug(slug: string): Promise<ServiceItem | null> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/services/${slug}`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return null;
    return (await res.json()) as ServiceItem;
  } catch {
    return null;
  }
}
