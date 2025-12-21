import { apiClient, handleApiError } from '@/lib/api-client';
import type { CaseStudy, CaseStudyCreate, CaseStudyUpdate, CaseStudyTag, PaginatedResponse } from '@/types/api';

export interface CaseStudyListParams {
  skip?: number;
  limit?: number;
  status?: 'draft' | 'published' | 'archived';
  featured?: boolean;
  industry?: string;
  tag?: string;
}

export const caseStudiesService = {
  async list(params: CaseStudyListParams = {}): Promise<PaginatedResponse<CaseStudy>> {
    try {
      const response = await apiClient.get<CaseStudy[]>('/api/v1/case-studies/', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          featured: params.featured,
          industry: params.industry,
          tag: params.tag,
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

  async getBySlug(slug: string): Promise<CaseStudy> {
    try {
      // Backend uses slug in path: GET /{slug}
      const response = await apiClient.get<CaseStudy>(`/api/v1/case-studies/${slug}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async create(data: CaseStudyCreate): Promise<CaseStudy> {
    try {
      const response = await apiClient.post<CaseStudy>('/api/v1/case-studies/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: CaseStudyUpdate): Promise<CaseStudy> {
    try {
      const response = await apiClient.put<CaseStudy>(`/api/v1/case-studies/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/case-studies/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Tags
  async listTags(): Promise<CaseStudyTag[]> {
    try {
      const response = await apiClient.get<CaseStudyTag[]>('/api/v1/case-studies/tags/');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createTag(name: string, slug: string): Promise<CaseStudyTag> {
    try {
      const response = await apiClient.post<CaseStudyTag>('/api/v1/case-studies/tags/', { name, slug });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};

