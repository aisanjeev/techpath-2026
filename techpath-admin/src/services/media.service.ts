import { apiClient, handleApiError } from '@/lib/api-client';

export interface MediaFile {
  id: number;
  filename: string;
  stored_path: string;
  file_hash: string;
  content_type: string;
  size: number;
  width: number | null;
  height: number | null;
  alt_text: string | null;
  url: string;
  created_at: string;
  updated_at: string;
}

export interface MediaFileListItem {
  id: number;
  filename: string;
  stored_path: string;
  content_type: string;
  size: number;
  width: number | null;
  height: number | null;
  alt_text: string | null;
  url: string;
  usage_count: number;
  created_at: string;
}

export interface MediaFileUsage {
  id: number;
  file_id: number;
  entity_type: string;
  entity_id: number;
  field_name: string;
  created_at: string;
}

export interface MediaFileDetail extends MediaFile {
  usages: MediaFileUsage[];
  usage_count: number;
}

export interface MediaUploadResponse {
  success: boolean;
  data: MediaFile;
  is_duplicate: boolean;
  message: string;
}

export interface MediaListParams {
  skip?: number;
  limit?: number;
  content_type?: string;
  search?: string;
}

export const mediaService = {
  async list(params: MediaListParams = {}): Promise<MediaFileListItem[]> {
    try {
      const response = await apiClient.get<MediaFileListItem[]>('/api/v1/media/', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 50,
          content_type: params.content_type,
          search: params.search,
        },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getById(id: number): Promise<MediaFileDetail> {
    try {
      const response = await apiClient.get<MediaFileDetail>(`/api/v1/media/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async update(id: number, data: { alt_text?: string }): Promise<MediaFile> {
    try {
      const response = await apiClient.patch<MediaFile>(`/api/v1/media/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/media/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getUsages(id: number): Promise<MediaFileUsage[]> {
    try {
      const response = await apiClient.get<MediaFileUsage[]>(`/api/v1/media/${id}/usages`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async removeUsage(mediaId: number, usageId: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/media/${mediaId}/usages/${usageId}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async uploadImage(
    file: File,
    folder: string = 'images',
    entityType?: string,
    entityId?: number,
    fieldName?: string
  ): Promise<MediaUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const params = new URLSearchParams({ folder });
      if (entityType) params.append('entity_type', entityType);
      if (entityId) params.append('entity_id', entityId.toString());
      if (fieldName) params.append('field_name', fieldName);

      const response = await apiClient.post<MediaUploadResponse>(
        `/api/v1/uploads/image?${params.toString()}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async uploadFile(
    file: File,
    folder: string = 'documents',
    entityType?: string,
    entityId?: number,
    fieldName?: string
  ): Promise<MediaUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const params = new URLSearchParams({ folder });
      if (entityType) params.append('entity_type', entityType);
      if (entityId) params.append('entity_id', entityId.toString());
      if (fieldName) params.append('field_name', fieldName);

      const response = await apiClient.post<MediaUploadResponse>(
        `/api/v1/uploads/file?${params.toString()}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  isImageType(contentType: string): boolean {
    return contentType.startsWith('image/');
  },

  isDocumentType(contentType: string): boolean {
    return [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
    ].includes(contentType);
  },

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },

  getFileTypeLabel(contentType: string): string {
    if (contentType.startsWith('image/')) return 'Image';
    if (contentType === 'application/pdf') return 'PDF';
    if (contentType.includes('word')) return 'Word Document';
    if (contentType === 'text/plain') return 'Text File';
    return 'File';
  },
};

