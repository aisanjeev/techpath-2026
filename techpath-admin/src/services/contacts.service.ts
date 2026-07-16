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

  /**
   * Fetch every inquiry across all pages (optionally filtered by status).
   * Used for exports and "clear all" — the list endpoint caps `limit` at 100.
   */
  async listAll(status?: ContactsListParams['status']): Promise<ContactInquiry[]> {
    try {
      const pageSize = 100;
      const all: ContactInquiry[] = [];
      let skip = 0;
      // Guard against an unexpected server loop; 100k rows is far beyond normal.
      while (skip < 100_000) {
        const response = await apiClient.get<ContactInquiry[]>('/api/v1/contact/inquiries', {
          params: { skip, limit: pageSize, status },
        });
        all.push(...response.data);
        if (response.data.length < pageSize) break;
        skip += pageSize;
      }
      return all;
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

  /**
   * Delete many inquiries. The backend exposes only single-record deletes, so
   * these run sequentially to stay gentle on the DB. Returns per-id results so
   * callers can report partial failures.
   */
  async deleteMany(ids: number[]): Promise<{ deleted: number; failed: number }> {
    let deleted = 0;
    let failed = 0;
    for (const id of ids) {
      try {
        await apiClient.delete(`/api/v1/contact/inquiries/${id}`);
        deleted += 1;
      } catch {
        failed += 1;
      }
    }
    return { deleted, failed };
  },
};

