import { useMemo } from 'react';
import { marked } from 'marked';

function youtubeId(url) {
  const m = (url || '').match(
    /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/))([A-Za-z0-9_-]{11})/
  );
  return m ? m[1] : null;
}

function renderMarkdown(text) {
  return marked.parse(text || '', { async: false });
}

/** Office Online's viewer fetches the file itself, so this only works for a URL its
 * servers can actually reach — never a localhost/private-network one. No key needed
 * either way; it's the same free, unauthenticated embed SharePoint/OneDrive use for
 * public link previews. */
function isPubliclyReachable(url) {
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

function InlineText({ asset }) {
  const html = useMemo(() => renderMarkdown(asset.body), [asset.body]);
  return (
    <div
      className="markdown-content px-1"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

function CodeSnippet({ asset }) {
  const language = asset.config?.language || 'text';
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
      <div className="flex items-center gap-2 border-b border-slate-800 bg-slate-800/60 px-4 py-2.5">
        <span className="h-3 w-3 rounded-full bg-red-500/80" />
        <span className="h-3 w-3 rounded-full bg-yellow-500/80" />
        <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
        <span className="ml-3 rounded bg-slate-700/60 px-2 py-0.5 font-mono text-xs text-slate-300">
          {language}
        </span>
      </div>
      <pre className="overflow-x-auto p-5 text-sm leading-relaxed">
        <code className="font-mono text-slate-100">{asset.body || ''}</code>
      </pre>
    </div>
  );
}

function PdfView({ asset }) {
  const src = asset.file_url || null;
  if (!src) return <DownloadCard asset={asset} message="This PDF isn't available for preview." />;
  return (
    <div className="h-[70vh] overflow-hidden rounded-2xl border border-slate-800 shadow-xl">
      <iframe src={`${src}#toolbar=1&view=FitH`} title={asset.title} className="h-full w-full" />
    </div>
  );
}

function VideoView({ asset }) {
  const src = asset.file_url || null;
  if (!src) return <DownloadCard asset={asset} message="This video isn't available." />;
  return (
    <video
      src={src}
      controls
      className="w-full rounded-2xl border border-slate-800 shadow-xl"
      style={{ maxHeight: '70vh' }}
    />
  );
}

function PptView({ asset }) {
  const src = asset.file_url || null;

  if (!src || !isPubliclyReachable(src)) {
    return (
      <DownloadCard
        asset={asset}
        message={
          src
            ? "Preview isn't available from a local address — download to view."
            : "This presentation isn't available."
        }
      />
    );
  }

  const embedSrc = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(src)}`;

  return (
    <div className="space-y-2">
      <div className="h-[70vh] overflow-hidden rounded-2xl border border-slate-800 bg-white shadow-xl">
        <iframe src={embedSrc} title={asset.title} className="h-full w-full" />
      </div>
      <div className="flex items-center justify-between text-xs text-slate-500">
        <span>Rendered by Microsoft Office Online</span>
        <a href={src} target="_blank" rel="noopener noreferrer" className="text-primary-400 hover:text-primary-300">
          Download instead
        </a>
      </div>
    </div>
  );
}

function YoutubeView({ asset }) {
  const vid = youtubeId(asset.external_url);
  if (!vid) return <LinkCard url={asset.external_url} label="Watch on YouTube" />;
  return (
    <div className="aspect-video overflow-hidden rounded-2xl border border-slate-800 shadow-xl">
      <iframe
        src={`https://www.youtube-nocookie.com/embed/${vid}?rel=0`}
        title={asset.title}
        className="h-full w-full"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    </div>
  );
}

function LinkCard({ url, label }) {
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="group flex items-center gap-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-6 transition hover:border-primary-500/50 hover:bg-slate-900"
    >
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary-500/10 text-primary-400">
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
          />
        </svg>
      </div>
      <div className="min-w-0 flex-1">
        <p className="font-medium text-white group-hover:text-primary-300">{label}</p>
        <p className="mt-0.5 truncate text-sm text-slate-500">{url}</p>
      </div>
    </a>
  );
}

