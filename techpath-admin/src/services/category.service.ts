import { apiClient, handleApiError } from '@/lib/api-client';

export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  parent_id: number | null;
  display_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface BlogCategoryTree extends BlogCategory {
  children: BlogCategoryTree[];
  post_count: number;
}

export interface BlogCategoryCreate {
  name: string;
  slug: string;
  description?: string;
  parent_id?: number | null;
  display_order?: number;
  is_active?: boolean;
}

export interface BlogCategoryUpdate {
  name?: string;
  slug?: string;
  description?: string;
  parent_id?: number | null;
  display_order?: number;
  is_active?: boolean;
}

export const categoryService = {
  async list(activeOnly: boolean = false): Promise<BlogCategory[]> {
    try {
      const response = await apiClient.get<BlogCategory[]>('/api/v1/blog/categories', {
        params: { active_only: activeOnly },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getTree(activeOnly: boolean = false): Promise<BlogCategoryTree[]> {
    try {
      const response = await apiClient.get<BlogCategoryTree[]>('/api/v1/blog/categories/tree', {
        params: { active_only: activeOnly },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getById(id: number): Promise<BlogCategory> {
    try {
      const response = await apiClient.get<BlogCategory>(`/api/v1/blog/categories/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async create(data: BlogCategoryCreate): Promise<BlogCategory> {
    try {
      const response = await apiClient.post<BlogCategory>('/api/v1/blog/categories', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: BlogCategoryUpdate): Promise<BlogCategory> {
    try {
      const response = await apiClient.put<BlogCategory>(`/api/v1/blog/categories/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/blog/categories/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Helper to flatten tree for dropdown
  flattenTree(categories: BlogCategoryTree[], level: number = 0): Array<BlogCategory & { level: number; fullPath: string }> {
    const result: Array<BlogCategory & { level: number; fullPath: string }> = [];
    
    for (const cat of categories) {
      const prefix = level > 0 ? '— '.repeat(level) : '';
      result.push({
        ...cat,
        level,
        fullPath: prefix + cat.name,
      });
      
      if (cat.children && cat.children.length > 0) {
        result.push(...this.flattenTree(cat.children, level + 1));
      }
    }
    
    return result;
  },
};

