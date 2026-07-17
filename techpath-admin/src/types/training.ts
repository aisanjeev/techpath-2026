// Training subsystem types. Mirrors app/schemas/training*.py on the backend.

export type AssetStorageKind = 'inline_text' | 'file' | 'link' | 'structured' | 'bundle';

export type AssetType =
  | 'markdown'
  | 'notes'
  | 'cheat_sheet'
  | 'code_snippet'
  | 'pdf'
  | 'ppt'
  | 'video'
  | 'notebook'
  | 'zip'
  | 'excel'
  | 'csv'
  | 'terminal_recording'
  | 'external_url'
  | 'github_repo'
  | 'youtube'
  | 'quiz'
  | 'assignment'
  | 'lab'
  | 'html_bundle';

export type ContentStatus = 'draft' | 'published' | 'archived';
export type DeliveryMode = 'online' | 'offline' | 'hybrid';
export type SessionStatus = 'scheduled' | 'live' | 'ended' | 'cancelled';

/** Registry entry served by GET /training/asset-types. */
export interface AssetTypeInfo {
  value: AssetType;
  label: string;
  storage_kind: AssetStorageKind;
  max_size_mb: number;
  allowed_content_types: string[];
  allowed_extensions: string[];
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
  explanation?: string | null;
}

export interface LectureAsset {
  id: number;
  public_id: string;
  title: string;
  asset_type: AssetType;
  description?: string | null;
  body?: string | null;
  media_file_id?: number | null;
  external_url?: string | null;
  config?: Record<string, unknown> | null;
  tags: string[];
  status: ContentStatus;
  is_active: boolean;
  storage_kind: AssetStorageKind;
  /** Resolved server-side from media_file_id — never construct this from config yourself,
   *  Azure Blob storage needs a signed URL the client can't produce. */
  file_url?: string | null;
  /** Also resolved server-side — a browser-side fetch of file_url would be blocked by
   *  the storage provider's CORS policy (Azure Blob grants none by default). */
  csv_preview?: {
    header: string[];
    rows: string[][];
    total_rows: number;
    truncated: boolean;
  } | null;
  created_at: string;
  updated_at: string;
}

export interface AssetUsage {
  module_id: number;
  module_title: string;
  program_id: number;
  program_title: string;
}

export interface ModuleAssetLink {
  id: number;
  asset_id: number;
  display_order: number;
  is_required: boolean;
  notes?: string | null;
  asset: LectureAsset;
}

export interface TrainingModule {
  id: number;
  program_id: number;
  title: string;
  slug: string;
  description?: string | null;
  display_order: number;
  estimated_minutes?: number | null;
  status: ContentStatus;
  asset_count: number;
  created_at: string;
  updated_at: string;
}

export interface TrainingModuleDetail extends TrainingModule {
  assets: ModuleAssetLink[];
}

export interface TrainingProgram {
  id: number;
  title: string;
  slug: string;
  summary?: string | null;
  description?: string | null;
  course_id?: number | null;
  delivery_mode: DeliveryMode;
  level?: string | null;
  duration?: string | null;
  cover_image?: string | null;
  tags: string[];
  status: ContentStatus;
  display_order: number;
  is_active: boolean;
  module_count: number;
  created_at: string;
  updated_at: string;
}

export interface TrainingProgramDetail extends TrainingProgram {
  modules: TrainingModule[];
}

export interface TrainingProgramCreate {
  title: string;
  slug: string;
  summary?: string;
  description?: string;
  course_id?: number | null;
  delivery_mode?: DeliveryMode;
  level?: string;
  duration?: string;
  cover_image?: string;
  tags?: string[];
  status?: ContentStatus;
  display_order?: number;
}

export type TrainingProgramUpdate = Partial<TrainingProgramCreate> & { is_active?: boolean };

export interface TrainingModuleCreate {
  title: string;
  slug: string;
  description?: string;
  display_order?: number;
  estimated_minutes?: number;
  status?: ContentStatus;
}

export type TrainingModuleUpdate = Partial<TrainingModuleCreate>;

export interface ReorderItem {
  id: number;
  display_order: number;
}

// ---------- roster mirror ----------

export interface TrainingBatch {
  id: number;
  external_id: string;
  name: string;
  code?: string | null;
  program_id?: number | null;
  program_title?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  timezone?: string | null;
  schedule?: {
    days?: string[];
    start_time?: string;
    end_time?: string;
    timezone?: string;
  } | null;
  status?: string | null;
  mode?: string | null;
  location?: string | null;
  trainer_email?: string | null;
  trainer_name?: string | null;
  student_count: number;
  course_ref?: string | null;
  synced_at?: string | null;
  external_updated_at?: string | null;
}

export interface TrainingStudent {
  id: number;
  external_id: string;
  name: string;
  email?: string | null;
  phone?: string | null;
  roll_no?: string | null;
  status?: string | null;
  photo_url?: string | null;
  enrolled_on?: string | null;
  synced_at?: string | null;
}

export interface SyncState {
  resource: string;
  cursor_updated_since?: string | null;
  last_run_at?: string | null;
  last_success_at?: string | null;
  last_status?: string | null;
  last_error?: string | null;
  records_processed: number;
  is_running: boolean;
}

export interface SyncStatus {
  provider: string;
  healthy: boolean;
  resources: SyncState[];
}

export interface SyncRunResult {
  success: boolean;
  results: Record<
    string,
    {
      resource: string;
      processed: number;
      created: number;
      updated: number;
      skipped_locked: boolean;
      error?: string | null;
    }
  >;
}

// ---------- trainer ----------

export interface TrainerBatchSummary {
  id: number;
  external_id: string;
  name: string;
  code?: string | null;
  status?: string | null;
  mode?: string | null;
  location?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  student_count: number;
  program_id?: number | null;
  program_title?: string | null;
  module_count: number;
}

export interface TrainingSession {
  id: number;
  batch_id: number;
  batch_name?: string | null;
  module_id?: number | null;
  module_title?: string | null;
  title?: string | null;
  scheduled_start?: string | null;
  scheduled_end?: string | null;
  status: SessionStatus;
  join_code?: string | null;
  started_at?: string | null;
  ended_at?: string | null;
  materials_published_at?: string | null;
}

export interface TrainingSessionCreate {
  batch_id: number;
  module_id?: number | null;
  title?: string;
  scheduled_start?: string | null;
  scheduled_end?: string | null;
}
