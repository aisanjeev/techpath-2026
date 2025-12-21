import { apiClient, handleApiError } from '@/lib/api-client';
import type {
  Course,
  CourseCreate,
  CourseUpdate,
  CourseCategory,
  CourseCategoryTree,
  CourseEnrollment,
  CourseEnrollmentUpdate,
  Skill,
  PaginatedResponse,
} from '@/types/api';

export interface CourseListParams {
  skip?: number;
  limit?: number;
  status?: 'draft' | 'published' | 'archived';
  featured?: boolean;
  category?: string;
  level?: string;
}

export interface EnrollmentListParams {
  skip?: number;
  limit?: number;
  status?: string;
  course_id?: number;
  assigned_to?: string;
}

export interface CourseCategoryCreate {
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  parent_id?: number | null;
  display_order?: number;
  is_active?: boolean;
}

export interface CourseCategoryUpdate {
  name?: string;
  slug?: string;
  description?: string;
  icon?: string;
  parent_id?: number | null;
  display_order?: number;
  is_active?: boolean;
}

export interface SkillCreate {
  name: string;
  slug: string;
}

interface ApiPaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    total: number;
    page: number;
    per_page: number;
    pages: number;
  };
}

export const courseService = {
  // Courses
  async list(params: CourseListParams = {}): Promise<PaginatedResponse<Course>> {
    try {
      const response = await apiClient.get<ApiPaginatedResponse<Course>>('/api/v1/courses/', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          featured: params.featured,
          category: params.category,
          level: params.level,
        },
      });
      // Transform API response to PaginatedResponse format
      return {
        items: response.data.data,
        total: response.data.pagination.total,
      };
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBySlug(slug: string): Promise<Course> {
    try {
      const response = await apiClient.get<Course>(`/api/v1/courses/${slug}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async create(data: CourseCreate): Promise<Course> {
    try {
      const response = await apiClient.post<Course>('/api/v1/courses/', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: CourseUpdate): Promise<Course> {
    try {
      const response = await apiClient.put<Course>(`/api/v1/courses/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/courses/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Categories
  async listCategories(activeOnly: boolean = false): Promise<CourseCategory[]> {
    try {
      const response = await apiClient.get<CourseCategory[]>('/api/v1/courses/categories', {
        params: { active_only: activeOnly },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getCategoryTree(activeOnly: boolean = false): Promise<CourseCategoryTree[]> {
    try {
      const response = await apiClient.get<CourseCategoryTree[]>('/api/v1/courses/categories/tree', {
        params: { active_only: activeOnly },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createCategory(data: CourseCategoryCreate): Promise<CourseCategory> {
    try {
      const response = await apiClient.post<CourseCategory>('/api/v1/courses/categories', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateCategory(id: number, data: CourseCategoryUpdate): Promise<CourseCategory> {
    try {
      const response = await apiClient.put<CourseCategory>(`/api/v1/courses/categories/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteCategory(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/courses/categories/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Skills
  async listSkills(): Promise<Skill[]> {
    try {
      const response = await apiClient.get<Skill[]>('/api/v1/courses/skills');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createSkill(data: SkillCreate): Promise<Skill> {
    try {
      const response = await apiClient.post<Skill>('/api/v1/courses/skills', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteSkill(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/courses/skills/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Enrollments
  async listEnrollments(params: EnrollmentListParams = {}): Promise<PaginatedResponse<CourseEnrollment>> {
    try {
      const response = await apiClient.get<ApiPaginatedResponse<CourseEnrollment>>('/api/v1/courses/enrollments/', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          course_id: params.course_id,
          assigned_to: params.assigned_to,
        },
      });
      return {
        items: response.data.data,
        total: response.data.pagination.total,
      };
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getEnrollment(id: number): Promise<CourseEnrollment> {
    try {
      const response = await apiClient.get<CourseEnrollment>(`/api/v1/courses/enrollments/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateEnrollment(id: number, data: CourseEnrollmentUpdate): Promise<CourseEnrollment> {
    try {
      const response = await apiClient.put<CourseEnrollment>(`/api/v1/courses/enrollments/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteEnrollment(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/courses/enrollments/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getEnrollmentStats(): Promise<{ total: number; by_status: Record<string, number> }> {
    try {
      const response = await apiClient.get<{ total: number; by_status: Record<string, number> }>('/api/v1/courses/enrollments/stats');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Helper to flatten category tree for dropdown
  flattenCategoryTree(categories: CourseCategoryTree[], level: number = 0): Array<CourseCategory & { level: number; fullPath: string }> {
    const result: Array<CourseCategory & { level: number; fullPath: string }> = [];

    for (const cat of categories) {
      const prefix = level > 0 ? '— '.repeat(level) : '';
      result.push({
        ...cat,
        level,
        fullPath: prefix + cat.name,
      });

      if (cat.children && cat.children.length > 0) {
        result.push(...this.flattenCategoryTree(cat.children, level + 1));
      }
    }

    return result;
  },
};

