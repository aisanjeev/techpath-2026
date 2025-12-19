import { apiClient, handleApiError } from '@/lib/api-client';

export interface SecretMetadata {
  id: number;
  key_name: string;
  display_name: string;
  description: string | null;
  category: string;
  is_required: boolean;
  is_set: boolean;
  display_order: number;
  updated_by_id: number | null;
  updated_by_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface SecretValue {
  key_name: string;
  value: string | null;
  is_masked: boolean;
  is_set: boolean;
}

export interface SecretCategory {
  category: string;
  display_name: string;
  secrets: SecretMetadata[];
}

export interface SecretsStatus {
  total_secrets: number;
  set_secrets: number;
  unset_secrets: number;
  required_unset: number;
  keyvault_configured: boolean;
}

export const secretsService = {
  /**
   * Get all secrets metadata
   */
  async list(category?: string): Promise<SecretMetadata[]> {
    try {
      const params = category ? { category } : {};
      const response = await apiClient.get<SecretMetadata[]>('/api/v1/secrets/', { params });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Get secrets grouped by category
   */
  async listByCategory(): Promise<SecretCategory[]> {
    try {
      const response = await apiClient.get<SecretCategory[]>('/api/v1/secrets/categories');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Get overall secrets status
   */
  async getStatus(): Promise<SecretsStatus> {
    try {
      const response = await apiClient.get<SecretsStatus>('/api/v1/secrets/status');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Get a secret value (optionally revealed)
   */
  async getValue(keyName: string, reveal: boolean = false): Promise<SecretValue> {
    try {
      const response = await apiClient.get<SecretValue>(`/api/v1/secrets/${keyName}`, {
        params: { reveal },
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Update a secret value in Key Vault
   */
  async updateValue(keyName: string, value: string): Promise<SecretMetadata> {
    try {
      const response = await apiClient.put<SecretMetadata>(`/api/v1/secrets/${keyName}`, {
        value,
      });
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Delete a secret value from Key Vault
   */
  async deleteValue(keyName: string): Promise<SecretMetadata> {
    try {
      const response = await apiClient.delete<SecretMetadata>(`/api/v1/secrets/${keyName}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Sync secrets status from Key Vault
   */
  async syncStatus(): Promise<SecretMetadata[]> {
    try {
      const response = await apiClient.post<SecretMetadata[]>('/api/v1/secrets/sync');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /**
   * Get category display name
   */
  getCategoryDisplayName(category: string): string {
    const names: Record<string, string> = {
      email: 'Email (Azure Communication)',
      azure_openai: 'Azure OpenAI',
      storage: 'Azure Storage',
    };
    return names[category] || category.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  },

  /**
   * Get category icon name
   */
  getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
      email: 'Mail',
      azure_openai: 'Brain',
      storage: 'HardDrive',
    };
    return icons[category] || 'Key';
  },
};

