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
