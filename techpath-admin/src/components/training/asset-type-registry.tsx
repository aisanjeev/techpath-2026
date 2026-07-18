import {
  FileText,
  StickyNote,
  ScrollText,
  Code2,
  FileType2,
  Presentation,
  Video,
  NotebookPen,
  FileArchive,
  Sheet,
  Table2,
  TerminalSquare,
  Link2,
  Github,
  Youtube,
  ListChecks,
  ClipboardList,
  FlaskConical,
  CodeXml,
} from 'lucide-react';
import type { AssetStorageKind, AssetType } from '@/types/training';

/**
 * Frontend mirror of ASSET_TYPE_RULES in app/core/constants.py.
 *
 * One registry drives the type picker, every list icon, the form switch and the
 * renderer switch — so a new type is added in one place, not five. The backend serves
 * the authoritative rules at GET /training/asset-types (limits, MIME types); this file
 * only adds what the API has no opinion about: icons and human copy.
 */

export interface AssetTypeMeta {
  label: string;
  kind: AssetStorageKind;
  icon: React.ComponentType<{ className?: string }>;
  hint: string;
}

export const ASSET_TYPE_META: Record<AssetType, AssetTypeMeta> = {
  markdown: {
    label: 'Markdown',
    kind: 'inline_text',
    icon: FileText,
    hint: 'Rich lesson content written in Markdown',
  },
  notes: {
    label: 'Notes',
    kind: 'inline_text',
    icon: StickyNote,
    hint: 'Short notes or talking points',
  },
  cheat_sheet: {
    label: 'Cheat Sheet',
    kind: 'inline_text',
    icon: ScrollText,
    hint: 'Quick reference students can keep',
  },
  code_snippet: {
    label: 'Code Snippet',
    kind: 'inline_text',
    icon: Code2,
    hint: 'A block of code with syntax highlighting',
  },
  pdf: { label: 'PDF', kind: 'file', icon: FileType2, hint: 'A PDF document' },
  ppt: {
    label: 'Presentation',
    kind: 'file',
    icon: Presentation,
    hint: 'PowerPoint slides (.ppt, .pptx)',
  },
  video: { label: 'Video', kind: 'file', icon: Video, hint: 'A recorded video lesson' },
  notebook: {
    label: 'Notebook',
    kind: 'file',
    icon: NotebookPen,
    hint: 'A Jupyter notebook (.ipynb)',
  },
  zip: { label: 'Archive', kind: 'file', icon: FileArchive, hint: 'A zip of course files' },
  excel: { label: 'Spreadsheet', kind: 'file', icon: Sheet, hint: 'Excel workbook' },
  csv: { label: 'CSV', kind: 'file', icon: Table2, hint: 'Comma-separated data' },
  terminal_recording: {
    label: 'Terminal Recording',
    kind: 'file',
    icon: TerminalSquare,
    hint: 'An asciinema cast of a terminal session',
  },
  external_url: {
    label: 'External Link',
    kind: 'link',
    icon: Link2,
    hint: 'Any link students should open',
  },
  github_repo: {
    label: 'GitHub Repo',
    kind: 'link',
    icon: Github,
    hint: 'A repository to clone or browse',
  },
  youtube: { label: 'YouTube', kind: 'link', icon: Youtube, hint: 'A YouTube video' },
  quiz: {
    label: 'Quiz',
    kind: 'structured',
    icon: ListChecks,
    hint: 'Multiple-choice questions with answers',
  },
  assignment: {
    label: 'Assignment',
    kind: 'structured',
    icon: ClipboardList,
    hint: 'Work students complete and submit',
  },
  lab: {
    label: 'Lab',
    kind: 'structured',
    icon: FlaskConical,
    hint: 'A guided hands-on exercise',
  },
  html_bundle: {
    label: 'HTML Bundle',
    kind: 'bundle',
    icon: CodeXml,
    hint: 'A standalone HTML/CSS/JS lecture',
  },
};

export const STORAGE_KIND_LABEL: Record<AssetStorageKind, string> = {
  inline_text: 'Written content',
  file: 'Uploaded file',
  link: 'Link',
  structured: 'Interactive',
  bundle: 'HTML bundle',
};

export function assetMeta(type: AssetType): AssetTypeMeta {
  return (
    ASSET_TYPE_META[type] ?? {
      label: type,
      kind: 'inline_text',
      icon: FileText,
      hint: '',
    }
  );
}

export function assetIcon(type: AssetType) {
  return assetMeta(type).icon;
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

export function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}
