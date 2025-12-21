import { apiClient, handleApiError } from '@/lib/api-client';
import type { LoginResponse, User } from '@/types/api';

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/f169a641-4bc6-4f52-86c3-62ff4f91ea69',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'auth.service.ts:login',message:'Login attempt with JSON body',data:{email,bodyType:'json'},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    try {
      // Send JSON body with email and password (matching backend UserLogin schema)
      const response = await apiClient.post<LoginResponse>('/api/v1/auth/login', {
        email,
        password,
      });
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/f169a641-4bc6-4f52-86c3-62ff4f91ea69',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'auth.service.ts:login:success',message:'Login successful',data:{hasToken:!!response.data?.access_token},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      return response.data;
    } catch (error) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/f169a641-4bc6-4f52-86c3-62ff4f91ea69',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'auth.service.ts:login:error',message:'Login failed',data:{error:String(error)},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      throw handleApiError(error);
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get<User>('/api/v1/auth/me');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/v1/auth/logout');
    } catch (error) {
      // Ignore logout errors, clear local state anyway
      console.error('Logout error:', error);
    }
  },
};

