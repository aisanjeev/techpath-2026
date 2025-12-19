import { apiClient, handleApiError } from '@/lib/api-client';

export interface AppSetting {
  id: number;
  key: string;
  value: string | null;
  display_name: string;
  description: string | null;
  category: string;
  value_type: 'string' | 'email' | 'number' | 'boolean' | 'json';
  display_order: number;
  updated_by_id: number | null;
  updated_by_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface SettingsCategory {
  category: string;
  display_name: string;
  settings: AppSetting[];
}

export const settingsService = {
  /**
   * Get all settings grouped by category
   */
  async listSettings(category?: string): Promise<SettingsCategory[]> {
    try {
      const params = category ? { category } : {};
      const response = await apiClient.get('/api/v1/settings', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Get a specific setting by key
   */
  async getSetting(key: string): Promise<AppSetting> {
    try {
      const response = await apiClient.get(`/api/v1/settings/${key}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Update a setting value
   */
  async updateSetting(key: string, value: string | null): Promise<AppSetting> {
    try {
      const response = await apiClient.put(`/api/v1/settings/${key}`, { value });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Batch update multiple settings
   */
  async updateSettings(updates: { key: string; value: string | null }[]): Promise<AppSetting[]> {
    const results: AppSetting[] = [];
    for (const update of updates) {
      const result = await this.updateSetting(update.key, update.value);
      results.push(result);
    }
    return results;
  },
};

