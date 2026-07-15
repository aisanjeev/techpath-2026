import { apiClient, handleApiError } from '@/lib/api-client';
import type {
  Page,
  PageCreate,
  PageListItem,
  PageUpdate,
  PaginatedResponse,
} from '@/types/api';

export interface PageListParams {
  skip?: number;
  limit?: number;
  status?: 'draft' | 'published' | 'archived';
  search?: string;
}

export const pagesService = {
  async list(params: PageListParams = {}): Promise<PaginatedResponse<PageListItem>> {
    try {
      const response = await apiClient.get<PageListItem[]>('/api/v1/pages', {
        params: {
          skip: params.skip ?? 0,
          limit: params.limit ?? 20,
          status: params.status,
          search: params.search,
        },
      });
      const totalHeader = response.headers?.['x-total-count'];
      const total = totalHeader != null ? parseInt(String(totalHeader), 10) : response.data.length;
      return {
        items: response.data,
        total: Number.isNaN(total) ? response.data.length : total,
      };
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBySlug(slug: string): Promise<Page> {
    try {
      const response = await apiClient.get<Page>(`/api/v1/pages/${slug}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async create(data: PageCreate): Promise<Page> {
    try {
      const response = await apiClient.post<Page>('/api/v1/pages', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: PageUpdate): Promise<Page> {
    try {
      const response = await apiClient.put<Page>(`/api/v1/pages/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/pages/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
