'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Plus,
  Trash2,
  Check,
  Copy,
  ExternalLink,
  Github,
  Youtube,
  Download,
  Info,
  Calendar,
  Eye,
  Settings,
  HelpCircle,
  Play,
  RotateCcw,
  CheckCircle,
  XCircle,
  Laptop,
  Smartphone,
  Sparkles,
  BookOpen,
  Sun,
  Moon,
  Upload,
  FileJson,
  X,
  Tag
} from 'lucide-react';
import toast from 'react-hot-toast';
import { marked } from 'marked';

import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { FormField } from '@/components/ui/FormField';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Spinner } from '@/components/ui/Spinner';
import { AssetFileUpload } from '@/components/training/AssetFileUpload';
import { CodeEditor, type CodeEditorHandle } from '@/components/editors/CodeEditor';
import { ImagePickerModal } from '@/components/ui/ImagePickerModal';
import {
  ASSET_TYPE_META,
  STORAGE_KIND_LABEL,
  assetMeta,
  formatBytes,
} from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import { cn } from '@/lib/utils/cn';
import type {
  AssetType,
  AssetTypeInfo,
  LectureAsset,
  QuizQuestion,
} from '@/types/training';

interface LectureAssetFormProps {
  asset?: LectureAsset;
}

const CODE_LANGUAGES = [
  'python',
  'javascript',
  'typescript',
  'java',
  'csharp',
  'go',
  'rust',
  'sql',
  'bash',
  'html',
  'css',
  'json',
  'yaml',
];

// Color mapping for asset types for enhanced branding/icons
const TYPE_COLOR_MAP: Record<string, { bg: string; text: string; border: string }> = {
  markdown: { bg: 'bg-emerald-50 text-emerald-600 border-emerald-200', text: 'text-emerald-700', border: 'border-emerald-500' },
  notes: { bg: 'bg-amber-50 text-amber-600 border-amber-200', text: 'text-amber-700', border: 'border-amber-500' },
  cheat_sheet: { bg: 'bg-orange-50 text-orange-600 border-orange-200', text: 'text-orange-700', border: 'border-orange-500' },
  code_snippet: { bg: 'bg-blue-50 text-blue-600 border-blue-200', text: 'text-blue-700', border: 'border-blue-500' },
  pdf: { bg: 'bg-red-50 text-red-600 border-red-200', text: 'text-red-700', border: 'border-red-500' },
  ppt: { bg: 'bg-rose-50 text-rose-600 border-rose-200', text: 'text-rose-700', border: 'border-rose-500' },
  video: { bg: 'bg-purple-50 text-purple-600 border-purple-200', text: 'text-purple-700', border: 'border-purple-500' },
  notebook: { bg: 'bg-violet-50 text-violet-600 border-violet-200', text: 'text-violet-700', border: 'border-violet-500' },
  zip: { bg: 'bg-indigo-50 text-indigo-600 border-indigo-200', text: 'text-indigo-700', border: 'border-indigo-500' },
  excel: { bg: 'bg-teal-50 text-teal-600 border-teal-200', text: 'text-teal-700', border: 'border-teal-500' },
  csv: { bg: 'bg-cyan-50 text-cyan-600 border-cyan-200', text: 'text-cyan-700', border: 'border-cyan-500' },
  terminal_recording: { bg: 'bg-slate-50 text-slate-700 border-slate-200', text: 'text-slate-900', border: 'border-slate-500' },
  external_url: { bg: 'bg-pink-50 text-pink-600 border-pink-200', text: 'text-pink-700', border: 'border-pink-500' },
  github_repo: { bg: 'bg-gray-100 text-gray-800 border-gray-200', text: 'text-gray-900', border: 'border-gray-900' },
  youtube: { bg: 'bg-red-50 text-red-600 border-red-200', text: 'text-red-700', border: 'border-red-500' },
  quiz: { bg: 'bg-fuchsia-50 text-fuchsia-600 border-fuchsia-200', text: 'text-fuchsia-700', border: 'border-fuchsia-500' },
  assignment: { bg: 'bg-purple-50 text-purple-600 border-purple-200', text: 'text-purple-700', border: 'border-purple-500' },
  lab: { bg: 'bg-sky-50 text-sky-600 border-sky-200', text: 'text-sky-700', border: 'border-sky-500' },
  html_bundle: { bg: 'bg-indigo-50 text-indigo-600 border-indigo-200', text: 'text-indigo-700', border: 'border-indigo-500' },
};

