import { apiRequest } from '@utils/api';
import { getFirebaseAuth } from '@/lib/firebase';
import type {
  QuizAttemptResult,
  StudentLoginResponse,
  StudentProgressResponse,
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

/** Which material items this student has completed and which are still locked.
 *  Computed server-side — the client doesn't know the pass mark and couldn't be
 *  trusted with the decision anyway. */
export async function getSessionProgress(sessionId: number) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<StudentProgressResponse>(
    `/api/v1/student/sessions/${sessionId}/progress`,
    {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }
  );
}

/** Submit a quiz for grading. `answers` is one selected option index per question,
 *  positionally aligned to the quiz. No score is sent — the server grades against
 *  the stored answer key, which this app never receives before submitting. */
export async function submitQuizAttempt(
  sessionId: number,
  assetId: number,
  answers: number[]
) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<QuizAttemptResult>(
    `/api/v1/student/sessions/${sessionId}/assets/${assetId}/quiz-attempts`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      // apiRequest stringifies this itself — passing a string here would double-encode.
      body: { answers },
    }
  );
}
