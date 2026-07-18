import type { ClassroomAsset } from './classroom';

/**
 * The student materials portal — a durable, Google-authenticated identity system,
 * deliberately separate from the live classroom's 6-digit-code + short-lived-token
 * flow (see classroom.ts). A student who attended a published session signs in here
 * with a real Firebase/Google account, days or weeks later, to view/download whatever
 * the trainer has published for that session.
 *
 * The one thing genuinely shared with the live classroom is the asset shape itself —
 * both surfaces serialize assets via the same backend `asset_to_response()`, so
 * `ClassroomAsset` is reused as-is here rather than duplicated.
 */

export interface StudentLoginResponse {
  display_name: string;
  email: string | null;
}

export interface StudentSessionSummary {
  session_id: number;
  title: string | null;
  batch_name: string;
  module_title: string | null;
  session_date: string;
  published_at: string;
}

export interface StudentSessionListResponse {
  sessions: StudentSessionSummary[];
}

/** The class's recorded replay, if it ever had live media. `watch_url` is always
 *  present once this object exists, but only actually playable once `status ===
 *  'ready'` — show a "still processing" state until then. */
export interface RecordingView {
  status: 'processing' | 'ready' | 'failed';
  watch_url: string | null;
}

export interface StudentSessionMaterialsResponse {
  session_id: number;
  title: string | null;
  batch_name: string;
  module_title: string | null;
  published_at: string;
  assets: ClassroomAsset[];
  recording: RecordingView | null;
}

/* -------------------------------------------------------------------------
 * Graded quizzes
 *
 * QuizAttemptResult / QuizQuestionFeedback are declared in classroom.ts and
 * re-exported here: both the portal and the live classroom submit quizzes, so
 * the shape belongs on the shared base module rather than on this one.
 * ---------------------------------------------------------------------- */

export type { QuizAttemptResult, QuizQuestionFeedback } from './classroom';

export interface StudentProgressItem {
  asset_id: number;
  index: number;
  is_quiz: boolean;
  /** Null for non-quiz items — they have nothing to pass, which is different
   *  from a quiz that has been failed. */
  passed: boolean | null;
  locked: boolean;
  best_score: number | null;
  total_questions: number | null;
  attempt_count: number | null;
}

export interface StudentProgressResponse {
  session_id: number;
  /** Index of the first quiz without a passing attempt; equals items.length when
   *  there is none. The item AT this index is reachable — later ones are not. */
  first_locked_index: number;
  items: StudentProgressItem[];
}