export function LectureAssetForm({ asset }: LectureAssetFormProps) {
  const router = useRouter();
  const isEdit = !!asset;

  const [types, setTypes] = useState<AssetTypeInfo[]>([]);
  const [loadingTypes, setLoadingTypes] = useState(true);
  const [saving, setSaving] = useState(false);

  // Form State
  const [assetType, setAssetType] = useState<AssetType>(asset?.asset_type ?? 'markdown');
  const [title, setTitle] = useState(asset?.title ?? '');
  const [description, setDescription] = useState(asset?.description ?? '');
  const [tags, setTags] = useState<string[]>(asset?.tags ?? []);
  const [tagInput, setTagInput] = useState('');
  const [existingTags, setExistingTags] = useState<string[]>([]);
  const [status, setStatus] = useState(asset?.status ?? 'draft');

  // Content Payload State
  const [body, setBody] = useState(asset?.body ?? '');
  const [language, setLanguage] = useState(
    (asset?.config?.language as string) ?? 'python'
  );
  const [externalUrl, setExternalUrl] = useState(asset?.external_url ?? '');
  const [file, setFile] = useState<{ id: number; filename: string; size: number; url?: string } | null>(
    asset?.media_file_id
      ? { id: asset.media_file_id, filename: asset?.config?.filename as string ?? 'Attached file', size: asset?.config?.size as number ?? 0 }
      : null
  );
  const [questions, setQuestions] = useState<QuizQuestion[]>(
    (asset?.config?.questions as QuizQuestion[]) ?? [
      { question: '', options: ['', ''], correct_index: 0, explanation: '' },
    ]
  );
  const [passMark, setPassMark] = useState<number>(
    (asset?.config?.pass_mark_percent as number) ?? 60
  );
  const [instructions, setInstructions] = useState(
    (asset?.config?.instructions as string) ?? ''
  );
  const [dueInDays, setDueInDays] = useState<string>(
    asset?.config?.due_in_days != null ? String(asset.config.due_in_days) : ''
  );
  const [objective, setObjective] = useState((asset?.config?.objective as string) ?? '');
  const [steps, setSteps] = useState<{title: string, instructions: string}[]>(() => {
    const rawSteps = asset?.config?.steps;
    if (Array.isArray(rawSteps)) {
      return rawSteps.map((s) => {
        if (typeof s === 'string') return { title: s, instructions: '' };
        if (s && typeof s === 'object') {
          return { title: String((s as any).title || ''), instructions: String((s as any).instructions || '') };
        }
        return { title: String(s || ''), instructions: '' };
      });
    }
    return [{ title: '', instructions: '' }];
  });

  const [showImagePicker, setShowImagePicker] = useState(false);
  const codeEditorRef = useRef<CodeEditorHandle>(null);

  const [errors, setErrors] = useState<Record<string, string>>({});

  // Interactive Preview States
  const [previewTheme, setPreviewTheme] = useState<'light' | 'dark'>('light');
  const [previewDevice, setPreviewDevice] = useState<'desktop' | 'mobile'>('desktop');
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [completedSteps, setCompletedSteps] = useState<Record<number, boolean>>({});

  const quizFileInputRef = useRef<HTMLInputElement>(null);
  const labFileInputRef = useRef<HTMLInputElement>(null);

  const handleQuizFileImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const json = JSON.parse(ev.target?.result as string);
        const raw: unknown[] = Array.isArray(json) ? json : json.questions;
        if (!Array.isArray(raw) || raw.length === 0) {
          toast.error('No questions found. Ensure file has a "questions" array.');
          return;
        }
        const parsed: QuizQuestion[] = raw.map((item: any) => ({
          question: String(item.question || ''),
          options: Array.isArray(item.options) ? item.options.map(String) : ['', ''],
          correct_index: typeof item.correct_index === 'number' ? item.correct_index : 0,
          explanation: String(item.explanation || ''),
        }));
        setQuestions(parsed);
        toast.success(`Imported ${parsed.length} question${parsed.length > 1 ? 's' : ''} from file`);
      } catch {
        toast.error('Invalid JSON file. Check the format and try again.');
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  const handleLabFileImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const json = JSON.parse(ev.target?.result as string);
        const rawSteps: unknown[] = Array.isArray(json) ? json : json.steps;
        if (!Array.isArray(rawSteps) || rawSteps.length === 0) {
          toast.error('No steps found. Ensure file has a "steps" array.');
          return;
        }
        const parsed = rawSteps.map((item: any) => ({
          title: String(item.title || item || ''),
          instructions: String(item.instructions || ''),
        }));
        setSteps(parsed);
        if (json.objective) setObjective(String(json.objective));
        if (json.title && !title) setTitle(String(json.title));
        if (json.description && !description) setDescription(String(json.description));
        if (Array.isArray(json.tags) && tags.length === 0) setTags(json.tags.map(String));
        toast.success(`Imported ${parsed.length} step${parsed.length > 1 ? 's' : ''} from file`);
      } catch {
        toast.error('Invalid JSON file. Check the format and try again.');
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  const downloadLabSample = () => {
    const sample = {
      title: "Explore Your Computer's Hardware",
      description: "Use built-in Windows tools to discover hardware specifications",
      objective: "Students will use Task Manager and System Information to identify CPU, RAM, storage, and GPU specs",
      steps: [
        {
          title: "Open System Information",
          instructions: "Press **Win + R**, type `msinfo32`, and press Enter.\n\nFind and write down:\n- **OS Name**\n- **Processor**\n- **Installed Physical Memory (RAM)**\n- **BaseBoard Manufacturer**"
        },
        {
          title: "Explore Task Manager Performance",
          instructions: "Press **Ctrl + Shift + Esc** to open Task Manager.\n\nClick the **Performance** tab and note:\n1. **CPU** — speed, cores, logical processors\n2. **Memory** — total RAM, in use, available\n3. **Disk** — SSD or HDD, read/write speeds\n4. **GPU** — graphics card name and dedicated memory"
        }
      ]
    };
    const blob = new Blob([JSON.stringify(sample, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'lab-sample.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadQuizSample = () => {
    const sample = {
      questions: [
        {
          question: "What does CPU stand for?",
          options: [
            "Computer Personal Unit",
            "Central Processing Unit",
            "Central Program Utility",
            "Computer Processing Unit"
          ],
          correct_index: 1,
          explanation: "CPU = Central Processing Unit. It is called the brain of the computer."
        },
        {
          question: "RAM is which type of memory?",
          options: [
            "Permanent memory",
            "Temporary memory (lost when power off)",
            "External memory",
            "Read-only memory"
          ],
          correct_index: 1,
          explanation: "RAM (Random Access Memory) is volatile — it loses all data when turned off."
        }
      ]
    };
    const blob = new Blob([JSON.stringify(sample, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'quiz-sample.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    trainingService
      .assetTypes()
      .then(setTypes)
      .catch(() => toast.error('Could not load asset types'))
      .finally(() => setLoadingTypes(false));
    trainingService.assetTags().then(setExistingTags).catch(() => undefined);
  }, []);

  // Fetch blob content for markdown assets that use media files instead of DB body
  useEffect(() => {
    if (isEdit && assetType === 'markdown' && !asset?.body && asset?.file_url) {
      fetch(asset.file_url)
        .then(res => res.text())
        .then(text => setBody(text))
        .catch(err => console.error('Failed to load markdown blob:', err));
    }
  }, [isEdit, assetType, asset?.body, asset?.file_url]);

  // Reset interactive preview states when asset type or settings change
  useEffect(() => {
    setQuizAnswers({});
    setQuizSubmitted(false);
    setCompletedSteps({});
  }, [assetType]);

  const rules = useMemo(() => types.find((t) => t.value === assetType), [types, assetType]);
  const kind = rules?.storage_kind ?? assetMeta(assetType).kind;

  const grouped = useMemo(() => {
    const out: Record<string, AssetTypeInfo[]> = {};
    for (const t of types) {
      (out[t.storage_kind] ??= []).push(t);
    }
    return out;
  }, [types]);

  // Live parsed Markdown cache
  const renderedBodyMarkdown = useMemo(() => {
    if (!body) return '';
    try {
      return marked.parse(body) as string;
    } catch {
      return body;
    }
  }, [body]);

  const renderedInstructionsMarkdown = useMemo(() => {
    if (!instructions) return '';
    try {
      return marked.parse(instructions) as string;
    } catch {
      return instructions;
    }
  }, [instructions]);

  const htmlPreviewUrl = useMemo(() => {
    return file?.url ?? asset?.file_url ?? null;
  }, [file, asset?.file_url]);

  const validate = (): boolean => {
    const next: Record<string, string> = {};
    if (!title.trim()) next.title = 'Give this asset a title';

    if (kind === 'inline_text' && !body.trim()) next.body = 'Content cannot be empty';
    if (kind === 'file' && !file) next.file = 'Upload a file for this asset';
    if (kind === 'link') {
      if (!externalUrl.trim()) next.external_url = 'Enter a URL';
      else {
        try {
          new URL(externalUrl);
        } catch {
          next.external_url = 'That does not look like a valid URL';
        }
      }
    }
    if (assetType === 'quiz') {
      if (!questions.length) next.questions = 'Add at least one question';
      questions.forEach((q, i) => {
        if (!q.question.trim()) next[`q${i}`] = 'Question text is required';
        else if (q.options.filter((o) => o.trim()).length < 2)
          next[`q${i}`] = 'Give at least two options';
        else if (q.correct_index >= q.options.length)
          next[`q${i}`] = 'Pick which option is correct';
      });
    }
    if (assetType === 'assignment' && !instructions.trim())
      next.instructions = 'Instructions are required';
    if (assetType === 'lab') {
      if (!objective.trim()) next.objective = 'Describe the objective';
      if (!steps.some((s) => s.title.trim())) next.steps = 'Add at least one step';
    }

    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const buildPayload = (): Record<string, unknown> => {
    const base: Record<string, unknown> = {
      asset_type: assetType,
      title: title.trim(),
      description: description.trim() || undefined,
      tags,
      status,
    };

    if (kind === 'inline_text') {
      base.body = body;
      base.config = {
        ...(assetType === 'code_snippet' && { language }),
      };
    } else if (kind === 'file') {
      base.media_file_id = file?.id;
      base.config = {
        filename: file?.filename,
        size: file?.size,
      };
    } else if (kind === 'link') {
      base.external_url = externalUrl.trim();
    } else if (assetType === 'quiz') {
      base.questions = questions.map((q) => ({
        ...q,
        options: q.options.filter((o) => o.trim()),
      }));
      base.pass_mark_percent = passMark;
    } else if (assetType === 'assignment') {
      base.instructions = instructions;
      if (dueInDays) base.due_in_days = Number(dueInDays);
    } else if (assetType === 'lab') {
      base.objective = objective;
      base.steps = steps.filter((s) => s.title.trim());
    }

    return base;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) {
      toast.error('Please fix the highlighted fields');
      const firstError = Object.keys(errors)[0];
      const element = document.getElementById(firstError);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      return;
    }

    setSaving(true);
    try {
      const payload = buildPayload();
      

      if (isEdit) {
        // asset_type is immutable
        delete payload.asset_type;
        await trainingService.updateAsset(asset.id, payload);
        toast.success('Asset updated successfully');
      } else {
        await trainingService.createAsset(payload);
        toast.success('Asset created successfully');
      }
      router.push('/training/assets');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not save the asset');
    } finally {
      setSaving(false);
    }
  };

  // Helper to extract YouTube video ID for video link previews
  const getYoutubeId = (url: string) => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return match && match[2].length === 11 ? match[2] : null;
  };

  const activeColor = TYPE_COLOR_MAP[assetType] ?? {
    bg: 'bg-teal-50 text-teal-600 border-teal-200',
    text: 'text-teal-700',
    border: 'border-teal-500',
  };

  // `file` is seeded from asset.media_file_id when editing (see the useState above), so
  // it's already non-null whenever a real file is attached — but existing assets were
  // never guaranteed a `config.filename`/`config.size` (the upload form historically
  // only wrote media_file_id), which used to leave `file.size` at its `0` fallback and
  // get misread downstream as "nothing uploaded". Only the true absence of `file` means
  // that; a present-but-metadata-less file gets an asset-type-flavored label instead of
  // a placeholder that implies nothing was ever uploaded.
  const fileAttachmentSummary = (() => {
    if (!file) return 'No file attached yet. Upload file to package asset.';
    if (file.size > 0) return `Attachment size: ${formatBytes(file.size)}`;
    return `Attached ${assetMeta(assetType).label} file — exact size unavailable`;
  })();

  if (loadingTypes) {
    return (
      <div className="flex justify-center py-24">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <>
    <form onSubmit={handleSubmit} className="mx-auto max-w-[1600px] space-y-6">
      {/* Visual Header / Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-200 bg-white p-4 shadow-sm rounded-xl">
        <div className="flex items-center gap-3">
          <div className={cn('flex h-10 w-10 items-center justify-center rounded-lg border', activeColor.bg)}>
            {(() => {
              const Icon = assetMeta(assetType).icon;
              return <Icon className="h-5 w-5 shrink-0" />;
            })()}
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">
              {isEdit ? `Edit Asset: ${asset.title}` : 'Authoring Studio'}
            </h1>
            <p className="text-xs text-gray-500">
              Create, configure, and instantly test interactive modules
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" disabled={saving} className="bg-teal-600 hover:bg-teal-700">
            {saving ? (
              <>
                <Spinner size="sm" className="mr-2" /> Saving...
              </>
            ) : isEdit ? (
              'Save Changes'
            ) : (
              'Create Asset'
            )}
          </Button>
        </div>
      </div>

      {/* Main Studio Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12 items-start">
        {/* Editor Columns (Left Pane - 60%) */}
        <div className="space-y-6 lg:col-span-7">
          {/* 1. Asset Type Selector (Hidden when editing) */}
          {!isEdit && (
            <Card className="p-6 transition-all duration-300 hover:shadow-md border-gray-200 bg-white">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="h-4.5 w-4.5 text-teal-600" />
                <h2 className="text-sm font-bold tracking-tight text-gray-900">Asset Type</h2>
              </div>
              <p className="text-xs text-gray-500 mb-5">
                Select the format below. Authoring options and live preview will adapt immediately.
              </p>

              <div className="space-y-6">
                {Object.entries(grouped).map(([kindKey, items]) => (
                  <div key={kindKey} className="space-y-2">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-gray-400">
                      {STORAGE_KIND_LABEL[kindKey as keyof typeof STORAGE_KIND_LABEL] ?? kindKey}
                    </p>
                    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                      {items.map((t) => {
                        const meta = ASSET_TYPE_META[t.value];
                        const Icon = meta?.icon;
                        const active = assetType === t.value;
                        const colors = TYPE_COLOR_MAP[t.value] ?? activeColor;
                        return (
                          <button
                            key={t.value}
                            type="button"
                            onClick={() => setAssetType(t.value)}
                            className={cn(
                              'group relative flex flex-col items-start gap-2 rounded-xl border p-4.5 text-left transition-all duration-200',
                              active
                                ? 'bg-teal-50 border-teal-500 shadow-sm ring-1 ring-teal-500'
                                : 'bg-white hover:bg-gray-50 border-gray-200 hover:border-gray-300'
                            )}
                          >
                            <div
                              className={cn(
                                'flex h-9 w-9 items-center justify-center rounded-lg border transition-colors',
                                active ? colors.bg : 'bg-gray-50 text-gray-500 group-hover:bg-gray-100 group-hover:text-gray-700 border-gray-150'
                              )}
                            >
                              {Icon && <Icon className="h-4.5 w-4.5" />}
                            </div>
                            <div className="space-y-0.5">
                              <p className="text-xs font-bold text-gray-900 leading-tight">
                                {t.label}
                              </p>
                              <p className="text-[10px] text-gray-500 line-clamp-2 leading-relaxed">
                                {meta?.hint}
                              </p>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* 2. Core Metadata Form */}
          <Card className="p-6 transition-all duration-300 hover:shadow-md border-gray-200 bg-white">
            <div className="flex items-center gap-2 mb-4">
              <Info className="h-4.5 w-4.5 text-teal-600" />
              <h2 className="text-sm font-bold tracking-tight text-gray-900">General Information</h2>
            </div>

            <div className="space-y-4">
              <FormField label="Title" required error={errors.title}>
                <Input
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Master-class in NumPy Operations"
                  error={!!errors.title}
                  className="bg-gray-50 focus:bg-white transition-colors py-2 px-3 text-sm rounded-lg"
                />
              </FormField>

              <FormField label="Description" description="Optional — a summary of this module. Helps search inside modules.">
                <Input
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="e.g. Learn vector manipulation, syntax limits, and boolean filters"
                  className="bg-gray-50 focus:bg-white transition-colors py-2 px-3 text-sm rounded-lg"
                />
              </FormField>

              <div className="grid gap-4 sm:grid-cols-2">
                <FormField label="Tags" description="Select existing or type new">
                  <div className="space-y-2">
                    {tags.length > 0 && (
                      <div className="flex flex-wrap gap-1.5">
                        {tags.map((t) => (
                          <span
                            key={t}
                            className="inline-flex items-center gap-1 rounded-full bg-teal-50 border border-teal-200 px-2 py-0.5 text-xs font-medium text-teal-700"
                          >
                            {t}
                            <button
                              type="button"
                              onClick={() => setTags(tags.filter((x) => x !== t))}
                              className="rounded-full p-0.5 hover:bg-teal-200 transition-colors"
                            >
                              <X className="h-3 w-3" />
                            </button>
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="relative">
                      <Tag className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-gray-400" />
                      <input
                        value={tagInput}
                        onChange={(e) => setTagInput(e.target.value)}
                        onKeyDown={(e) => {
                          if ((e.key === 'Enter' || e.key === ',') && tagInput.trim()) {
                            e.preventDefault();
                            const val = tagInput.trim().toLowerCase().replace(/,/g, '');
                            if (val && !tags.includes(val)) setTags([...tags, val]);
                            setTagInput('');
                          }
                        }}
                        placeholder="Type & press Enter…"
                        className="w-full rounded-lg border border-gray-300 bg-gray-50 py-1.5 pl-8 pr-3 text-sm focus:border-teal-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-teal-500"
                      />
                    </div>
                    {existingTags.filter((t) => !tags.includes(t) && (!tagInput || t.includes(tagInput.toLowerCase()))).length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {existingTags
                          .filter((t) => !tags.includes(t) && (!tagInput || t.includes(tagInput.toLowerCase())))
                          .slice(0, 12)
                          .map((t) => (
                            <button
                              key={t}
                              type="button"
                              onClick={() => {
                                setTags([...tags, t]);
                                setTagInput('');
                              }}
                              className="rounded-full border border-gray-200 bg-white px-2 py-0.5 text-[11px] text-gray-600 hover:border-teal-400 hover:bg-teal-50 hover:text-teal-700 transition-colors"
                            >
                              + {t}
                            </button>
                          ))}
                      </div>
                    )}
                  </div>
                </FormField>
                <FormField label="Status" description="Control learner visibility">
                  <Select
                    value={status}
                    onChange={(e) => setStatus(e.target.value as never)}
                    className="bg-gray-50 hover:bg-gray-100 transition-colors py-2 px-3 text-sm rounded-lg border border-gray-300"
                  >
                    <option value="draft">Draft (Visible to Trainer)</option>
                    <option value="published">Published (Visible to Learners)</option>
                    <option value="archived">Archived</option>
                  </Select>
                </FormField>
              </div>
            </div>
          </Card>

          {/* 3. Dynamic Content Payload Editor */}
          <Card className="p-6 transition-all duration-300 hover:shadow-md border-gray-200 bg-white">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-5">
              <div className="flex items-center gap-2">
                <BookOpen className="h-4.5 w-4.5 text-teal-600" />
                <h2 className="text-sm font-bold tracking-tight text-gray-900">Asset Content</h2>
              </div>
              {kind === 'inline_text' && (
                <span className="inline-flex items-center gap-1 rounded bg-teal-50 border border-teal-100 px-2 py-0.5 text-[10px] font-semibold text-teal-700">
                  <Sparkles className="h-3 w-3" /> Live Sync Active
                </span>
              )}
            </div>

            {/* A. Text / Code Editor Panel */}
            {kind === 'inline_text' && (
              <div className="space-y-4">
                {assetType === 'code_snippet' && (
                  <div className="w-1/2">
                    <FormField label="Programming Language">
                      <Select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="bg-gray-50 hover:bg-gray-100 transition-colors text-sm rounded-lg"
                      >
                        {CODE_LANGUAGES.map((l) => (
                          <option key={l} value={l}>
                            {l.toUpperCase()}
                          </option>
                        ))}
                      </Select>
                    </FormField>
                  </div>
                )}
                
                {assetType === 'markdown' && (
                  <div className="flex items-center gap-2 rounded-lg border border-dashed border-gray-300 bg-gray-50 p-3 mb-2">
                    <FileJson className="h-4 w-4 text-gray-500 shrink-0" />
                    <span className="text-xs text-gray-600 flex-1">Import content from a .md file</span>
                    <input
                      type="file"
                      accept=".md,.markdown,.txt"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) {
                          const reader = new FileReader();
                          reader.onload = (ev) => {
                            setBody(ev.target?.result as string);
                            toast.success('File content loaded successfully');
                          };
                          reader.readAsText(file);
                        }
                        e.target.value = '';
                      }}
                      className="hidden"
                      id="md-upload-input"
                    />
                    <button
                      type="button"
                      onClick={() => document.getElementById('md-upload-input')?.click()}
                      className="inline-flex items-center gap-1.5 rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-bold text-gray-700 hover:bg-gray-100 shadow-sm transition-colors"
                    >
                      <Upload className="h-3.5 w-3.5" /> Import File
                    </button>
                  </div>
                )}

                <FormField
                  label={assetType === 'code_snippet' ? 'Code Editor' : 'Content Markdown'}
                  required
                  error={errors.body}
                  description={
                    assetType === 'code_snippet'
                      ? 'Type or paste code snippet. Features autocomplete, formatting, syntax highlighting.'
                      : 'Markdown markup supported (tables, code snippets, inline CSS).'
                  }
                >
                  <CodeEditor
                    ref={assetType !== 'code_snippet' ? codeEditorRef : undefined}
                    value={body}
                    onChange={(val) => setBody(val)}
                    language={assetType === 'code_snippet' ? language : 'markdown'}
                    error={!!errors.body}
                    height="450px"
                    onInsertImage={assetType !== 'code_snippet' ? () => setShowImagePicker(true) : undefined}
                  />
                </FormField>
              </div>
            )}

            {/* B. File Uploader Panel */}
            {kind === 'file' && (
              <FormField label="Attach File" required error={errors.file}>
                <div className="rounded-xl border border-dashed border-gray-300 p-4 hover:bg-gray-50 transition-colors">
                  <AssetFileUpload
                    assetType={assetType}
                    rules={rules}
                    value={file}
                    onChange={(f) => setFile(f)}
                  />
                </div>
              </FormField>
            )}

            {/* C. Link Input Panel */}
            {kind === 'link' && (
              <FormField label="External Target URL" required error={errors.external_url}>
                <div className="relative rounded-lg shadow-sm">
                  <Input
                    value={externalUrl}
                    onChange={(e) => setExternalUrl(e.target.value)}
                    placeholder={
                      assetType === 'youtube'
                        ? 'e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                        : assetType === 'github_repo'
                        ? 'e.g. https://github.com/techpath/numpy-lessons'
                        : 'https://example.com'
                    }
                    error={!!errors.external_url}
                    className="pl-3 pr-10 py-2 px-3 bg-gray-50 focus:bg-white text-sm rounded-lg"
                  />
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                    <ExternalLink className="h-4 w-4 text-gray-400" />
                  </div>
                </div>
              </FormField>
            )}

            {/* D. Interactive Quiz Builder */}
            {assetType === 'quiz' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between bg-teal-50/50 p-3 rounded-lg border border-teal-100">
                  <div className="text-xs text-teal-800 font-medium">
                    Create questions, specify alternatives, set the correct answers, and provide feedback explanations.
                  </div>
                  <div className="w-28 shrink-0">
                    <FormField label="Pass score %">
                      <Input
                        type="number"
                        min={0}
                        max={100}
                        value={passMark}
                        onChange={(e) => setPassMark(Number(e.target.value))}
                        className="py-1 px-2.5 text-xs text-center font-bold bg-white"
                      />
                    </FormField>
                  </div>
                </div>

                <div className="flex items-center gap-2 rounded-lg border border-dashed border-gray-300 bg-gray-50 p-3">
                  <FileJson className="h-4 w-4 text-gray-500 shrink-0" />
                  <span className="text-xs text-gray-600 flex-1">Import questions from a JSON file</span>
                  <input
                    ref={quizFileInputRef}
                    type="file"
                    accept=".json"
                    onChange={handleQuizFileImport}
                    className="hidden"
                  />
                  <button
                    type="button"
                    onClick={() => quizFileInputRef.current?.click()}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-bold text-gray-700 hover:bg-gray-100 shadow-sm transition-colors"
                  >
                    <Upload className="h-3.5 w-3.5" /> Fill from File
                  </button>
                  <button
                    type="button"
                    onClick={downloadQuizSample}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-teal-200 bg-teal-50 px-3 py-1.5 text-xs font-bold text-teal-700 hover:bg-teal-100 shadow-sm transition-colors"
                  >
                    <Download className="h-3.5 w-3.5" /> Sample File
                  </button>
                </div>

                {errors.questions && <p className="text-xs text-red-500 font-medium">{errors.questions}</p>}

                <div className="space-y-4">
                  {questions.map((q, qi) => (
                    <div key={qi} className="group relative rounded-xl border border-gray-200 bg-white p-5 shadow-sm hover:shadow transition-shadow">
                      <div className="mb-4 flex items-center justify-between border-b border-gray-150 pb-2">
                        <span className="inline-flex items-center gap-1.5 rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-bold text-gray-600">
                          Question {qi + 1}
                        </span>
                        {questions.length > 1 && (
                          <button
                            type="button"
                            onClick={() => setQuestions(questions.filter((_, i) => i !== qi))}
                            className="rounded p-1 text-gray-400 hover:bg-rose-50 hover:text-rose-600 transition-colors"
                            aria-label="Remove question"
                          >
                            <Trash2 className="h-4.5 w-4.5" />
                          </button>
                        )}
                      </div>

                      <div className="space-y-4">
                        <FormField label="Question Statement" required>
                          <Input
                            value={q.question}
                            onChange={(e) => {
                              const next = [...questions];
                              next[qi] = { ...q, question: e.target.value };
                              setQuestions(next);
                            }}
                            placeholder="e.g. What is the complexity of sorting a numpy array using quicksort?"
                            className="text-sm py-2 px-3 bg-gray-50 focus:bg-white"
                          />
                        </FormField>

                        <div className="space-y-2">
                          <label className="text-xs font-bold text-gray-600">Answer Options</label>
                          <div className="space-y-2">
                            {q.options.map((opt, oi) => (
                              <div key={oi} className="flex items-center gap-2">
                                <button
                                  type="button"
                                  onClick={() => {
                                    const next = [...questions];
                                    next[qi] = { ...q, correct_index: oi };
                                    setQuestions(next);
                                  }}
                                  className={cn(
                                    'flex h-6 w-6 shrink-0 items-center justify-center rounded-full border transition-all active:scale-90',
                                    q.correct_index === oi
                                      ? 'border-teal-600 bg-teal-600 text-white'
                                      : 'border-gray-300 bg-white hover:border-teal-500'
                                  )}
                                  title="Mark as correct answer"
                                >
                                  {q.correct_index === oi ? (
                                    <Check className="h-3.5 w-3.5" />
                                  ) : (
                                    <span className="text-[10px] text-gray-400 font-bold">{oi + 1}</span>
                                  )}
                                </button>
                                <Input
                                  value={opt}
                                  onChange={(e) => {
                                    const next = [...questions];
                                    const options = [...q.options];
                                    options[oi] = e.target.value;
                                    next[qi] = { ...q, options };
                                    setQuestions(next);
                                  }}
                                  placeholder={`Option ${oi + 1}`}
                                  className="text-xs py-1.5 px-3 bg-gray-50 focus:bg-white"
                                />
                                {q.options.length > 2 && (
                                  <button
                                    type="button"
                                    onClick={() => {
                                      const next = [...questions];
                                      const options = q.options.filter((_, i) => i !== oi);
                                      next[qi] = {
                                        ...q,
                                        options,
                                        correct_index: Math.min(q.correct_index, options.length - 1),
                                      };
                                      setQuestions(next);
                                    }}
                                    className="rounded p-1.5 text-gray-400 hover:text-rose-600 transition-colors"
                                    aria-label="Remove option"
                                  >
                                    <Trash2 className="h-4 w-4" />
                                  </button>
                                )}
                              </div>
                            ))}
                          </div>
                          <button
                            type="button"
                            onClick={() => {
                              const next = [...questions];
                              next[qi] = { ...q, options: [...q.options, ''] };
                              setQuestions(next);
                            }}
                            className="inline-flex items-center gap-1 mt-1 text-xs font-bold text-teal-600 hover:text-teal-700"
                          >
                            <Plus className="h-3.5 w-3.5" /> Add alternative choice
                          </button>
                        </div>

                        <FormField label="Explanation / Solution rationale" description="Shown to student after answering">
                          <Input
                            value={q.explanation ?? ''}
                            onChange={(e) => {
                              const next = [...questions];
                              next[qi] = { ...q, explanation: e.target.value };
                              setQuestions(next);
                            }}
                            placeholder="Explain the solution detail here..."
                            className="text-xs py-1.5 px-3 bg-gray-50 focus:bg-white"
                          />
                        </FormField>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex items-center justify-between border-t border-gray-100 pt-4">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      setQuestions([
                        ...questions,
                        { question: '', options: ['', ''], correct_index: 0, explanation: '' },
                      ])
                    }
                    className="border-gray-300 hover:bg-gray-50 text-gray-700 font-bold"
                  >
                    <Plus className="mr-1.5 h-4 w-4" />
                    New Question Card
                  </Button>
                </div>
              </div>
            )}

            {/* E. Interactive Assignment Form */}
            {assetType === 'assignment' && (
              <div className="space-y-4">
                <FormField label="Instructions" required error={errors.instructions} description="Explain what work needs submission. Markdown is supported.">
                  <CodeEditor
                    value={instructions}
                    onChange={(val) => setInstructions(val)}
                    language="markdown"
                    error={!!errors.instructions}
                    height="300px"
                  />
                </FormField>
                <div className="w-1/2">
                  <FormField label="Due Timeline (Days)" description="Optional — days allowed for submission">
                    <div className="flex items-center gap-2">
                      <Input
                        type="number"
                        min={0}
                        value={dueInDays}
                        onChange={(e) => setDueInDays(e.target.value)}
                        placeholder="e.g. 7"
                        className="py-2 px-3 bg-gray-50 text-sm rounded-lg"
                      />
                      <span className="text-xs text-gray-500 font-bold">Days</span>
                    </div>
                  </FormField>
                </div>
              </div>
            )}

            {/* F. Interactive Lab Form */}
            {assetType === 'lab' && (
              <div className="space-y-5">
                <FormField label="Objective" required error={errors.objective} description="Summarize the learning outcome of this guided exercise.">
                  <Input
                    value={objective}
                    onChange={(e) => setObjective(e.target.value)}
                    placeholder="e.g. Connect to a local MySQL container and create index views"
                    className="text-sm py-2 px-3 bg-gray-50 focus:bg-white"
                  />
                </FormField>

                <div className="flex items-center gap-2 rounded-lg border border-dashed border-gray-300 bg-gray-50 p-3">
                  <FileJson className="h-4 w-4 text-gray-500 shrink-0" />
                  <span className="text-xs text-gray-600 flex-1">Import lab steps from a JSON file</span>
                  <input
                    ref={labFileInputRef}
                    type="file"
                    accept=".json"
                    onChange={handleLabFileImport}
                    className="hidden"
                  />
                  <button
                    type="button"
                    onClick={() => labFileInputRef.current?.click()}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-xs font-bold text-gray-700 hover:bg-gray-100 shadow-sm transition-colors"
                  >
                    <Upload className="h-3.5 w-3.5" /> Fill from File
                  </button>
                  <button
                    type="button"
                    onClick={downloadLabSample}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-teal-200 bg-teal-50 px-3 py-1.5 text-xs font-bold text-teal-700 hover:bg-teal-100 shadow-sm transition-colors"
                  >
                    <Download className="h-3.5 w-3.5" /> Sample File
                  </button>
                </div>

                <FormField label="Steps" required error={errors.steps} description="List instructions in sequence. Click check icon to review progress.">
                  <div className="space-y-3">
                    {steps.map((step, i) => (
                      <div key={i} className="flex gap-3">
                        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-teal-50 text-xs font-bold text-teal-700 border border-teal-100 mt-1">
                          {i + 1}
                        </span>
                        <div className="flex-1 space-y-2">
                          <Input
                            value={step.title}
                            onChange={(e) => {
                              const next = [...steps];
                              next[i] = { ...step, title: e.target.value };
                              setSteps(next);
                            }}
                            placeholder={`Step ${i + 1} Title...`}
                            className="text-xs py-1.5 px-3 bg-gray-50 focus:bg-white font-medium"
                          />
                          <textarea
                            value={step.instructions}
                            onChange={(e) => {
                              const next = [...steps];
                              next[i] = { ...step, instructions: e.target.value };
                              setSteps(next);
                            }}
                            placeholder="Detailed instructions (Markdown supported)..."
                            className="w-full rounded-md border border-gray-300 bg-gray-50 px-3 py-2 text-xs focus:border-teal-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-teal-500 min-h-[80px] font-mono"
                          />
                        </div>
                        {steps.length > 1 && (
                          <button
                            type="button"
                            onClick={() => setSteps(steps.filter((_, x) => x !== i))}
                            className="rounded p-1.5 text-gray-400 hover:text-rose-600 hover:bg-rose-50 transition-colors mt-1 h-fit"
                            aria-label="Remove step"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={() => setSteps([...steps, { title: '', instructions: '' }])}
                      className="inline-flex items-center gap-1 text-xs font-bold text-teal-600 hover:text-teal-700 mt-1"
                    >
                      <Plus className="h-3.5 w-3.5" /> Add procedural step
                    </button>
                  </div>
                </FormField>
              </div>
            )}
          </Card>
        </div>

        {/* Live Preview Column (Right Pane - 40%) */}
        <div className="lg:col-span-5 lg:sticky lg:top-6 space-y-4">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <Eye className="h-4 w-4 text-teal-600" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-gray-600">Student Preview</h3>
            </div>
            <div className="flex items-center gap-2">
              {/* Device switcher */}
              <div className="flex rounded-lg border border-gray-200 bg-white p-0.5">
                <button
                  type="button"
                  onClick={() => setPreviewDevice('desktop')}
                  className={cn(
                    'rounded p-1 transition-colors',
                    previewDevice === 'desktop' ? 'bg-gray-150 text-gray-800' : 'text-gray-400 hover:text-gray-700'
                  )}
                  title="Desktop View"
                >
                  <Laptop className="h-3.5 w-3.5" />
                </button>
                <button
                  type="button"
                  onClick={() => setPreviewDevice('mobile')}
                  className={cn(
                    'rounded p-1 transition-colors',
                    previewDevice === 'mobile' ? 'bg-gray-150 text-gray-800' : 'text-gray-400 hover:text-gray-700'
                  )}
                  title="Mobile View"
                >
                  <Smartphone className="h-3.5 w-3.5" />
                </button>
              </div>

              {/* Dark mode preview toggle */}
              <button
                type="button"
                onClick={() => setPreviewTheme((prev) => (prev === 'light' ? 'dark' : 'light'))}
                className="flex items-center gap-1 rounded-lg border border-gray-200 bg-white px-2.5 py-1 text-[10px] font-bold text-gray-600 hover:bg-gray-50 active:scale-95"
              >
                {previewTheme === 'light' ? (
                  <>
                    <Moon className="h-3 w-3" />
                    <span>Dark UI</span>
                  </>
                ) : (
                  <>
                    <Sun className="h-3 w-3" />
                    <span>Light UI</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Student View Device Shell */}
          <div
            className={cn(
              'mx-auto w-full overflow-hidden rounded-2xl border bg-gray-100 shadow-xl transition-all duration-300',
              previewDevice === 'mobile' ? 'max-w-[375px] aspect-[9/16]' : 'w-full min-h-[600px]',
              previewTheme === 'dark' ? 'border-gray-800 bg-gray-950' : 'border-gray-200 bg-white'
            )}
          >
            {/* Mock Web Browser Chrome */}
            <div
              className={cn(
                'flex h-10 items-center border-b px-4 gap-2',
                previewTheme === 'dark' ? 'border-gray-800 bg-gray-900' : 'border-gray-250 bg-gray-100'
              )}
            >
              <div className="flex gap-1.5 shrink-0">
                <span className="h-2.5 w-2.5 rounded-full bg-red-400" />
                <span className="h-2.5 w-2.5 rounded-full bg-amber-400" />
                <span className="h-2.5 w-2.5 rounded-full bg-green-400" />
              </div>
              <div
                className={cn(
                  'mx-4 flex h-6 flex-1 items-center justify-center rounded px-3 text-[10px] truncate',
                  previewTheme === 'dark' ? 'bg-gray-950 text-gray-500' : 'bg-white text-gray-400 border border-gray-200'
                )}
              >
                techpath.edu/training/asset/{isEdit ? asset.public_id : 'new-asset'}
              </div>
            </div>

            {/* Preview Frame Area */}
            <div
              className={cn(
                'p-6 h-[calc(100%-40px)] overflow-y-auto space-y-4',
                previewTheme === 'dark' ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-800'
              )}
            >
              {/* Asset Header */}
              <div className="border-b pb-4 border-gray-200/50">
                <span
                  className={cn(
                    'rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider',
                    activeColor.bg
                  )}
                >
                  {assetMeta(assetType).label}
                </span>
                <h2
                  className={cn(
                    'mt-2 text-base font-extrabold tracking-tight',
                    previewTheme === 'dark' ? 'text-white' : 'text-gray-950'
                  )}
                >
                  {title || 'Untitled Lecture Asset'}
                </h2>
                {description && <p className="mt-1 text-xs text-gray-400">{description}</p>}
                {tags.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1">
                    {tags.map((t, idx) => (
                        <span
                          key={idx}
                          className={cn(
                            'rounded px-1.5 py-0.5 text-[9px] font-medium border',
                            previewTheme === 'dark'
                              ? 'bg-gray-800 text-gray-300 border-gray-700'
                              : 'bg-white text-gray-600 border-gray-200'
                          )}
                        >
                          #{t}
                        </span>
                      ))}
                  </div>
                )}
              </div>

              {/* Dynamic Content Views */}

              {/* 1. Markdown / Inline Text Preview */}
              {kind === 'inline_text' && assetType !== 'code_snippet' && (
                <div
                  className={cn(
                    'prose prose-sm max-w-none transition-colors break-words',
                    previewTheme === 'dark' ? 'prose-invert text-gray-300' : 'text-gray-800'
                  )}
                  dangerouslySetInnerHTML={{
                    __html: renderedBodyMarkdown || '<p class="text-xs text-gray-400 italic">No content written yet.</p>',
                  }}
                />
              )}

              {/* 2. Code Snippet Preview */}
              {assetType === 'code_snippet' && (
                <div className="space-y-2">
                  {body ? (
                    <CodeEditor
                      value={body}
                      language={language}
                      readOnly
                      height={previewDevice === 'mobile' ? '250px' : '320px'}
                    />
                  ) : (
                    <div className="flex h-32 items-center justify-center rounded-xl border border-dashed border-gray-300 text-xs text-gray-400 italic">
                      Type code in editor to preview
                    </div>
                  )}
                </div>
              )}

              {/* 3. File Preview */}
              {kind === 'file' && assetType !== 'html_bundle' && (
                <div
                  className={cn(
                    'flex flex-col items-center justify-center rounded-xl border p-6 text-center gap-3',
                    previewTheme === 'dark' ? 'bg-gray-950 border-gray-800' : 'bg-white border-gray-200'
                  )}
                >
                  <div
                    className={cn(
                      'flex h-12 w-12 items-center justify-center rounded-full border',
                      activeColor.bg
                    )}
                  >
                    {(() => {
                      const Icon = assetMeta(assetType).icon;
                      return <Icon className="h-6 w-6" />;
                    })()}
                  </div>
                  <div className="space-y-1">
                    <p
                      className={cn(
                        'text-xs font-bold truncate max-w-xs',
                        previewTheme === 'dark' ? 'text-white' : 'text-gray-900'
                      )}
                    >
                      {file ? file.filename : 'Attach_Module_Resource.pdf'}
                    </p>
                    <p className="text-[10px] text-gray-400">{fileAttachmentSummary}</p>
                  </div>
                  {file && (
                    <button
                      type="button"
                      className="inline-flex items-center gap-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-xs font-bold shadow transition-transform active:scale-95"
                    >
                      <Download className="h-3.5 w-3.5" /> Download File
                    </button>
                  )}
                </div>
              )}

              {assetType === 'html_bundle' && htmlPreviewUrl && (
                <div className="flex w-full items-center justify-center">
                  <div className="h-96 w-full rounded-xl border border-gray-700 bg-white overflow-hidden shadow-2xl">
                    <iframe
                      src={htmlPreviewUrl}
                      sandbox="allow-scripts allow-same-origin"
                      className="h-full w-full"
                      title={title || 'HTML Bundle Preview'}
                    />
                  </div>
                </div>
              )}

              {/* 4. Link & Video Link Previews */}
              {kind === 'link' && (
                <div className="space-y-3">
                  {/* YouTube Embed Player */}
                  {assetType === 'youtube' && getYoutubeId(externalUrl) ? (
                    <div className="overflow-hidden rounded-xl border border-gray-200 shadow-md">
                      <div className="aspect-video w-full bg-black">
                        <iframe
                          width="100%"
                          height="100%"
                          src={`https://www.youtube.com/embed/${getYoutubeId(externalUrl)}`}
                          title="YouTube video player"
                          frameBorder="0"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen
                        />
                      </div>
                    </div>
                  ) : (
                    <div
                      className={cn(
                        'rounded-xl border p-4.5 transition-all shadow-sm hover:shadow hover:border-gray-300 flex items-start gap-3.5 cursor-pointer',
                        previewTheme === 'dark' ? 'bg-gray-950 border-gray-800' : 'bg-white border-gray-200'
                      )}
                    >
                      <div
                        className={cn(
                          'flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border',
                          activeColor.bg
                        )}
                      >
                        {assetType === 'youtube' && <Youtube className="h-5 w-5" />}
                        {assetType === 'github_repo' && <Github className="h-5 w-5" />}
                        {assetType === 'external_url' && <ExternalLink className="h-5 w-5" />}
                      </div>
                      <div className="min-w-0 flex-1 space-y-1">
                        <p
                          className={cn(
                            'text-xs font-bold truncate',
                            previewTheme === 'dark' ? 'text-white' : 'text-gray-900'
                          )}
                        >
                          {externalUrl ? new URL(externalUrl).hostname : 'Resource Portal Link'}
                        </p>
                        <p className="text-[10px] text-gray-400 line-clamp-2 leading-relaxed">
                          {externalUrl || 'No external URL target specified. Enter a URL on the left configuration card.'}
                        </p>
                        {externalUrl && (
                          <a
                            href={externalUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-[10px] font-bold text-teal-600 hover:text-teal-700 mt-1"
                          >
                            Visit Website <ExternalLink className="h-2.5 w-2.5" />
                          </a>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 5. Playable Quiz Preview */}
              {assetType === 'quiz' && (
                <div className="space-y-4">
                  {questions.filter((q) => q.question.trim()).length === 0 ? (
                    <div className="flex h-32 items-center justify-center rounded-xl border border-dashed border-gray-300 text-xs text-gray-400 italic">
                      Add questions to preview quiz
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {questions
                        .filter((q) => q.question.trim())
                        .map((q, qi) => {
                          const hasSelected = quizAnswers[qi] !== undefined;
                          const selectedOptionIdx = quizAnswers[qi];
                          const isCorrect = selectedOptionIdx === q.correct_index;

                          return (
                            <div
                              key={qi}
                              className={cn(
                                'rounded-xl border p-4.5 space-y-3 shadow-sm transition-all',
                                previewTheme === 'dark' ? 'bg-gray-950 border-gray-800' : 'bg-white border-gray-200'
                              )}
                            >
                              <div className="flex items-start justify-between gap-2 border-b border-gray-100 pb-2">
                                <span className="text-[10px] font-bold text-gray-400 uppercase">
                                  Question {qi + 1}
                                </span>
                                {quizSubmitted && (
                                  <span
                                    className={cn(
                                      'inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[9px] font-bold border',
                                      isCorrect
                                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                        : 'bg-rose-50 text-rose-700 border-rose-200'
                                    )}
                                  >
                                    {isCorrect ? (
                                      <>
                                        <CheckCircle className="h-3 w-3" /> Correct
                                      </>
                                    ) : (
                                      <>
                                        <XCircle className="h-3 w-3" /> Incorrect
                                      </>
                                    )}
                                  </span>
                                )}
                              </div>
                              <p
                                className={cn(
                                  'text-xs font-bold leading-relaxed',
                                  previewTheme === 'dark' ? 'text-white' : 'text-gray-900'
                                )}
                              >
                                {q.question}
                              </p>

                              <div className="space-y-1.5">
                                {q.options
                                  .filter((opt) => opt.trim())
                                  .map((opt, oi) => {
                                    const isOptionSelected = selectedOptionIdx === oi;
                                    const isOptionCorrect = q.correct_index === oi;

                                    let optionStyle = 'border-gray-200 hover:border-teal-500 hover:bg-teal-50/10';
                                    if (previewTheme === 'dark') optionStyle = 'border-gray-800 hover:border-teal-500 hover:bg-teal-900/10';

                                    if (isOptionSelected) {
                                      optionStyle = 'border-teal-600 bg-teal-500/10 text-teal-600';
                                      if (previewTheme === 'dark') optionStyle = 'border-teal-500 bg-teal-500/20 text-teal-400';
                                    }

                                    if (quizSubmitted) {
                                      if (isOptionCorrect) {
                                        optionStyle = 'border-emerald-600 bg-emerald-500/10 text-emerald-600';
                                        if (previewTheme === 'dark') optionStyle = 'border-emerald-500 bg-emerald-500/20 text-emerald-400';
                                      } else if (isOptionSelected) {
                                        optionStyle = 'border-rose-600 bg-rose-500/10 text-rose-600';
                                        if (previewTheme === 'dark') optionStyle = 'border-rose-500 bg-rose-500/20 text-rose-400';
                                      } else {
                                        optionStyle = 'opacity-55 border-gray-200';
                                        if (previewTheme === 'dark') optionStyle = 'opacity-40 border-gray-800';
                                      }
                                    }

                                    return (
                                      <button
                                        key={oi}
                                        type="button"
                                        disabled={quizSubmitted}
                                        onClick={() => {
                                          setQuizAnswers((prev) => ({ ...prev, [qi]: oi }));
                                        }}
                                        className={cn(
                                          'flex w-full items-center justify-between gap-3 rounded-lg border px-3 py-2 text-left text-xs transition-all duration-150',
                                          optionStyle
                                        )}
                                      >
                                        <span>{opt}</span>
                                        {isOptionSelected && <span className="h-1.5 w-1.5 rounded-full bg-current shrink-0" />}
                                      </button>
                                    );
                                  })}
                              </div>

                              {quizSubmitted && q.explanation && (
                                <div
                                  className={cn(
                                    'mt-3 rounded-lg p-2.5 text-[10px] leading-relaxed border',
                                    isCorrect
                                      ? 'bg-emerald-50/50 border-emerald-100 text-emerald-800'
                                      : 'bg-rose-50/50 border-rose-100 text-rose-800',
                                    previewTheme === 'dark' ? 'bg-gray-900 border-gray-800 text-gray-300' : ''
                                  )}
                                >
                                  <span className="font-bold">Solution Hint:</span> {q.explanation}
                                </div>
                              )}
                            </div>
                          );
                        })}

                      {/* Quiz controls */}
                      <div className="flex items-center justify-between border-t border-gray-200/50 pt-3">
                        <div className="text-[10px] font-medium text-gray-400">
                          Pass mark: <span className="font-bold text-teal-600">{passMark}%</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => {
                              setQuizAnswers({});
                              setQuizSubmitted(false);
                            }}
                            className={cn(
                              'flex h-7 w-7 items-center justify-center rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors',
                              previewTheme === 'dark' ? 'bg-gray-950 hover:bg-gray-800 border-gray-800 text-gray-300' : 'bg-white'
                            )}
                            title="Reset Quiz"
                          >
                            <RotateCcw className="h-3.5 w-3.5" />
                          </button>
                          {!quizSubmitted ? (
                            <button
                              type="button"
                              onClick={() => setQuizSubmitted(true)}
                              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-xs font-bold shadow"
                            >
                              Submit Quiz
                            </button>
                          ) : (
                            <span className="text-xs font-bold text-teal-600">Submitted</span>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* 6. Assignment Preview */}
              {assetType === 'assignment' && (
                <div className="space-y-4">
                  <div
                    className={cn(
                      'rounded-xl border p-4 shadow-sm space-y-3',
                      previewTheme === 'dark' ? 'bg-gray-950 border-gray-800' : 'bg-white border-gray-200'
                    )}
                  >
                    <div className="flex items-center justify-between border-b pb-2 border-gray-150">
                      <div className="flex items-center gap-1.5 text-xs font-bold">
                        <Calendar className="h-4 w-4 text-teal-600" />
                        <span>Deadline Info</span>
                      </div>
                      <span className="rounded bg-rose-500/10 border border-rose-500/20 text-rose-600 px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider">
                        {dueInDays ? `Due in ${dueInDays} days` : 'No absolute due date'}
                      </span>
                    </div>

                    <div
                      className={cn(
                        'prose prose-sm max-w-none break-words',
                        previewTheme === 'dark' ? 'prose-invert text-gray-300' : 'text-gray-800'
                      )}
                      dangerouslySetInnerHTML={{
                        __html: renderedInstructionsMarkdown || '<p class="text-xs text-gray-400 italic">No instructions written yet.</p>',
                      }}
                    />
                  </div>

                  {/* Mock file submission area */}
                  <div
                    className={cn(
                      'rounded-xl border border-dashed p-6 text-center space-y-3',
                      previewTheme === 'dark' ? 'bg-gray-900 border-gray-800' : 'bg-gray-50 border-gray-300'
                    )}
                  >
                    <p className="text-xs font-bold">Upload Submission</p>
                    <p className="text-[10px] text-gray-400">PDF, ZIP, or DOCX formats accepted.</p>
                    <button
                      type="button"
                      disabled
                      className="rounded-lg border border-gray-300 bg-white px-3.5 py-1.5 text-xs font-bold text-gray-700 shadow-sm opacity-60 shrink-0 cursor-not-allowed"
                    >
                      Attach Document
                    </button>
                  </div>
                </div>
              )}

              {/* 7. Interactive Lab Steps Preview */}
              {assetType === 'lab' && (
                <div className="space-y-4">
                  {/* Progress Header */}
                  {steps.filter((s) => s.title.trim()).length > 0 && (
                    <div
                      className={cn(
                        'rounded-xl border p-4 space-y-2.5 shadow-sm',
                        previewTheme === 'dark' ? 'bg-gray-950 border-gray-800' : 'bg-white border-gray-200'
                      )}
                    >
                      <div className="flex items-center justify-between text-xs font-bold">
                        <span>Guided Exercise Progress</span>
                        <span className="text-teal-600">
                          {Math.round(
                            (Object.values(completedSteps).filter(Boolean).length /
                              steps.filter((s) => s.title.trim()).length) *
                              100
                          )}
                          % Done
                        </span>
                      </div>
                      <div className="h-1.5 w-full overflow-hidden rounded-full bg-gray-100">
                        <div
                          className="h-full bg-teal-600 transition-all duration-300"
                          style={{
                            width: `${
                              (Object.values(completedSteps).filter(Boolean).length /
                                steps.filter((s) => s.title.trim()).length) *
                              100
                            }%`,
                          }}
                        />
                      </div>
                    </div>
                  )}

                  {objective && (
                    <div
                      className={cn(
                        'rounded-xl border p-4.5 shadow-sm space-y-2',
                        previewTheme === 'dark' ? 'bg-gray-950 border-gray-800' : 'bg-white border-gray-200'
                      )}
                    >
                      <div className="flex items-center gap-1 text-xs font-bold text-teal-600">
                        <Info className="h-4 w-4" />
                        <span>Objective</span>
                      </div>
                      <p className="text-xs leading-relaxed text-gray-500">{objective}</p>
                    </div>
                  )}

                  {/* Timeline Checklist */}
                  <div className="space-y-3.5">
                    {steps.filter((s) => s.title.trim()).length === 0 ? (
                      <div className="flex h-32 items-center justify-center rounded-xl border border-dashed border-gray-300 text-xs text-gray-400 italic">
                        Add procedures to build timeline
                      </div>
                    ) : (
                      steps
                        .filter((s) => s.title.trim())
                        .map((step, idx) => {
                          const isDone = !!completedSteps[idx];
                          return (
                            <div key={idx} className="flex gap-3">
                              {/* Connector Dot */}
                              <div className="flex flex-col items-center">
                                <button
                                  type="button"
                                  onClick={() => {
                                    setCompletedSteps((prev) => ({
                                      ...prev,
                                      [idx]: !prev[idx],
                                    }));
                                  }}
                                  className={cn(
                                    'flex h-6 w-6 items-center justify-center rounded-full border text-xs font-bold transition-all active:scale-95',
                                    isDone
                                      ? 'bg-teal-600 border-teal-600 text-white'
                                      : 'bg-white border-gray-300 hover:border-teal-500 text-gray-500'
                                  )}
                                >
                                  {isDone ? <Check className="h-3.5 w-3.5" /> : idx + 1}
                                </button>
                                {idx < steps.filter((s) => s.title.trim()).length - 1 && (
                                  <div className="h-full w-0.5 bg-gray-200 mt-1" />
                                )}
                              </div>
                              <div className="pt-0.5 space-y-0.5 min-w-0">
                                <p
                                  className={cn(
                                    'text-xs leading-relaxed',
                                    isDone ? 'line-through text-gray-400' : 'font-medium'
                                  )}
                                >
                                  {step.title}
                                </p>
                              </div>
                            </div>
                          );
                        })
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </form>

    <ImagePickerModal
      isOpen={showImagePicker}
      onClose={() => setShowImagePicker(false)}
      onSelect={(url) => {
        codeEditorRef.current?.insertAtCursor(`![image](${url})`);
        setShowImagePicker(false);
      }}
      folder="assets"
      entityType="lecture_asset"
    />
    </>
  );
}
