import { apiClient, handleApiError } from '@/lib/api-client';
import type { AdminUser, PaginatedResponse, Role } from '@/types/api';

export interface UserListParams {
  skip?: number;
  limit?: number;
  role?: Role;
}

export interface UserProvision {
  email: string;
  name: string;
  role: Role;
  password?: string;
  is_active?: boolean;
}

export interface UserAdminUpdate {
  name?: string;
  role?: Role;
  is_active?: boolean;
}

export const usersService = {
  async list(params: UserListParams = {}): Promise<PaginatedResponse<AdminUser>> {
    try {
      const response = await apiClient.get<AdminUser[]>('/api/v1/auth/users', {
        params: { skip: params.skip || 0, limit: params.limit || 50, role: params.role },
      });
      const totalHeader = response.headers?.['x-total-count'];
      const total =
        totalHeader != null ? parseInt(String(totalHeader), 10) : response.data.length;
      return { items: response.data, total: Number.isNaN(total) ? response.data.length : total };
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async provision(data: UserProvision): Promise<AdminUser> {
    try {
      const response = await apiClient.post<AdminUser>('/api/v1/auth/users', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: UserAdminUpdate): Promise<AdminUser> {
    try {
      const response = await apiClient.patch<AdminUser>(`/api/v1/auth/users/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async remove(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/auth/users/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
