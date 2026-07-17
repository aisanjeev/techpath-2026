import { apiRequest } from '@utils/api';
import { getFirebaseAuth } from '@/lib/firebase';
import type {
  StudentLoginResponse,
  StudentSessionListResponse,
  StudentSessionMaterialsResponse,
} from '@/types/studentPortal';

/**
 * The student side of the materials portal. A real Firebase/Google account, not the
 * live classroom's 6-digit join code + short-lived token (classroomService.ts is that
 * other, separate half — see studentPortal.ts's top-of-file note on why they're kept
 * apart). Every call fetches a fresh ID token rather than caching one itself —
 * Firebase's SDK already caches/refreshes it internally, exactly like the admin app's
 * axios interceptor does for the same reason.
 */

export async function loginToPortal() {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<StudentLoginResponse>('/api/v1/student/auth/login', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getMySessions() {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<StudentSessionListResponse>('/api/v1/student/sessions', {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getSessionMaterials(sessionId: number) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<StudentSessionMaterialsResponse>(
    `/api/v1/student/sessions/${sessionId}/materials`,
    {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }
  );
}
