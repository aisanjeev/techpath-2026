'use client';

import { useState, useCallback, useEffect } from 'react';

interface UseApiOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: unknown) => void;
  dependencies?: unknown[];
  immediate?: boolean;
}

interface UseApiReturn<T> {
  data: T | null;
  loading: boolean;
  error: unknown;
  refetch: () => Promise<T | null>;
  execute: () => Promise<T | null>;
}

export function useApi<T>(
  fn: () => Promise<T>,
  options: UseApiOptions<T> = {}
): UseApiReturn<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(options.immediate !== false);
  const [error, setError] = useState<unknown>(null);

  const execute = useCallback(async (): Promise<T | null> => {
    setLoading(true);
    setError(null);
    try {
      const result = await fn();
      setData(result);
      options.onSuccess?.(result);
      return result;
    } catch (err) {
      setError(err);
      options.onError?.(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, [fn, options]);

  useEffect(() => {
    if (options.immediate !== false) {
      execute();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, options.dependencies || []);

  return {
    data,
    loading,
    error,
    refetch: execute,
    execute,
  };
}

// Mutation hook for create/update/delete operations
interface UseMutationOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: unknown) => void;
}

interface UseMutationReturn<T, P> {
  data: T | null;
  loading: boolean;
  error: unknown;
  mutate: (params: P) => Promise<T | null>;
  reset: () => void;
}

export function useMutation<T, P>(
  fn: (params: P) => Promise<T>,
  options: UseMutationOptions<T> = {}
): UseMutationReturn<T, P> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const mutate = useCallback(async (params: P): Promise<T | null> => {
    setLoading(true);
    setError(null);
    try {
      const result = await fn(params);
      setData(result);
      options.onSuccess?.(result);
      return result;
    } catch (err) {
      setError(err);
      options.onError?.(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, [fn, options]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    data,
    loading,
    error,
    mutate,
    reset,
  };
}