function QuizView({ asset }) {
  const questions = asset.config?.questions || [];
  return (
    <div className="space-y-5">
      {questions.map((q, qi) => (
        <div key={qi} className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <p className="mb-3 font-medium text-white">
            <span className="mr-2 text-primary-400">Q{qi + 1}.</span>
            {q.question}
          </p>
          <div className="space-y-2">
            {(q.options || []).map((opt, oi) => (
              <div
                key={oi}
                className="rounded-xl border border-slate-800 px-4 py-2.5 text-sm text-slate-300"
              >
                {opt}
              </div>
            ))}
          </div>
        </div>
      ))}
      {questions.length === 0 && (
        <p className="text-center text-slate-500">No questions in this quiz yet.</p>
      )}
    </div>
  );
}

function StructuredView({ asset }) {
  const config = asset.config || {};
  const instructions = config.instructions || config.description || '';
  const steps = config.steps || [];
  const html = useMemo(() => renderMarkdown(instructions), [instructions]);

  return (
    <div className="space-y-5">
      {instructions && (
        <div className="markdown-content" dangerouslySetInnerHTML={{ __html: html }} />
      )}
      {steps.length > 0 && (
        <ol className="space-y-3">
          {steps.map((step, i) => (
            <li key={i} className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
              <div className="flex items-start gap-3">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary-500 text-sm font-bold text-white">
                  {i + 1}
                </span>
                <div className="min-w-0">
                  <p className="font-medium text-white">{step.title}</p>
                  {step.instructions && (
                    <div
                      className="markdown-content mt-1 text-sm"
                      dangerouslySetInnerHTML={{ __html: renderMarkdown(step.instructions) }}
                    />
                  )}
                </div>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

function CsvView({ asset }) {
  const src = asset.file_url || null;
  const preview = asset.csv_preview;

  if (!src) return <DownloadCard asset={asset} message="This file isn't available." />;
  if (!preview) return <DownloadCard asset={asset} message="Couldn't load this file for preview." />;

  return (
    <div className="space-y-2">
      <div className="max-h-[60vh] overflow-auto rounded-2xl border border-slate-800">
        <table className="w-full text-left text-sm">
          <thead className="sticky top-0 bg-slate-800">
            <tr>
              {preview.header.map((cell, i) => (
                <th key={i} className="whitespace-nowrap px-3 py-2 font-medium text-slate-200">
                  {cell}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.rows.map((r, ri) => (
              <tr key={ri} className="border-t border-slate-800 odd:bg-slate-900/40">
                {r.map((cell, ci) => (
                  <td key={ci} className="whitespace-nowrap px-3 py-1.5 text-slate-300">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between text-xs text-slate-500">
        <span>
          {preview.truncated
            ? `Showing first ${preview.rows.length} rows — download for the full file`
            : `${preview.total_rows} row${preview.total_rows === 1 ? '' : 's'}`}
        </span>
        <a href={src} target="_blank" rel="noopener noreferrer" className="text-primary-400 hover:text-primary-300">
          Download full file
        </a>
      </div>
    </div>
  );
}

function DownloadCard({ asset, message }) {
  const src = asset.file_url || null;
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-8 text-center">
      <p className="font-medium text-white">{asset.title}</p>
      {message && <p className="mt-1 text-sm text-slate-500">{message}</p>}
      {src && (
        <a
          href={src}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-flex items-center gap-2 rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600"
        >
          Download
        </a>
      )}
    </div>
  );
}

export default function ClassroomAssetView({ asset }) {
  if (!asset) return null;

  switch (asset.asset_type) {
    case 'markdown':
    case 'notes':
    case 'cheat_sheet':
      return <InlineText asset={asset} />;
    case 'code_snippet':
      return <CodeSnippet asset={asset} />;
    case 'pdf':
      return <PdfView asset={asset} />;
    case 'ppt':
      return <PptView asset={asset} />;
    case 'video':
      return <VideoView asset={asset} />;
    case 'csv':
      return <CsvView asset={asset} />;
    case 'youtube':
      return <YoutubeView asset={asset} />;
    case 'external_url':
      return <LinkCard url={asset.external_url} label={asset.title} />;
    case 'github_repo':
      return <LinkCard url={asset.external_url} label={`View on GitHub — ${asset.title}`} />;
    case 'quiz':
      return <QuizView asset={asset} />;
    case 'assignment':
    case 'lab':
      return <StructuredView asset={asset} />;
    default:
      return <DownloadCard asset={asset} />;
  }
}
