import type { LectureAsset } from '@/types/training';

export interface RosterParticipant {
  id: number;
  display_name: string;
  is_guest: boolean;
  is_online: boolean;
  is_confused: boolean;
  first_joined_at: string;
  last_seen_at: string;
  hand_raised: boolean;
  hand_raised_at: string | null;
}

export interface ConfusionSummary {
  online: number;
  confused: number;
  ratio: number;
}

/** One entry in the trainer's raise-hand queue — already sorted first-raised-first by
 *  the backend. */
export interface HandRaisedEntry {
  participant_id: number;
  display_name: string;
  hand_raised_at: string | null;
}

export interface DoubtRequest {
  id: number;
  participant_id: number;
  display_name: string;
  status: 'pending' | 'approved' | 'completed';
  requested_at: string;
  whep_url?: string;
}

export interface TimerView {
  duration_seconds: number;
  started_at: string;
}

export interface RosterResponse {
  participants: RosterParticipant[];
  confusion: ConfusionSummary;
  hands_raised: HandRaisedEntry[];
  doubt_requests: DoubtRequest[];
  /** A timer already in progress, if any — read on mount so a page refresh doesn't
   *  lose track of a running countdown. Live updates after that arrive over the
   *  timer_started / timer_cancelled WebSocket events instead of this field. */
  timer: TimerView | null;
}

export interface PollResultsResponse {
  id: number;
  question: string;
  options: string[];
  status: 'open' | 'closed';
  results: Record<number, number>;
  total_votes: number;
  /** Set only for a poll launched from a quiz question; null for an ordinary poll.
   *  The backend never sends this while the poll is open — only trust/show it once
   *  status === 'closed'. */
  correct_option_index: number | null;
  created_at: string;
  closed_at?: string | null;
}

export interface WsTokenResponse {
  token: string;
  expires_in_minutes: number;
}

/** Shared ack shape for trainer actions that don't return a resource body (kick,
 *  lower-hand, timer start/cancel) — just a confirmation. */
export interface ActionResponse {
  success: boolean;
  message: string;
}

export interface AttendanceRow {
  participant_id: number;
  display_name: string;
  is_guest: boolean;
  student_id: number | null;
  first_joined_at: string;
  last_seen_at: string;
  left_at: string | null;
  is_online: boolean;
  duration_minutes: number;
}

export interface AttendanceReportResponse {
  session_id: number;
  session_title: string | null;
  total_participants: number;
  rows: AttendanceRow[];
}

export interface PollHistoryEntry {
  id: number;
  question: string;
  options: string[];
  status: 'open' | 'closed';
  results: Record<number, number>;
  total_votes: number;
  correct_option_index: number | null;
  created_at: string;
  closed_at: string | null;
}

export interface PollHistoryResponse {
  session_id: number;
  polls: PollHistoryEntry[];
}

/* ---------- quiz results ---------- */

export interface QuizStudentResult {
  student_id: number;
  name: string;
  email: string | null;
  attempt_count: number;
  best_score: number | null;
  total_questions: number | null;
  passed: boolean;
  last_attempted_at: string | null;
  /** The best attempt was graded against a different question count than the quiz
   *  has now. Catches added/removed questions, not a reworded one. */
  is_stale: boolean;
}

export interface QuizQuestionStat {
  index: number;
  question: string;
  correct_count: number;
  attempted_count: number;
}

export interface QuizResultSummary {
  asset_id: number;
  title: string;
  total_questions: number;
  pass_mark: number;
  attempted_count: number;
  passed_count: number;
  roster_size: number;
  question_stats: QuizQuestionStat[];
  /** Every roster student, including those who never attempted — those carry
   *  attempt_count 0 and null scores. */
  students: QuizStudentResult[];
}

export interface QuizResultsResponse {
  session_id: number;
  quizzes: QuizResultSummary[];
}

export interface ConfusionTimelinePoint {
  timestamp: string;
  online: number;
  confused: number;
  ratio: number;
}

export interface ConfusionTimelineResponse {
  session_id: number;
  points: ConfusionTimelinePoint[];
}

export interface TrainingSessionQuestionResponse {
  id: number;
  session_id: number;
  student_id: number | null;
  student_name: string | null;
  question_text: string;
  is_answered: boolean;
  upvotes: number;
  created_at: string;
}

/** The roster_changed WS payload mirrors the REST roster response but isn't byte-for-
 *  byte identical to it: the raised-hands list is named hands_raised_queue on the wire
 *  (vs. hands_raised from GET .../roster) and it carries no `timer` field — ongoing
 *  timer state travels over its own timer_started / timer_cancelled events instead, the
 *  REST roster's `timer` is only for resuming state on initial load. */
export interface RosterChangedPayload {
  participants: RosterParticipant[];
  confusion: ConfusionSummary;
  hands_raised_queue: HandRaisedEntry[];
}

/** Every shape the classroom WebSocket can deliver. The trainer panel acts on
 * roster_changed, poll_open, poll_closed, poll_vote_cast, timer_started,
 * timer_cancelled and reaction — slide_change and code_update are things the trainer
 * broadcasts, not receives, and participant_kicked is only actionable on the student
 * app (the roster_changed broadcast that follows a kick already updates this view) —
 * but all are typed here since the socket is shared wire format with the student app. */
export type ClassroomEvent =
  | { type: 'roster_changed'; payload: RosterChangedPayload }
  | { type: 'poll_open'; payload: { id: number; question: string; options: string[] } }
  | {
      type: 'poll_closed';
      payload: { id: number; results: Record<number, number>; total_votes: number };
    }
  | { type: 'poll_vote_cast'; payload: { poll_id: number } }
  | { type: 'session_ended'; payload: Record<string, never> }
  | { type: 'slide_change'; payload: { asset: LectureAsset } }
  | { type: 'code_update'; payload: { language: string; content: string } }
  | { type: 'timer_started'; payload: TimerView }
  | { type: 'timer_cancelled'; payload: Record<string, never> }
  | { type: 'reaction'; payload: { emoji: string; display_name: string } }
  | { type: 'participant_kicked'; payload: { participant_key: string } }
  | {
      type: 'media_state_changed';
      payload: {
        broadcasting: boolean;
        mic_muted: boolean;
        camera_off: boolean;
        screen_sharing: boolean;
      };
    }
  | { type: 'question_asked'; payload: TrainingSessionQuestionResponse }
  | { type: 'question_upvoted'; payload: { question_id: number; upvotes: number } }
  | { type: 'question_answered'; payload: { question_id: number } }
  | { type: 'questions_visibility_changed'; payload: { questions_are_public: boolean } }
  | {
      type: 'quiz_attempt_submitted';
      payload: {
        asset_id: number;
        participant_id: number;
        display_name: string;
        score: number;
        total_questions: number;
        passed: boolean;
        recorded: boolean;
      };
    }
  | { type: 'doubt_requested'; payload: { doubt_id: number; participant_id: number; display_name: string; } }
  // These mirror what trainer.py's approve_doubt/complete_doubt actually publish — a
  // flat payload keyed by `doubt_id`, NOT a serialized DoubtRequest (which keys on `id`).
  | { type: 'doubt_approved'; payload: { doubt_id: number; participant_id: number; whip_url: string; whep_url: string; } }
  | { type: 'doubt_completed'; payload: { doubt_id: number; participant_id: number; } };
