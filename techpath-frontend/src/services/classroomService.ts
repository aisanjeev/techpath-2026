import { apiRequest } from '@utils/api';
import type {
  IdentifyResponse,
  JoinResponse,
  SessionStateResponse,
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

export async function setHandRaised(sessionId: number, token: string, raised: boolean) {
  return apiRequest<SessionStateResponse>(`/api/v1/classroom/${sessionId}/hand`, {
    method: 'POST',
    body: { raised },
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
