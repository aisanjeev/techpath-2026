import { apiClient, handleApiError } from '@/lib/api-client';
import type {
  TrainerBatchSummary,
  TrainingModule,
  TrainingModuleDetail,
  TrainingSession,
  TrainingSessionCreate,
  TrainingStudent,
} from '@/types/training';
import type {
  ActionResponse,
  AttendanceReportResponse,
  ConfusionTimelineResponse,
  PollHistoryResponse,
  PollResultsResponse,
  RosterResponse,
  WsTokenResponse,
} from '@/types/classroom';

/** Trainer-scoped views. The backend restricts these to the signed-in trainer's own
 *  batches, matched by email; admins are allowed through for support. */
export const trainerService = {
  async myBatches(): Promise<TrainerBatchSummary[]> {
    try {
      const response = await apiClient.get<TrainerBatchSummary[]>('/api/v1/trainer/me/batches');
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async sessionsToday(): Promise<TrainingSession[]> {
    try {
      const response = await apiClient.get<TrainingSession[]>(
        '/api/v1/trainer/me/sessions/today'
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBatch(id: number): Promise<TrainerBatchSummary> {
    try {
      const response = await apiClient.get<TrainerBatchSummary>(`/api/v1/trainer/batches/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBatchStudents(id: number): Promise<TrainingStudent[]> {
    try {
      const response = await apiClient.get<TrainingStudent[]>(
        `/api/v1/trainer/batches/${id}/students`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Modules available to present, via the batch's linked programme. */
  async getBatchModules(id: number): Promise<TrainingModule[]> {
    try {
      const response = await apiClient.get<TrainingModule[]>(
        `/api/v1/trainer/batches/${id}/modules`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getBatchSessions(id: number): Promise<TrainingSession[]> {
    try {
      const response = await apiClient.get<TrainingSession[]>(
        `/api/v1/trainer/batches/${id}/sessions`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createSession(data: TrainingSessionCreate): Promise<TrainingSession> {
    try {
      const response = await apiClient.post<TrainingSession>('/api/v1/trainer/sessions', data);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getSession(id: number): Promise<TrainingSession> {
    try {
      const response = await apiClient.get<TrainingSession>(`/api/v1/trainer/sessions/${id}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Go live: flips status and mints the join code students will use. */
  async startSession(id: number, moduleId?: number | null): Promise<TrainingSession> {
    try {
      const response = await apiClient.post<TrainingSession>(
        `/api/v1/trainer/sessions/${id}/start`,
        { module_id: moduleId ?? null }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getModule(id: number): Promise<TrainingModuleDetail> {
    try {
      const response = await apiClient.get<TrainingModuleDetail>(
        `/api/v1/trainer/modules/${id}`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async endSession(id: number): Promise<TrainingSession> {
    try {
      const response = await apiClient.post<TrainingSession>(
        `/api/v1/trainer/sessions/${id}/end`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Makes every asset in this session's module visible in the student portal, to
   *  everyone who attended. Only valid once the session has ended. */
  async publishMaterials(id: number): Promise<TrainingSession> {
    try {
      const response = await apiClient.post<TrainingSession>(
        `/api/v1/trainer/sessions/${id}/materials/publish`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async unpublishMaterials(id: number): Promise<TrainingSession> {
    try {
      const response = await apiClient.post<TrainingSession>(
        `/api/v1/trainer/sessions/${id}/materials/unpublish`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Short-lived, session-scoped — a native WebSocket handshake can't carry an
   *  Authorization header, so this is what goes in the connection's query string
   *  instead of the real Firebase ID token. */
  async mintWsToken(sessionId: number): Promise<WsTokenResponse> {
    try {
      const response = await apiClient.post<WsTokenResponse>(
        `/api/v1/trainer/sessions/${sessionId}/ws-token`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Changes what students see. Broadcasts immediately over the classroom socket. */
  async setSlide(sessionId: number, assetId: number): Promise<void> {
    try {
      await apiClient.post(`/api/v1/trainer/sessions/${sessionId}/slide`, { asset_id: assetId });
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Live tally while the poll is still open. */
  async getPollResults(sessionId: number, pollId: number): Promise<PollResultsResponse> {
    try {
      const response = await apiClient.get<PollResultsResponse>(
        `/api/v1/trainer/sessions/${sessionId}/polls/${pollId}`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async createPoll(
    sessionId: number,
    question: string,
    options: string[]
  ): Promise<PollResultsResponse> {
    try {
      const response = await apiClient.post<PollResultsResponse>(
        `/api/v1/trainer/sessions/${sessionId}/polls`,
        { question, options }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async closePoll(sessionId: number, pollId: number): Promise<PollResultsResponse> {
    try {
      const response = await apiClient.post<PollResultsResponse>(
        `/api/v1/trainer/sessions/${sessionId}/polls/${pollId}/close`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** The client is expected to debounce keystrokes before calling this. */
  async updateLiveCode(sessionId: number, language: string, content: string): Promise<void> {
    try {
      await apiClient.post(`/api/v1/trainer/sessions/${sessionId}/code`, { language, content });
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getRoster(sessionId: number): Promise<RosterResponse> {
    try {
      const response = await apiClient.get<RosterResponse>(
        `/api/v1/trainer/sessions/${sessionId}/roster`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async kickParticipant(sessionId: number, participantId: number): Promise<ActionResponse> {
    try {
      const response = await apiClient.post<ActionResponse>(
        `/api/v1/trainer/sessions/${sessionId}/participants/${participantId}/kick`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async lowerHand(sessionId: number, participantId: number): Promise<ActionResponse> {
    try {
      const response = await apiClient.post<ActionResponse>(
        `/api/v1/trainer/sessions/${sessionId}/participants/${participantId}/lower-hand`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async startTimer(sessionId: number, durationSeconds: number): Promise<ActionResponse> {
    try {
      const response = await apiClient.post<ActionResponse>(
        `/api/v1/trainer/sessions/${sessionId}/timer/start`,
        { duration_seconds: durationSeconds }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async cancelTimer(sessionId: number): Promise<ActionResponse> {
    try {
      const response = await apiClient.post<ActionResponse>(
        `/api/v1/trainer/sessions/${sessionId}/timer/cancel`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  /** Launches a poll pre-filled from a quiz asset's question so the trainer doesn't
   *  have to retype it — returns the same shape as createPoll. */
  async createPollFromQuiz(
    sessionId: number,
    assetId: number,
    questionIndex: number
  ): Promise<PollResultsResponse> {
    try {
      const response = await apiClient.post<PollResultsResponse>(
        `/api/v1/trainer/sessions/${sessionId}/polls/from-quiz`,
        { asset_id: assetId, question_index: questionIndex }
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getAttendanceReport(sessionId: number): Promise<AttendanceReportResponse> {
    try {
      const response = await apiClient.get<AttendanceReportResponse>(
        `/api/v1/trainer/sessions/${sessionId}/attendance`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getPollHistory(sessionId: number): Promise<PollHistoryResponse> {
    try {
      const response = await apiClient.get<PollHistoryResponse>(
        `/api/v1/trainer/sessions/${sessionId}/polls/history`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  async getConfusionTimeline(sessionId: number): Promise<ConfusionTimelineResponse> {
    try {
      const response = await apiClient.get<ConfusionTimelineResponse>(
        `/api/v1/trainer/sessions/${sessionId}/confusion-timeline`
      );
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};
