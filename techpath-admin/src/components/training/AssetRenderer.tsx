'use client';

import { useMemo, useState, useEffect } from 'react';
import {
  ExternalLink,
  Github,
  Download,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Check,
  Info,
  Calendar,
} from 'lucide-react';
import { marked } from 'marked';
import type { LectureAsset } from '@/types/training';
import { assetMeta } from '@/components/training/asset-type-registry';

function youtubeId(url: string): string | null {
  const m =
    url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/))([A-Za-z0-9_-]{11})/) ??
    null;
  return m ? m[1] : null;
}

function renderMarkdown(text: string): string {
  const processedText = text ? text.replace(/\\n/g, '\n') : '';
  return marked.parse(processedText, { async: false }) as string;
}

/** Office Online's viewer fetches the file itself, so this only works for a URL its
 * servers can actually reach — never a localhost/private-network one (local dev
 * storage, an internal-only backend). No dev key needed either way; it's the same
 * free, unauthenticated embed SharePoint/OneDrive use for public link previews. */
function isPubliclyReachable(url: string): boolean {
  try {
    const { hostname, protocol } = new URL(url);
    if (protocol !== 'https:') return false;
    if (hostname === 'localhost' || hostname === '127.0.0.1') return false;
    if (/^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(hostname)) return false;
    return true;
  } catch {
    return false;
  }
}

interface Props {
  asset: LectureAsset;
  className?: string;
}

