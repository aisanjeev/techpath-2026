import { apiRequest } from '@utils/api';
import type {
  IdentifyResponse,
  JoinResponse,
  SessionStateResponse,
  QuizAttemptResult,
  TrainingSessionQuestionResponse,
} from '@/types/classroom';

/**
 * The student side of the live classroom. No Firebase account — a 6-digit join code
 * plus (ideally) a roster-email match, per the plan. Three of these five calls need the
 * short-lived classroom token identify() returns; apiRequest already supports a headers
 * override so this reuses it directly rather than the get/post wrappers, which don't
 * expose one.
 */

function authHeaders(token: string): Record<string, string> {
  return { Authorization: `Bearer ${token}` };
}

export async function joinClassroom(joinCode: string) {
  return apiRequest<JoinResponse>('/api/v1/classroom/join', {
    method: 'POST',
    body: { join_code: joinCode },
  });
}

export async function identify(params: {
  sessionId: number;
  email?: string;
  guestName?: string;
}) {
  return apiRequest<IdentifyResponse>('/api/v1/classroom/identify', {
    method: 'POST',
    body: {
      session_id: params.sessionId,
      email: params.email || undefined,
      guest_name: params.guestName || undefined,
    },
  });
}

export async function getState(sessionId: number, token: string) {
  return apiRequest<SessionStateResponse>(`/api/v1/classroom/${sessionId}/state`, {
    method: 'GET',
    headers: authHeaders(token),
  });
}

export async function setConfusion(sessionId: number, token: string, confused: boolean) {
  return apiRequest<SessionStateResponse>(`/api/v1/classroom/${sessionId}/confusion`, {
    method: 'POST',
    body: { confused },
    headers: authHeaders(token),
  });
}

export async function vote(sessionId: number, token: string, pollId: number, optionIndex: number) {
  return apiRequest<SessionStateResponse>(
    `/api/v1/classroom/${sessionId}/polls/${pollId}/vote`,
    {
      method: 'POST',
      body: { option_index: optionIndex },
      headers: authHeaders(token),
    }
  );
}

/** Submit a quiz asset during the live class, as a session participant.
 *
 *  Separate endpoint from the portal's — a live participant holds a classroom token,
 *  not a Firebase account, so the two identities can't share one route. Same grading
 *  and same response shape. A roster-matched participant's attempt is recorded; a
 *  guest is graded but not stored (no roster row to attach it to). */
export async function submitQuizAttempt(
  sessionId: number,
  token: string,
  assetId: number,
  answers: number[]
) {
  return apiRequest<QuizAttemptResult>(
    `/api/v1/classroom/${sessionId}/assets/${assetId}/quiz-attempts`,
    {
      method: 'POST',
      body: { answers },
      headers: authHeaders(token),
    }
  );
}

export async function setHandRaised(sessionId: number, token: string, raised: boolean) {
  return apiRequest<SessionStateResponse>(`/api/v1/classroom/${sessionId}/hand`, {
    method: 'POST',
    body: { raised },
    headers: authHeaders(token),
  });
}

/** Creates a doubt request so the trainer sees an "Enable Mic" button in the
 *  Doubt Audio Requests queue. Called alongside setHandRaised when raising. */
export async function requestDoubt(sessionId: number, token: string) {
  return apiRequest<SessionStateResponse>(`/api/v1/classroom/${sessionId}/doubts`, {
    method: 'POST',
    headers: authHeaders(token),
  });
}

export async function sendReaction(sessionId: number, token: string, emoji: string) {
  return apiRequest<{ message: string }>(`/api/v1/classroom/${sessionId}/reactions`, {
    method: 'POST',
    body: { emoji },
    headers: authHeaders(token),
  });
}

export async function getQuestions(sessionId: number, token: string) {
  return apiRequest<TrainingSessionQuestionResponse[]>(`/api/v1/classroom/${sessionId}/questions`, {
    method: 'GET',
    headers: authHeaders(token),
  });
}

export async function askQuestion(sessionId: number, token: string, questionText: string) {
  return apiRequest<TrainingSessionQuestionResponse>(`/api/v1/classroom/${sessionId}/questions`, {
    method: 'POST',
    body: { question_text: questionText },
    headers: authHeaders(token),
  });
}

export async function upvoteQuestion(sessionId: number, token: string, questionId: number) {
  return apiRequest<TrainingSessionQuestionResponse>(`/api/v1/classroom/${sessionId}/questions/${questionId}/upvote`, {
    method: 'POST',
    headers: authHeaders(token),
  });
}
