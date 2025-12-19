import { apiClient, handleApiError } from '@/lib/api-client';
import type { ContactInquiry, ContactInquiryUpdate, PaginatedResponse } from '@/types/api';

export interface ContactsListParams {
  skip?: number;
  limit?: number;
  status?: 'new' | 'in_progress' | 'resolved' | 'closed';
}

export const contactsService = {
  async list(params: ContactsListParams = {}): Promise<PaginatedResponse<ContactInquiry>> {
    try {
      const response = await apiClient.get<ContactInquiry[]>('/api/v1/contact/inquiries', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
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

  async getById(id: number): Promise<ContactInquiry> {
    try {
      const response = await apiClient.get<ContactInquiry>(`/api/v1/contact/inquiries/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: ContactInquiryUpdate): Promise<ContactInquiry> {
    try {
      const response = await apiClient.put<ContactInquiry>(`/api/v1/contact/inquiries/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/contact/inquiries/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },
};

