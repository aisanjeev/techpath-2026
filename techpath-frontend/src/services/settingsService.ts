/**
 * Service for fetching app settings from the backend API.
 */

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

export interface PublicSettings {
  // Company info
  company_name?: string;
  company_email?: string;
  company_phone?: string;
  company_address?: string;
  // Social media
  social_twitter?: string;
  social_linkedin?: string;
  social_facebook?: string;
  // SEO
  seo_default_title?: string;
  seo_default_description?: string;
  google_analytics_id?: string;
  gtm_id?: string;
}

/**
 * Fetch all public settings from the API.
 */
export async function fetchPublicSettings(): Promise<PublicSettings> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/settings/public/all`);
    
    if (!response.ok) {
      console.error('Failed to fetch public settings:', response.status);
      return {};
    }
    
    const result = await response.json();
    return result.data || {};
  } catch (error) {
    console.error('Error fetching public settings:', error);
    return {};
  }
}

/**
 * Fetch a specific public setting by key.
 */
export async function fetchPublicSetting(key: string): Promise<string | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/settings/public/${key}`);
    
    if (!response.ok) {
      return null;
    }
    
    const result = await response.json();
    return result.value || null;
  } catch (error) {
    console.error(`Error fetching setting ${key}:`, error);
    return null;
  }
}

/**
 * Get SEO settings for use in page head.
 */
export async function fetchSeoSettings(): Promise<{
  title: string;
  description: string;
  analyticsId: string | null;
}> {
  const settings = await fetchPublicSettings();
  
  return {
    title: settings.seo_default_title || 'TechPath - IT Services & Gen AI Solutions',
    description: settings.seo_default_description || 'Professional IT services and Generative AI solutions for modern businesses',
    analyticsId: settings.google_analytics_id || null,
  };
}

/**
 * Get company info settings.
 */
export async function fetchCompanyInfo(): Promise<{
  name: string;
  email: string;
  phone: string;
  address: string;
  social: {
    twitter?: string;
    linkedin?: string;
    facebook?: string;
  };
}> {
  const settings = await fetchPublicSettings();
  
  return {
    name: settings.company_name || 'TechPath Professional Services',
    email: settings.company_email || 'info@techpath.biz',
    phone: settings.company_phone || '',
    address: settings.company_address || '',
    social: {
      twitter: settings.social_twitter || undefined,
      linkedin: settings.social_linkedin || undefined,
      facebook: settings.social_facebook || undefined,
    },
  };
}

