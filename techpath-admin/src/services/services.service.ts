import { apiClient, handleApiError } from '@/lib/api-client';
import type { Service, ServiceCreate, ServiceUpdate, PaginatedResponse } from '@/types/api';

export interface ServicesListParams {
  skip?: number;
  limit?: number;
  active_only?: boolean;
  featured?: boolean;
  search?: string;
}

export const servicesService = {
  async list(params: ServicesListParams = {}): Promise<PaginatedResponse<Service>> {
    try {
      const response = await apiClient.get<Service[]>('/api/v1/services/', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          active_only: params.active_only ?? false, // Get all services for admin
          featured: params.featured,
        },
      });
      // Backend returns array, wrap in paginated format
      return {
        items: response.data,
        total: response.data.length,
      };
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBySlug(slug: string): Promise<Service> {
    try {
      // Backend uses slug in path: GET /{slug}
      const response = await apiClient.get<Service>(`/api/v1/services/${slug}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async create(data: ServiceCreate): Promise<Service> {
    try {
      const response = await apiClient.post<Service>('/api/v1/services/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: ServiceUpdate): Promise<Service> {
    try {
      const response = await apiClient.put<Service>(`/api/v1/services/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/services/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};

