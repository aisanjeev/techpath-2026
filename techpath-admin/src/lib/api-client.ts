import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '@/store/auth.store';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear auth state and redirect to login
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
    
    // Handle API error format: { success: false, error: { message: "..." } }
    if (responseData?.error?.message) {
      return {
        status: axiosError.response?.status || 500,
        message: responseData.error.message,
        detail: responseData.detail,
      };
    }
    
    // Handle FastAPI validation error format: { detail: "..." }
    if (typeof responseData?.detail === 'string') {
      return {
        status: axiosError.response?.status || 500,
        message: responseData.detail,
        detail: responseData.detail,
      };
    }
    
    // Handle FastAPI validation error array format
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

