'use client';

import { forwardRef, useImperativeHandle, useRef, useState } from 'react';
import Editor, { type OnMount } from '@monaco-editor/react';
import { Sun, Moon, AlignLeft, Check, Copy, ImagePlus } from 'lucide-react';
import { cn } from '@/lib/utils/cn';
import { Spinner } from '@/components/ui/Spinner';

export interface CodeEditorHandle {
  insertAtCursor: (text: string) => void;
}

interface CodeEditorProps {
  value: string;
  onChange?: (value: string) => void;
  language?: string;
  className?: string;
  error?: boolean;
  readOnly?: boolean;
  height?: string;
  showMinimap?: boolean;
  onInsertImage?: () => void;
}

export const CodeEditor = forwardRef<CodeEditorHandle, CodeEditorProps>(function CodeEditor(
  {
    value,
    onChange,
    language = 'javascript',
    className,
    error,
    readOnly = false,
    height = '400px',
    showMinimap = false,
    onInsertImage,
  },
  ref
) {
  const [editorTheme, setEditorTheme] = useState<'vs-dark' | 'vs-light'>('vs-dark');
  const [wordWrap, setWordWrap] = useState<'on' | 'off'>('on');
  const [copied, setCopied] = useState(false);
  const monacoEditorRef = useRef<Parameters<OnMount>[0] | null>(null);
  const onChangeRef = useRef(onChange);
  onChangeRef.current = onChange;

  const handleEditorMount: OnMount = (editor) => {
    monacoEditorRef.current = editor;
  };

  useImperativeHandle(ref, () => ({
    insertAtCursor: (text: string) => {
      const editor = monacoEditorRef.current;
      if (!editor) return;
      const selection = editor.getSelection();
      if (!selection) return;
      editor.executeEdits('insert-image', [
        { range: selection, text, forceMoveMarkers: true },
      ]);
      // @monaco-editor/react filters out programmatic edits from its onChange
      // callback, so we manually sync the updated value to React state.
      const updatedValue = editor.getValue();
      onChangeRef.current?.(updatedValue);
      editor.focus();
    },
  }));

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text', err);
    }
  };

  return (
    <div
      className={cn(
        'relative overflow-hidden rounded-xl border shadow-lg transition-all duration-300',
        editorTheme === 'vs-dark' ? 'border-gray-800 bg-gray-950' : 'border-gray-200 bg-white',
        error ? 'border-red-500 ring-1 ring-red-500' : '',
        className
      )}
    >
      {/* IDE Header */}
      <div
        className={cn(
          'flex h-11 items-center justify-between px-4 border-b transition-colors duration-300',
          editorTheme === 'vs-dark'
            ? 'border-gray-800 bg-gray-900/80 text-gray-400'
            : 'border-gray-200 bg-gray-50 text-gray-600'
        )}
      >
        {/* Mock OS Window Controls */}
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-rose-500/80 hover:bg-rose-500 transition-colors" />
          <span className="h-3 w-3 rounded-full bg-amber-500/80 hover:bg-amber-500 transition-colors" />
          <span className="h-3 w-3 rounded-full bg-emerald-500/80 hover:bg-emerald-500 transition-colors" />
          <span
            className={cn(
              'ml-3 rounded px-2 py-0.5 text-xs font-semibold uppercase tracking-wider',
              editorTheme === 'vs-dark' ? 'bg-gray-800 text-gray-300' : 'bg-gray-200 text-gray-700'
            )}
          >
            {language}
          </span>
          {readOnly && (
            <span className="rounded bg-teal-500/10 text-teal-500 px-2 py-0.5 text-xs font-medium border border-teal-500/20">
              Preview Mode
            </span>
          )}
        </div>

        {/* Toolbar Controls */}
        <div className="flex items-center gap-1.5">
          {readOnly ? (
            <button
              type="button"
              onClick={handleCopy}
              className={cn(
                'flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium transition-all duration-200 active:scale-95',
                editorTheme === 'vs-dark'
                  ? 'hover:bg-gray-800 hover:text-gray-100'
                  : 'hover:bg-gray-200 hover:text-gray-900'
              )}
              title="Copy Code"
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5 text-emerald-500" />
                  <span className="text-emerald-500">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" />
                  <span>Copy</span>
                </>
              )}
            </button>
          ) : (
            <>
              {/* Insert Image */}
              {onInsertImage && (
                <button
                  type="button"
                  onClick={onInsertImage}
                  className={cn(
                    'rounded-md p-1.5 transition-colors',
                    editorTheme === 'vs-dark'
                      ? 'hover:bg-gray-800 hover:text-gray-100'
                      : 'hover:bg-gray-200 hover:text-gray-900'
                  )}
                  title="Insert Image"
                >
                  <ImagePlus className="h-4 w-4" />
                </button>
              )}

              {/* Word Wrap Toggle */}
              <button
                type="button"
                onClick={() => setWordWrap((prev) => (prev === 'on' ? 'off' : 'on'))}
                className={cn(
                  'rounded-md p-1.5 transition-colors',
                  wordWrap === 'on'
                    ? 'text-teal-500 bg-teal-500/10'
                    : editorTheme === 'vs-dark'
                    ? 'hover:bg-gray-800 hover:text-gray-100'
                    : 'hover:bg-gray-200 hover:text-gray-900'
                )}
                title="Toggle Word Wrap"
              >
                <AlignLeft className="h-4 w-4" />
              </button>

              {/* Theme Toggle */}
              <button
                type="button"
                onClick={() => setEditorTheme((prev) => (prev === 'vs-dark' ? 'vs-light' : 'vs-dark'))}
                className={cn(
                  'rounded-md p-1.5 transition-colors',
                  editorTheme === 'vs-dark'
                    ? 'hover:bg-gray-800 hover:text-gray-100'
                    : 'hover:bg-gray-200 hover:text-gray-900'
                )}
                title="Toggle Theme"
              >
                {editorTheme === 'vs-dark' ? (
                  <Sun className="h-4 w-4" />
                ) : (
                  <Moon className="h-4 w-4" />
                )}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Editor Frame */}
      <div className="relative">
        <Editor
          height={height}
          language={language}
          theme={editorTheme}
          value={value}
          onChange={(val) => onChange?.(val ?? '')}
          onMount={handleEditorMount}
          options={{
            readOnly,
            minimap: { enabled: showMinimap },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
            wordWrap,
            padding: { top: 12, bottom: 12 },
            cursorBlinking: 'smooth',
            smoothScrolling: true,
            fontFamily: "'Fira Code', 'Courier New', Courier, monospace",
            renderLineHighlight: readOnly ? 'none' : 'all',
          }}
          loading={
            <div
              className={cn(
                'flex h-full items-center justify-center py-20',
                editorTheme === 'vs-dark' ? 'bg-gray-950' : 'bg-gray-50'
              )}
            >
              <Spinner size="lg" />
            </div>
          }
        />
      </div>
    </div>
  );
});
