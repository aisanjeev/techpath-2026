import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { getFirebaseAuth } from '@/lib/firebase';
import { useAuthStore } from '@/store/auth.store';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Attach a fresh Firebase ID token to every request (auto-refreshes if expired)
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const firebaseUser = getFirebaseAuth().currentUser;
    if (firebaseUser) {
      const token = await firebaseUser.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// On 401, sign out and redirect to login
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export interface ApiError {
  status: number;
  message: string;
  detail?: string | { msg: string; type: string }[];
}

interface ApiErrorResponse {
  success?: boolean;
  error?: {
    code?: string;
    message?: string;
    details?: Record<string, unknown>;
  };
  detail?: string | { msg: string; type: string }[];
}

export function handleApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiErrorResponse>;
    const responseData = axiosError.response?.data;

    if (responseData?.error?.message) {
      return {
        status: axiosError.response?.status || 500,
        message: responseData.error.message,
        detail: responseData.detail,
      };
    }

    if (typeof responseData?.detail === 'string') {
      return {
        status: axiosError.response?.status || 500,
        message: responseData.detail,
        detail: responseData.detail,
      };
    }

    if (Array.isArray(responseData?.detail)) {
      const messages = responseData.detail.map((d) => d.msg).join(', ');
      return {
        status: axiosError.response?.status || 500,
        message: messages || axiosError.message,
        detail: responseData.detail,
      };
    }

    return {
      status: axiosError.response?.status || 500,
      message: axiosError.message,
      detail: responseData?.detail,
    };
  }
  return {
    status: 500,
    message: 'An unexpected error occurred',
  };
}

export { apiClient };
