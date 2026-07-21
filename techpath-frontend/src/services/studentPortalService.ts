import { apiRequest } from '@utils/api';
import { getFirebaseAuth } from '@/lib/firebase';
import type {
  QuizAttemptResult,
  SelfPacedCourseDetailResponse,
  SelfPacedCourseListResponse,
  SelfPacedModuleMaterialsResponse,
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
      body: { answers },
    }
  );
}


// ---------------------------------------------------------------------------
// Self-paced courses
// ---------------------------------------------------------------------------

export async function getSelfPacedCourses() {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<SelfPacedCourseListResponse>('/api/v1/student/courses', {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getSelfPacedCourse(programId: number) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<SelfPacedCourseDetailResponse>(
    `/api/v1/student/courses/${programId}`,
    {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }
  );
}

export async function getSelfPacedModuleMaterials(
  programId: number,
  moduleId: number
) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<SelfPacedModuleMaterialsResponse>(
    `/api/v1/student/courses/${programId}/modules/${moduleId}/materials`,
    {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }
  );
}

export async function getSelfPacedModuleProgress(
  programId: number,
  moduleId: number
) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<StudentProgressResponse>(
    `/api/v1/student/courses/${programId}/modules/${moduleId}/progress`,
    {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }
  );
}

export async function updateSelfPacedModuleBookmark(
  programId: number,
  moduleId: number,
  lastAssetIndex: number
) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<{ success: boolean }>(
    `/api/v1/student/courses/${programId}/modules/${moduleId}/bookmark`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ last_asset_index: lastAssetIndex }),
    }
  );
}

export async function submitSelfPacedQuizAttempt(
  programId: number,
  moduleId: number,
  assetId: number,
  answers: number[]
) {
  const token = await getFirebaseAuth().currentUser?.getIdToken();
  if (!token) return { success: false as const, error: 'Not signed in' };
  return apiRequest<QuizAttemptResult>(
    `/api/v1/student/courses/${programId}/modules/${moduleId}/assets/${assetId}/quiz-attempts`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: { answers },
    }
  );
}