function InlineTextSlide({ asset }: Props) {
  const [content, setContent] = useState(asset.body ?? '');
  
  useEffect(() => {
    if (!asset.body && asset.file_url) {
      fetch(asset.file_url)
        .then((res) => res.text())
        .then((text) => setContent(text))
        .catch((err) => console.error('Failed to load markdown content:', err));
    } else {
      setContent(asset.body ?? '');
    }
  }, [asset.body, asset.file_url]);

  const html = useMemo(() => renderMarkdown(content), [content]);

  return (
    <article
      className="prose prose-dark text-lg max-w-none px-8 py-6"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

function CodeSnippetSlide({ asset }: Props) {
  const config = asset.config as { language?: string } | null;
  const language = config?.language ?? 'text';

  return (
    <div className="px-8 py-6">
      <div className="rounded-xl border border-gray-700 bg-gray-900 overflow-hidden">
        <div className="flex items-center gap-2 border-b border-gray-700 px-4 py-2">
          <span className="h-3 w-3 rounded-full bg-red-500" />
          <span className="h-3 w-3 rounded-full bg-yellow-500" />
          <span className="h-3 w-3 rounded-full bg-green-500" />
          <span className="ml-4 text-xs font-mono text-gray-400">{language}</span>
        </div>
        <pre className="overflow-auto p-6 text-sm leading-relaxed">
          <code className="text-gray-100 font-mono whitespace-pre">{asset.body ?? ''}</code>
        </pre>
      </div>
    </div>
  );
}

function PdfSlide({ asset }: Props) {
  const src = asset.file_url ?? null;

  if (!src) {
    return <DownloadCard asset={asset} message="PDF file not available for preview" />;
  }

  return (
    <div className="flex h-full items-center justify-center px-4 py-4">
      <iframe
        src={`${src}#toolbar=1&view=FitH`}
        className="h-full w-full max-w-5xl rounded-lg border border-gray-700"
        title={asset.title}
      />
    </div>
  );
}

function VideoSlide({ asset }: Props) {
  const src = asset.file_url ?? null;

  if (!src) {
    return <DownloadCard asset={asset} message="Video file not available" />;
  }

  return (
    <div className="flex h-full items-center justify-center px-8 py-6">
      <video
        src={src}
        controls
        className="max-h-full max-w-full rounded-lg shadow-2xl"
        style={{ maxHeight: 'calc(100vh - 200px)' }}
      >
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

function PptSlide({ asset }: Props) {
  const src = asset.file_url ?? null;

  if (!src || !isPubliclyReachable(src)) {
    return (
      <DownloadCard
        asset={asset}
        message={
          src
            ? "Preview isn't available from a local address — download to view."
            : 'Presentation file not available'
        }
      />
    );
  }

  const embedSrc = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(src)}`;

  return (
    <div className="flex h-full flex-col gap-3 px-4 py-4">
      <div className="min-h-0 flex-1 overflow-hidden rounded-lg border border-gray-700 bg-white">
        <iframe src={embedSrc} className="h-full w-full" title={asset.title} />
      </div>
      <div className="flex shrink-0 items-center justify-between text-xs text-gray-500">
        <span>Rendered by Microsoft Office Online — trouble viewing?</span>
        <a
          href={src}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 rounded-lg border border-gray-700 px-3 py-1.5 font-medium text-gray-300 transition hover:bg-gray-800"
        >
          <Download className="h-3.5 w-3.5" />
          Download instead
        </a>
      </div>
    </div>
  );
}

function YoutubeSlide({ asset }: Props) {
  const vid = youtubeId(asset.external_url ?? '');
  if (!vid) {
    return <LinkCard url={asset.external_url ?? ''} label="YouTube Video" />;
  }

  return (
    <div className="flex h-full items-center justify-center px-8 py-6">
      <div className="w-full max-w-5xl aspect-video rounded-xl overflow-hidden shadow-2xl border border-gray-700">
        <iframe
          src={`https://www.youtube-nocookie.com/embed/${vid}?rel=0`}
          className="h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          title={asset.title}
        />
      </div>
    </div>
  );
}

function LinkCard({ url, label }: { url: string; label: string }) {
  return (
    <div className="flex h-full items-center justify-center px-8 py-6">
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center gap-4 rounded-xl border border-gray-700 bg-gray-800/50
          px-8 py-6 text-teal-400 transition hover:border-teal-500 hover:bg-gray-800"
      >
        <ExternalLink className="h-8 w-8 shrink-0" />
        <div>
          <p className="text-lg font-medium">{label}</p>
          <p className="mt-1 text-sm text-gray-400 break-all">{url}</p>
        </div>
      </a>
    </div>
  );
}

function GithubSlide({ asset }: Props) {
  const url = asset.external_url ?? '';
  return (
    <div className="flex h-full items-center justify-center px-8 py-6">
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center gap-4 rounded-xl border border-gray-700 bg-gray-800/50
          px-8 py-6 text-white transition hover:border-teal-500 hover:bg-gray-800"
      >
        <Github className="h-10 w-10 shrink-0" />
        <div>
          <p className="text-lg font-medium">{asset.title}</p>
          <p className="mt-1 text-sm text-gray-400 break-all">{url}</p>
        </div>
      </a>
    </div>
  );
}

function QuizSlide({ asset }: Props) {
  const config = asset.config as {
    questions?: Array<{
      question: string;
      options: string[];
      correct_index?: number;
      explanation?: string;
    }>;
  } | null;
  const questions = config?.questions ?? [];

  return (
    <div className="overflow-auto px-8 py-6">
      <div className="mx-auto max-w-3xl space-y-8">
        {questions.map((q, qi) => (
          <div key={qi} className="rounded-xl border border-gray-700 bg-gray-800/50 p-6">
            <p className="mb-4 text-lg font-medium text-white">
              <span className="mr-2 text-teal-400">Q{qi + 1}.</span>
              {q.question}
            </p>
            <div className="space-y-2">
              {q.options.map((opt, oi) => {
                const isCorrect = q.correct_index === oi;
                return (
                  <div
                    key={oi}
                    className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm ${
                      isCorrect
                        ? 'border border-green-600/50 bg-green-900/20 text-green-300'
                        : 'border border-gray-700 text-gray-300'
                    }`}
                  >
                    {isCorrect ? (
                      <CheckCircle2 className="h-4 w-4 shrink-0 text-green-400" />
                    ) : (
                      <XCircle className="h-4 w-4 shrink-0 text-gray-600" />
                    )}
                    {opt}
                  </div>
                );
              })}
            </div>
            {q.explanation && (
              <p className="mt-3 flex items-start gap-2 text-sm text-gray-400">
                <HelpCircle className="mt-0.5 h-4 w-4 shrink-0 text-teal-500" />
                {q.explanation}
              </p>
            )}
          </div>
        ))}
        {questions.length === 0 && (
          <p className="text-center text-gray-500">No questions configured.</p>
        )}
      </div>
    </div>
  );
}

function StructuredSlide({ asset }: Props) {
  const config = (asset.config as Record<string, unknown>) || {};
  
  // For assignments
  const instructions = (config.instructions as string) || (config.description as string) || '';
  const html = useMemo(() => renderMarkdown(instructions), [instructions]);
  
  // For labs
  const objective = (config.objective as string) || '';
  const steps = (config.steps as Array<{ title: string; instructions: string }>) || [];

  const [completedSteps, setCompletedSteps] = useState<Record<number, boolean>>({});

  if (asset.asset_type === 'assignment') {
    const dueInDays = config.due_in_days as number | undefined;
    return (
      <div className="overflow-auto px-8 py-6">
        <div className="mx-auto max-w-3xl space-y-6">
          <div className="rounded-xl border border-gray-700 bg-gray-800/50 p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-gray-700 pb-3">
              <div className="flex items-center gap-2 text-sm font-bold text-gray-200">
                <Calendar className="h-5 w-5 text-teal-400" />
                <span>Deadline Info</span>
              </div>
              <span className="rounded bg-rose-500/10 border border-rose-500/20 text-rose-400 px-2.5 py-1 text-xs font-bold uppercase tracking-wider">
                {dueInDays ? `Due in ${dueInDays} days` : 'No absolute due date'}
              </span>
            </div>

            <div
              className="prose prose-dark text-lg max-w-none"
              dangerouslySetInnerHTML={{
                __html: html || '<p class="text-gray-400 italic">No instructions provided.</p>',
              }}
            />
          </div>

          <div className="rounded-xl border border-dashed border-gray-600 bg-gray-800/30 p-8 text-center space-y-3">
            <p className="text-sm font-bold text-gray-300">File Submission (Student View)</p>
            <p className="text-xs text-gray-500">Students will upload their work here.</p>
          </div>
        </div>
      </div>
    );
  }

  // Lab View
  return (
    <div className="overflow-auto px-8 py-6">
      <div className="mx-auto max-w-3xl space-y-6">
        {steps.length > 0 && (
          <div className="rounded-xl border border-gray-700 bg-gray-800/50 p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between text-sm font-bold text-gray-200">
              <span>Guided Exercise Progress</span>
              <span className="text-teal-400">
                {Math.round((Object.values(completedSteps).filter(Boolean).length / steps.length) * 100)}% Done
              </span>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
              <div
                className="h-full bg-teal-500 transition-all duration-300"
                style={{
                  width: `${(Object.values(completedSteps).filter(Boolean).length / steps.length) * 100}%`,
                }}
              />
            </div>
          </div>
        )}

        {objective && (
          <div className="rounded-xl border border-gray-700 bg-gray-800/50 p-5 shadow-sm space-y-2.5">
            <div className="flex items-center gap-1.5 text-sm font-bold text-teal-400">
              <Info className="h-5 w-5" />
              <span>Objective</span>
            </div>
            <p className="text-base leading-relaxed text-gray-300">{objective}</p>
          </div>
        )}

        {steps.length > 0 && (
          <div className="space-y-4 pl-1 pt-2">
            {steps.map((step, idx) => {
              const isDone = !!completedSteps[idx];
              return (
                <div key={idx} className="flex gap-4">
                  <div className="flex flex-col items-center">
                    <button
                      type="button"
                      onClick={() => {
                        setCompletedSteps((prev) => ({
                          ...prev,
                          [idx]: !prev[idx],
                        }));
                      }}
                      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full border text-sm font-bold transition-all active:scale-95 ${
                        isDone
                          ? 'border-teal-500 bg-teal-500 text-white'
                          : 'border-gray-500 bg-gray-700 text-gray-300 hover:border-teal-400'
                      }`}
                    >
                      {isDone ? <Check className="h-4 w-4" /> : idx + 1}
                    </button>
                    {idx < steps.length - 1 && (
                      <div className="h-full w-0.5 bg-gray-700 mt-1.5" />
                    )}
                  </div>
                  <div className="pt-1 pb-5 min-w-0 flex-1">
                    <p
                      className={`text-lg leading-relaxed ${
                        isDone ? 'line-through text-gray-500' : 'font-medium text-white'
                      }`}
                    >
                      {step.title}
                    </p>
                    {step.instructions && (
                      <div
                        className={`mt-2 text-base prose prose-dark max-w-none ${isDone ? 'opacity-50' : ''}`}
                        dangerouslySetInnerHTML={{
                          __html: renderMarkdown(step.instructions),
                        }}
                      />
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

function CsvSlide({ asset }: Props) {
  const src = asset.file_url ?? null;
  const preview = asset.csv_preview;

  if (!src) {
    return <DownloadCard asset={asset} message="CSV file not available" />;
  }
  if (!preview) {
    return <DownloadCard asset={asset} message="Couldn't load this file for preview" />;
  }

  return (
    <div className="flex h-full flex-col gap-3 px-4 py-4">
      <div className="min-h-0 flex-1 overflow-auto rounded-lg border border-gray-700">
        <table className="w-full text-left text-sm">
          <thead className="sticky top-0 bg-gray-800">
            <tr>
              {preview.header.map((cell, i) => (
                <th key={i} className="whitespace-nowrap px-3 py-2 font-medium text-gray-200">
                  {cell}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.rows.map((r, ri) => (
              <tr key={ri} className="border-t border-gray-800 odd:bg-gray-900/40">
                {r.map((cell, ci) => (
                  <td key={ci} className="whitespace-nowrap px-3 py-1.5 text-gray-300">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex shrink-0 items-center justify-between text-xs text-gray-500">
        <span>
          {preview.truncated
            ? `Showing first ${preview.rows.length} rows — download for the full file`
            : `${preview.total_rows} row${preview.total_rows === 1 ? '' : 's'}`}
        </span>
        <a
          href={src}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 rounded-lg border border-gray-700 px-3 py-1.5 font-medium text-gray-300 transition hover:bg-gray-800"
        >
          <Download className="h-3.5 w-3.5" />
          Download full file
        </a>
      </div>
    </div>
  );
}

function DownloadCard({ asset, message }: Props & { message?: string }) {
  const meta = assetMeta(asset.asset_type);
  const Icon = meta.icon;
  const src = asset.file_url ?? null;

  return (
    <div className="flex h-full items-center justify-center px-8 py-6">
      <div className="rounded-xl border border-gray-700 bg-gray-800/50 px-10 py-8 text-center">
        <Icon className="mx-auto h-16 w-16 text-gray-500" />
        <p className="mt-4 text-lg font-medium text-white">{asset.title}</p>
        <p className="mt-1 text-sm text-gray-400">{meta.label}</p>
        {message && <p className="mt-2 text-xs text-gray-500">{message}</p>}
        {src && (
          <a
            href={src}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center gap-2 rounded-lg bg-teal-600 px-5 py-2.5
              text-sm font-medium text-white transition hover:bg-teal-700"
          >
            <Download className="h-4 w-4" />
            Download
          </a>
        )}
      </div>
    </div>
  );
}
function HtmlBundleSlide({ asset }: Props) {
  const src = asset.file_url ?? null;

  if (!src) {
    return <DownloadCard asset={asset} message="HTML file not available" />;
  }

  return (
    <div className="flex h-full items-center justify-center px-4 py-4">
      <iframe
        src={src}
        sandbox="allow-scripts allow-same-origin"
        className="h-full w-full rounded-xl border border-gray-700 bg-white shadow-2xl"
        title={asset.title}
      />
    </div>
  );
}


export function AssetRenderer({ asset, className }: Props) {
  const type = asset.asset_type;

  const content = (() => {
    switch (type) {
      case 'markdown':
      case 'notes':
      case 'cheat_sheet':
        return <InlineTextSlide asset={asset} />;
      case 'code_snippet':
        return <CodeSnippetSlide asset={asset} />;
      case 'pdf':
        return <PdfSlide asset={asset} />;
      case 'ppt':
        return <PptSlide asset={asset} />;
      case 'video':
        return <VideoSlide asset={asset} />;
      case 'csv':
        return <CsvSlide asset={asset} />;
      case 'youtube':
        return <YoutubeSlide asset={asset} />;
      case 'external_url':
        return <LinkCard url={asset.external_url ?? ''} label={asset.title} />;
      case 'github_repo':
        return <GithubSlide asset={asset} />;
      case 'quiz':
        return <QuizSlide asset={asset} />;
      case 'assignment':
      case 'lab':
        return <StructuredSlide asset={asset} />;
      case 'html_bundle':
        return <HtmlBundleSlide asset={asset} />;
      default:
        return <DownloadCard asset={asset} />;
    }
  })();

  return <div className={className}>{content}</div>;
}
