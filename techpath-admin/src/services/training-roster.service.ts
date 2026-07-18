import { apiClient, handleApiError } from '@/lib/api-client';
import type { PaginatedResponse } from '@/types/api';
import type {
  SyncRunResult,
  SyncStatus,
  TrainingBatch,
  TrainingStudent,
} from '@/types/training';

export interface BatchListParams {
  skip?: number;
  limit?: number;
  status?: string;
  trainer_email?: string;
  search?: string;
}

export interface StudentListParams {
  skip?: number;
  limit?: number;
  status?: string;
  batch_id?: number;
  search?: string;
}

function paginate<T>(response: {
  data: T[];
  headers?: Record<string, unknown>;
}): PaginatedResponse<T> {
  const totalHeader = response.headers?.['x-total-count'];
  const total = totalHeader != null ? parseInt(String(totalHeader), 10) : response.data.length;
  return { items: response.data, total: Number.isNaN(total) ? response.data.length : total };
}

/**
 * Batches and students are mirrored from an external system and are read-only here.
 * There is no create/update/delete — the only writable field is a batch's program_id,
 * which is ours.
 */
export const trainingRosterService = {
  async listBatches(params: BatchListParams = {}): Promise<PaginatedResponse<TrainingBatch>> {
    try {
      const response = await apiClient.get<TrainingBatch[]>('/api/v1/training/batches', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          trainer_email: params.trainer_email,
          search: params.search,
        },
      });
      return paginate(response);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBatch(id: number): Promise<TrainingBatch> {
    try {
      const response = await apiClient.get<TrainingBatch>(`/api/v1/training/batches/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBatchStudents(id: number): Promise<TrainingStudent[]> {
    try {
      const response = await apiClient.get<TrainingStudent[]>(
        `/api/v1/training/batches/${id}/students`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async linkProgram(batchId: number, programId: number | null): Promise<TrainingBatch> {
    try {
      const response = await apiClient.patch<TrainingBatch>(
        `/api/v1/training/batches/${batchId}/program`,
        { program_id: programId }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async assignTrainer(batchId: number, trainerEmail: string | null): Promise<TrainingBatch> {
    try {
      const response = await apiClient.patch<TrainingBatch>(
        `/api/v1/training/batches/${batchId}/trainer`,
        { trainer_email: trainerEmail }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async listStudents(params: StudentListParams = {}): Promise<PaginatedResponse<TrainingStudent>> {
    try {
      const response = await apiClient.get<TrainingStudent[]>('/api/v1/training/students', {
        params: {
          skip: params.skip || 0,
          limit: params.limit || 20,
          status: params.status,
          batch_id: params.batch_id,
          search: params.search,
        },
      });
      return paginate(response);
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getStudent(id: number): Promise<TrainingStudent> {
    try {
      const response = await apiClient.get<TrainingStudent>(`/api/v1/training/students/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async syncStatus(): Promise<SyncStatus> {
    try {
      const response = await apiClient.get<SyncStatus>('/api/v1/training/sync/status');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async runSync(resource: 'batches' | 'students' | 'all' = 'all'): Promise<SyncRunResult> {
    try {
      const response = await apiClient.post<SyncRunResult>(`/api/v1/training/sync/${resource}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
