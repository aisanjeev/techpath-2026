import { apiClient, handleApiError } from '@/lib/api-client';
import type { PaginatedResponse } from '@/types/api';
import type {
  AssetType,
  AssetTypeInfo,
  AssetUsage,
  ContentStatus,
  LectureAsset,
  ModuleAssetLink,
  ReorderItem,
  TrainingModule,
  TrainingModuleCreate,
  TrainingModuleDetail,
  TrainingModuleUpdate,
  TrainingProgram,
  TrainingProgramCreate,
  TrainingProgramDetail,
  TrainingProgramUpdate,
} from '@/types/training';

export interface ProgramListParams {
  skip?: number;
  limit?: number;
  status?: ContentStatus;
  course_id?: number;
  search?: string;
}

export interface AssetListParams {
  skip?: number;
  limit?: number;
  asset_type?: AssetType;
  status?: ContentStatus;
  search?: string;
  program_id?: number;
  module_id?: number;
  tag?: string;
  unassigned?: boolean;
}

function paginate<T>(response: { data: T[]; headers?: Record<string, unknown> }): PaginatedResponse<T> {
  const totalHeader = response.headers?.['x-total-count'];
  const total = totalHeader != null ? parseInt(String(totalHeader), 10) : response.data.length;
  return { items: response.data, total: Number.isNaN(total) ? response.data.length : total };
}

export const trainingService = {
  // ---------- registry ----------

  /** The asset-type registry, served by the backend so both agree on the rules. */
  async assetTypes(): Promise<AssetTypeInfo[]> {
    try {
      const response = await apiClient.get<AssetTypeInfo[]>('/api/v1/training/asset-types');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ---------- programs ----------

  async listPrograms(params: ProgramListParams = {}): Promise<PaginatedResponse<TrainingProgram>> {
    try {
      const response = await apiClient.get<TrainingProgram[]>('/api/v1/training/programs', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          course_id: params.course_id,
          search: params.search,
        },
      });
      return paginate(response);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getProgram(id: number): Promise<TrainingProgramDetail> {
    try {
      const response = await apiClient.get<TrainingProgramDetail>(
        `/api/v1/training/programs/${id}`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createProgram(data: TrainingProgramCreate): Promise<TrainingProgramDetail> {
    try {
      const response = await apiClient.post<TrainingProgramDetail>(
        '/api/v1/training/programs',
        data
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateProgram(id: number, data: TrainingProgramUpdate): Promise<TrainingProgram> {
    try {
      const response = await apiClient.put<TrainingProgram>(
        `/api/v1/training/programs/${id}`,
        data
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteProgram(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/training/programs/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ---------- modules ----------

  async listModules(programId: number): Promise<TrainingModule[]> {
    try {
      const response = await apiClient.get<TrainingModule[]>(
        `/api/v1/training/programs/${programId}/modules`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createModule(programId: number, data: TrainingModuleCreate): Promise<TrainingModule> {
    try {
      const response = await apiClient.post<TrainingModule>(
        `/api/v1/training/programs/${programId}/modules`,
        data
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async reorderModules(programId: number, items: ReorderItem[]): Promise<void> {
    try {
      await apiClient.put(`/api/v1/training/programs/${programId}/modules/order`, { items });
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getModule(id: number): Promise<TrainingModuleDetail> {
    try {
      const response = await apiClient.get<TrainingModuleDetail>(
        `/api/v1/training/modules/${id}`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateModule(id: number, data: TrainingModuleUpdate): Promise<TrainingModule> {
    try {
      const response = await apiClient.put<TrainingModule>(`/api/v1/training/modules/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteModule(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/training/modules/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ---------- module <-> asset placement ----------

  async attachAsset(
    moduleId: number,
    data: { asset_id: number; display_order?: number; is_required?: boolean; notes?: string }
  ): Promise<ModuleAssetLink> {
    try {
      const response = await apiClient.post<ModuleAssetLink>(
        `/api/v1/training/modules/${moduleId}/assets`,
        data
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async reorderModuleAssets(moduleId: number, items: ReorderItem[]): Promise<void> {
    try {
      await apiClient.put(`/api/v1/training/modules/${moduleId}/assets/order`, { items });
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async detachAsset(moduleId: number, assetId: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/training/modules/${moduleId}/assets/${assetId}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // ---------- asset library ----------

  async listAssets(params: AssetListParams = {}): Promise<PaginatedResponse<LectureAsset>> {
    try {
      const response = await apiClient.get<LectureAsset[]>('/api/v1/training/assets', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          asset_type: params.asset_type,
          status: params.status,
          search: params.search,
          program_id: params.program_id,
          module_id: params.module_id,
          tag: params.tag,
          unassigned: params.unassigned,
        },
      });
      return paginate(response);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async assetTags(): Promise<string[]> {
    try {
      const response = await apiClient.get<string[]>('/api/v1/training/assets/tags');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getAsset(id: number): Promise<LectureAsset> {
    try {
      const response = await apiClient.get<LectureAsset>(`/api/v1/training/assets/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Where an asset is placed. Shown before edit/delete — assets are shared. */
  async getAssetUsages(id: number): Promise<AssetUsage[]> {
    try {
      const response = await apiClient.get<AssetUsage[]>(`/api/v1/training/assets/${id}/usages`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async bulkAssetPrograms(
    ids: number[]
  ): Promise<Record<string, { program_id: number; program_title: string }[]>> {
    if (!ids.length) return {};
    try {
      const response = await apiClient.post<{
        data: Record<string, { program_id: number; program_title: string }[]>;
      }>('/api/v1/training/assets/bulk-programs', { asset_ids: ids });
      return response.data.data;
    } catch {
      return {};
    }
  },

  /** Payload shape depends on asset_type — the backend validates it as a union. */
  async createAsset(data: Record<string, unknown>): Promise<LectureAsset> {
    try {
      const response = await apiClient.post<LectureAsset>('/api/v1/training/assets', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async updateAsset(id: number, data: Record<string, unknown>): Promise<LectureAsset> {
    try {
      const response = await apiClient.put<LectureAsset>(`/api/v1/training/assets/${id}`, data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async deleteAsset(id: number): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/training/assets/${id}`);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async bulkDeleteAssets(
    assetIds: number[]
  ): Promise<{ deleted: number; failed: number; in_use: number; message: string }> {
    try {
      const response = await apiClient.post<{
        deleted: number;
        failed: number;
        in_use: number;
        message: string;
      }>('/api/v1/training/assets/bulk-delete', { asset_ids: assetIds });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Upload a file for a file-backed asset. Streams server-side; reports progress. */
  async uploadAssetFile(
    assetType: AssetType,
    file: File,
    onProgress?: (percent: number) => void
  ): Promise<{ data: { id: number; url: string; filename: string; size: number } }> {
    try {
      const form = new FormData();
      form.append('file', file);
      const response = await apiClient.post(
        `/api/v1/uploads/lecture-asset?asset_type=${assetType}`,
        form,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          // Large uploads without progress feel broken, so surface it.
          onUploadProgress: (event) => {
            if (onProgress && event.total) {
              onProgress(Math.round((event.loaded * 100) / event.total));
            }
          },
        }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
