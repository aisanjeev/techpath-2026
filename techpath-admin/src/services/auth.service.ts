import { signInWithEmailAndPassword, signOut } from 'firebase/auth';
import type { User as FirebaseUser } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import { apiClient, handleApiError } from '@/lib/api-client';
import type { User } from '@/types/api';

export const authService = {
  async login(email: string, password: string): Promise<FirebaseUser> {
    const credential = await signInWithEmailAndPassword(getFirebaseAuth(), email, password);
    return credential.user;
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
    } catch {
      // Ignore backend logout errors — Firebase signOut is the source of truth
    } finally {
      await signOut(getFirebaseAuth());
    }
  },
};
