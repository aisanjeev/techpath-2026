import { apiClient, handleApiError } from '@/lib/api-client';

export interface UploadResponse {
  success: boolean;
  data: {
    path: string;
    url: string;
    filename: string;
    content_type: string;
    size: number;
  };
}

export const uploadsService = {
  async uploadImage(file: File, folder: string = 'images'): Promise<UploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post<UploadResponse>(
        `/api/v1/uploads/image?folder=${encodeURIComponent(folder)}`,
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

  async uploadFile(file: File, folder: string = 'files'): Promise<UploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post<UploadResponse>(
        `/api/v1/uploads/file?folder=${encodeURIComponent(folder)}`,
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

  async deleteFile(filePath: string): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/uploads/${encodeURIComponent(filePath)}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Get the full URL for a file path.
   * For local storage, prepends the API base URL.
   * For Azure, the URL is already complete.
   */
  getFileUrl(pathOrUrl: string): string {
    if (!pathOrUrl) return '';
    
    // If it's already a full URL, return as-is
    if (pathOrUrl.startsWith('http://') || pathOrUrl.startsWith('https://')) {
      return pathOrUrl;
    }
    
    // For local storage paths (e.g., /uploads/images/file.jpg)
    if (pathOrUrl.startsWith('/uploads/')) {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      return `${apiBase}${pathOrUrl}`;
    }
    
    // For relative paths without /uploads prefix
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    return `${apiBase}/uploads/${pathOrUrl}`;
  },
};

