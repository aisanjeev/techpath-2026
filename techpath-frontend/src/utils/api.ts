/**
 * API Client for TechPath Frontend
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  timestamp?: string;
}

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: unknown;
  headers?: Record<string, string>;
}

/**
 * Makes an API request to the backend
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<ApiResponse<T>> {
  const { method = 'GET', body, headers = {} } = options;

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  };

  if (body && method !== 'GET') {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    const data = await response.json();

    if (!response.ok) {
      // The backend's APIException handler wraps errors as {error: {message}}, not a
      // top-level message/detail — without this, every backend-raised error (invalid
      // input, not found, etc.) silently fell through to the generic fallback below.
      return {
        success: false,
        error: data.error?.message || data.message || data.detail || 'An error occurred',
      };
    }

    return {
      success: true,
      data: data.data || data,
      message: data.message,
      timestamp: data.timestamp,
    };
  } catch (error) {
    console.error('API request failed:', error);
    return {
      success: false,
      error: 'Network error. Please check your connection.',
    };
  }
}

/**
 * GET request helper
 */
export async function get<T>(endpoint: string): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, { method: 'GET' });
}

/**
 * POST request helper
 */
export async function post<T>(endpoint: string, body: unknown): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, { method: 'POST', body });
}

/**
 * PUT request helper
 */
export async function put<T>(endpoint: string, body: unknown): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, { method: 'PUT', body });
}

/**
 * DELETE request helper
 */
export async function del<T>(endpoint: string): Promise<ApiResponse<T>> {
  return apiRequest<T>(endpoint, { method: 'DELETE' });
}

// API Endpoints
export const api = {
  // Contact
  contact: {
    submit: (data: { name: string; email: string; company?: string; message: string; service?: string }) =>
      post('/api/v1/contact', data),
  },

  // Newsletter
  newsletter: {
    subscribe: (email: string) => post('/api/v1/newsletter/subscribe', { email }),
    unsubscribe: (email: string) => post('/api/v1/newsletter/unsubscribe', { email }),
  },

  // Services
  services: {
    list: () => get('/api/v1/services'),
    get: (slug: string) => get(`/api/v1/services/${slug}`),
  },

  // Blog
  blog: {
    list: (params?: { page?: number; limit?: number; tag?: string }) => {
      const query = new URLSearchParams();
      if (params?.page) query.set('page', params.page.toString());
      if (params?.limit) query.set('limit', params.limit.toString());
      if (params?.tag) query.set('tag', params.tag);
      return get(`/api/v1/blog?${query.toString()}`);
    },
    get: (slug: string) => get(`/api/v1/blog/${slug}`),
  },

  // Inquiries
  inquiries: {
    submit: (data: {
      name: string;
      email: string;
      company?: string;
      service: string;
      budget?: string;
      timeline?: string;
      description: string;
    }) => post('/api/v1/inquiries', data),
  },
};

export default api;

