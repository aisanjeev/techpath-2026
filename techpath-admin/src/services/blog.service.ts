import { apiClient, handleApiError } from '@/lib/api-client';
import type { BlogPost, BlogPostCreate, BlogPostUpdate, BlogTag, PaginatedResponse } from '@/types/api';

export interface BlogListParams {
  skip?: number;
  limit?: number;
  status?: 'draft' | 'published' | 'archived';
  featured?: boolean;
  tag?: string;
  search?: string;
}

export const blogService = {
  async list(params: BlogListParams = {}): Promise<PaginatedResponse<BlogPost>> {
    try {
      const response = await apiClient.get<BlogPost[]>('/api/v1/blog/posts', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          featured: params.featured,
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

  async getBySlug(slug: string): Promise<BlogPost> {
    try {
      // Backend uses slug in path: GET /posts/{slug}
      const response = await apiClient.get<BlogPost>(`/api/v1/blog/posts/${slug}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async create(data: BlogPostCreate): Promise<BlogPost> {
    try {
      const response = await apiClient.post<BlogPost>('/api/v1/blog/posts', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: BlogPostUpdate): Promise<BlogPost> {
    try {
      const response = await apiClient.put<BlogPost>(`/api/v1/blog/posts/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/blog/posts/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Tags
  async listTags(): Promise<BlogTag[]> {
    try {
      const response = await apiClient.get<BlogTag[]>('/api/v1/blog/tags');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createTag(data: { name: string; slug: string }): Promise<BlogTag> {
    try {
      const response = await apiClient.post<BlogTag>('/api/v1/blog/tags', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteTag(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/blog/tags/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};

