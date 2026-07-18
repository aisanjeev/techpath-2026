export interface ClassroomAsset {
  id: number;
  public_id: string;
  title: string;
  asset_type: string;
  description?: string | null;
  body?: string | null;
  media_file_id?: number | null;
  external_url?: string | null;
  config?: Record<string, unknown> | null;
  tags: string[];
  status: string;
  is_active: boolean;
  storage_kind: 'inline_text' | 'file' | 'link' | 'structured' | 'bundle';
  file_url?: string | null;
  csv_preview?: {
    header: string[];
    rows: string[][];
    total_rows: number;
    truncated: boolean;
  } | null;
  created_at: string;
  updated_at: string;
}

export interface JoinResponse {
  session_id: number;
  batch_name: string;
  session_title?: string | null;
  module_title?: string | null;
  status: string;
}

export interface IdentifyResponse {
  matched: boolean;
  token: string | null;
  display_name: string | null;
}

export interface PollStateView {
  id: number;
  question: string;
  options: string[];
  status: 'open' | 'closed';
  my_vote?: number | null;
  results?: Record<number, number> | null;
  correct_option_index?: number | null;
}

export interface CodeStateView {
  language: string;
  content: string;
}

export interface TimerStateView {
  duration_seconds: number;
  started_at: string;
}

/** Participant-facing live audio/video — whep_url/hls_url only, never a publish URL.
 *  Absent (null on the response) until the trainer has started publishing media. */
export interface MediaStateView {
  whep_url?: string | null;
  hls_url?: string | null;
  /** False until the trainer turns their camera/mic on — the video tile is not rendered
   *  at all in that case, since there is nothing to wait for. */
  broadcasting: boolean;
  mic_muted: boolean;
  camera_off: boolean;
  screen_sharing: boolean;
}

export interface SessionStateResponse {
  session_id: number;
  title?: string | null;
  status: string;
  batch_name: string;
  module_title?: string | null;
  current_asset?: ClassroomAsset | null;
  open_poll?: PollStateView | null;
  code?: CodeStateView | null;
  my_confusion: boolean;
  presence: { online: number };
  timer?: TimerStateView | null;
  media?: MediaStateView | null;
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

export type ClassroomEvent =
  | { type: 'roster_changed'; payload: unknown }
  | { type: 'poll_open'; payload: { id: number; question: string; options: string[] } }
  | {
      type: 'poll_closed';
      payload: {
        id: number;
        results: Record<number, number>;
        total_votes: number;
        correct_option_index?: number | null;
      };
    }
  | { type: 'poll_vote_cast'; payload: { poll_id: number } }
  | { type: 'session_ended'; payload: Record<string, never> }
  | { type: 'slide_change'; payload: { asset: ClassroomAsset } }
  | { type: 'code_update'; payload: { language: string; content: string } }
  | { type: 'timer_started'; payload: TimerStateView }
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
  | { type: 'questions_visibility_changed'; payload: { questions_are_public: boolean } };
