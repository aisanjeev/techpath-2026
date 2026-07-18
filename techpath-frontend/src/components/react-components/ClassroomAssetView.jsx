import { useMemo, useState } from 'react';
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

/**
 * A takeable, server-graded quiz — one question at a time.
 *
 * `asset.config.questions` here carries only `question` and `options`; the backend
 * strips the answer key for students. The only correctness information this component
 * ever has is what comes back from a submitted attempt, which is why feedback renders
 * from `result.questions` rather than from the asset.
 *
 * One question per screen rather than a long scroll: it keeps a projected classroom on
 * the same question at the same time, and stops a student skimming ahead while the
 * trainer is still talking about Q1.
 *
 * `onSubmit` is injected so the same component serves both surfaces — the portal posts
 * as a signed-in student, the live classroom posts as a session participant. Without
 * it the quiz still renders and can be answered, but says so plainly instead of
 * showing a submit button that would go nowhere.
 */
function QuizView({ asset, onSubmit, initialResult }) {
  const questions = asset.config?.questions || [];
  const [selected, setSelected] = useState({});
  const [step, setStep] = useState(0);
  const [result, setResult] = useState(initialResult || null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  if (questions.length === 0) {
    return <p className="text-center text-slate-500">No questions in this quiz yet.</p>;
  }

  const answeredCount = questions.filter((_, i) => selected[i] != null).length;
  const allAnswered = answeredCount === questions.length;
  const feedbackByIndex = {};
  if (result) {
    for (const f of result.questions || []) feedbackByIndex[f.index] = f;
  }

  const submit = async () => {
    if (!allAnswered || submitting || !onSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await onSubmit(questions.map((_, i) => selected[i]));
      if (res?.success === false) {
        setError(res.error || 'Could not submit your answers.');
      } else {
        setResult(res);
        setStep(0);
      }
    } catch (err) {
      setError(err?.message || 'Could not submit your answers.');
    } finally {
      setSubmitting(false);
    }
  };

  const retry = () => {
    setSelected({});
    setResult(null);
    setError(null);
    setStep(0);
  };

  const isLast = step === questions.length - 1;
  const q = questions[step];
  const feedback = feedbackByIndex[step];
  const chosen = feedback ? feedback.your_answer : selected[step];
  // After submitting, every question is navigable so a student can read all the
  // explanations. Before submitting, Next requires an answer for the current one.
  const canAdvance = result ? !isLast : !isLast && selected[step] != null;

  return (
    <div className="space-y-4">
      {result && (
        <div
          className={`rounded-2xl border p-5 ${
            result.passed
              ? 'border-emerald-600/50 bg-emerald-950/30'
              : 'border-amber-600/50 bg-amber-950/30'
          }`}
        >
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p
                className={`font-semibold ${
                  result.passed ? 'text-emerald-300' : 'text-amber-300'
                }`}
              >
                {result.passed ? 'Passed' : 'Not passed yet'}
              </p>
              <p className="mt-0.5 text-sm text-slate-400">
                {result.score} of {result.total_questions} correct (
                {Math.round(result.percentage)}%) · {Math.round(result.pass_mark * 100)}% needed
              </p>
            </div>
            <button
              onClick={retry}
              className="rounded-xl border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800"
            >
              {result.passed ? 'Try again' : 'Retry quiz'}
            </button>
          </div>
        </div>
      )}

      {/* Step dots: where you are, and which questions still need an answer. */}
      <div className="flex flex-wrap items-center gap-1.5">
        {questions.map((_, i) => {
          const fb = feedbackByIndex[i];
          let tone = 'bg-slate-700';
          if (fb) tone = fb.is_correct ? 'bg-emerald-500' : 'bg-red-500';
          else if (selected[i] != null) tone = 'bg-primary-500';
          return (
            <button
              key={i}
              type="button"
              onClick={() => setStep(i)}
              aria-label={`Go to question ${i + 1}`}
              className={`h-1.5 rounded-full transition-all ${tone} ${
                i === step ? 'w-8 ring-2 ring-primary-400/60' : 'w-5 hover:opacity-80'
              }`}
            />
          );
        })}
      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
        <div className="mb-1 flex items-center justify-between">
          <span className="text-xs font-medium uppercase tracking-wide text-primary-400">
            Question {step + 1} of {questions.length}
          </span>
          {!result && <span className="text-xs text-slate-500">{answeredCount} answered</span>}
        </div>
        <p className="mb-4 text-base font-medium text-white">{q.question}</p>

        <div className="space-y-2">
          {(q.options || []).map((opt, oi) => {
            const isChosen = chosen === oi;
            // Correctness is only known after submitting — before that, this component
            // genuinely does not have the answer.
            const isCorrect = feedback && feedback.correct_index === oi;
            const isWrongChoice = feedback && isChosen && !feedback.is_correct;

            let tone =
              'border-slate-700 text-slate-200 hover:border-primary-500 hover:bg-primary-500/5';
            if (isCorrect) tone = 'border-emerald-600/60 bg-emerald-950/30 text-emerald-200';
            else if (isWrongChoice) tone = 'border-red-600/60 bg-red-950/30 text-red-200';
            else if (isChosen) tone = 'border-primary-500 bg-primary-500/10 text-white';

            return (
              <button
                key={oi}
                type="button"
                disabled={!!result || submitting}
                onClick={() => setSelected((s) => ({ ...s, [step]: oi }))}
                className={`flex w-full items-center gap-3 rounded-xl border px-4 py-3 text-left text-sm transition disabled:cursor-default ${tone}`}
              >
                <span
                  className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-[11px] ${
                    isChosen || isCorrect ? 'border-current' : 'border-slate-600'
                  }`}
                >
                  {isCorrect ? '✓' : isWrongChoice ? '✕' : isChosen ? '•' : ''}
                </span>
                <span className="min-w-0 flex-1">{opt}</span>
              </button>
            );
          })}
        </div>

        {feedback?.explanation && (
          <p className="mt-4 rounded-xl bg-slate-800/60 px-4 py-3 text-sm text-slate-300">
            {feedback.explanation}
          </p>
        )}
      </div>

      {error && (
        <p className="rounded-xl border border-red-800 bg-red-950/40 px-4 py-3 text-sm text-red-300">
          {error}
        </p>
      )}

      <div className="flex items-center justify-between gap-3">
        <button
          type="button"
          onClick={() => setStep((s) => Math.max(0, s - 1))}
          disabled={step === 0}
          className="rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-medium text-slate-200 transition hover:bg-slate-800 disabled:opacity-40"
        >
          Back
        </button>

        {isLast && !result ? (
          onSubmit ? (
            <button
              type="button"
              onClick={submit}
              disabled={!allAnswered || submitting}
              title={!allAnswered ? 'Answer every question first' : undefined}
              className="rounded-xl bg-primary-500 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {submitting ? 'Submitting…' : 'Submit answers'}
            </button>
          ) : (
            <span className="text-xs text-slate-500">Submitting is not available here</span>
          )
        ) : (
          <button
            type="button"
            onClick={() => setStep((s) => Math.min(questions.length - 1, s + 1))}
            disabled={!canAdvance}
            title={!canAdvance && !result ? 'Choose an answer to continue' : undefined}
            className="rounded-xl bg-primary-500 px-6 py-2.5 text-sm font-medium text-white transition hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Next
          </button>
        )}
      </div>
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

export default function ClassroomAssetView({ asset, onQuizSubmit, quizResult }) {
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
      return <QuizView asset={asset} onSubmit={onQuizSubmit} initialResult={quizResult} />;
    case 'assignment':
    case 'lab':
      return <StructuredView asset={asset} />;
    default:
      return <DownloadCard asset={asset} />;
  }
}
