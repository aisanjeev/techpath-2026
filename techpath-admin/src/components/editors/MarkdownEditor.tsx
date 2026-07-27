'use client';

import { useState, useCallback } from 'react';
import {
  Bold,
  Italic,
  Strikethrough,
  Code,
  List,
  ListOrdered,
  Quote,
  Link as LinkIcon,
  Image as ImageIcon,
  Heading1,
  Heading2,
  Heading3,
  Minus,
  Eye,
  Edit3,
  Code2,
} from 'lucide-react';
import { cn } from '@/lib/utils/cn';
import { marked } from 'marked';

interface MarkdownEditorProps {
  content: string;
  onChange: (content: string) => void;
  placeholder?: string;
  className?: string;
  error?: boolean;
  minHeight?: string;
}

export function MarkdownEditor({
  content,
  onChange,
  placeholder = 'Write your content in Markdown...',
  className,
  error,
  minHeight = '400px',
}: MarkdownEditorProps) {
  const [mode, setMode] = useState<'edit' | 'preview' | 'split'>('edit');

  const insertMarkdown = useCallback(
    (before: string, after: string = '', placeholder: string = '') => {
      const textarea = document.getElementById('markdown-textarea') as HTMLTextAreaElement;
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selectedText = content.substring(start, end) || placeholder;
      
      const newContent =
        content.substring(0, start) +
        before +
        selectedText +
        after +
        content.substring(end);
      
      onChange(newContent);

      // Restore cursor position after React re-renders
      setTimeout(() => {
        textarea.focus();
        const newCursorPos = start + before.length + selectedText.length;
        textarea.setSelectionRange(newCursorPos, newCursorPos);
      }, 0);
    },
    [content, onChange]
  );

  const toolbarActions = [
    { icon: Bold, action: () => insertMarkdown('**', '**', 'bold text'), title: 'Bold (Ctrl+B)' },
    { icon: Italic, action: () => insertMarkdown('*', '*', 'italic text'), title: 'Italic (Ctrl+I)' },
    { icon: Strikethrough, action: () => insertMarkdown('~~', '~~', 'strikethrough'), title: 'Strikethrough' },
    { icon: Code, action: () => insertMarkdown('`', '`', 'code'), title: 'Inline Code' },
    { type: 'divider' },
    { icon: Heading1, action: () => insertMarkdown('\n# ', '\n', 'Heading 1'), title: 'Heading 1' },
    { icon: Heading2, action: () => insertMarkdown('\n## ', '\n', 'Heading 2'), title: 'Heading 2' },
    { icon: Heading3, action: () => insertMarkdown('\n### ', '\n', 'Heading 3'), title: 'Heading 3' },
    { type: 'divider' },
    { icon: List, action: () => insertMarkdown('\n- ', '\n', 'list item'), title: 'Bullet List' },
    { icon: ListOrdered, action: () => insertMarkdown('\n1. ', '\n', 'list item'), title: 'Numbered List' },
    { icon: Quote, action: () => insertMarkdown('\n> ', '\n', 'quote'), title: 'Blockquote' },
    { icon: Code2, action: () => insertMarkdown('\n```\n', '\n```\n', 'code block'), title: 'Code Block' },
    { icon: Minus, action: () => insertMarkdown('\n---\n', '', ''), title: 'Horizontal Rule' },
    { type: 'divider' },
    { icon: LinkIcon, action: () => insertMarkdown('[', '](url)', 'link text'), title: 'Link' },
    { icon: ImageIcon, action: () => insertMarkdown('![', '](image-url)', 'alt text'), title: 'Image' },
  ];

  // Simple markdown to HTML converter for preview
  const renderMarkdown = (md: string): string => {
    const processedText = md ? md.replace(/\\n/g, '\n') : '';
    return marked.parse(processedText, { async: false }) as string;
  };

  return (
    <div
      className={cn(
        'overflow-hidden rounded-lg border bg-white',
        error ? 'border-red-500' : 'border-gray-300',
        className
      )}
    >
      {/* Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-1 border-b border-gray-200 bg-gray-50 p-2">
        <div className="flex flex-wrap items-center gap-1">
          {toolbarActions.map((item, index) =>
            item.type === 'divider' ? (
              <div key={index} className="mx-1 h-6 w-px bg-gray-300" />
            ) : (
              <button
                key={index}
                type="button"
                onClick={item.action}
                title={item.title}
                className="rounded p-1.5 text-gray-600 transition-colors hover:bg-gray-200 hover:text-gray-900"
              >
                {item.icon && <item.icon className="h-4 w-4" />}
              </button>
            )
          )}
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center gap-1 rounded-lg bg-gray-200 p-0.5">
          <button
            type="button"
            onClick={() => setMode('edit')}
            className={cn(
              'flex items-center gap-1 rounded px-2 py-1 text-xs font-medium transition-colors',
              mode === 'edit'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            )}
          >
            <Edit3 className="h-3 w-3" />
            Edit
          </button>
          <button
            type="button"
            onClick={() => setMode('split')}
            className={cn(
              'rounded px-2 py-1 text-xs font-medium transition-colors',
              mode === 'split'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            )}
          >
            Split
          </button>
          <button
            type="button"
            onClick={() => setMode('preview')}
            className={cn(
              'flex items-center gap-1 rounded px-2 py-1 text-xs font-medium transition-colors',
              mode === 'preview'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            )}
          >
            <Eye className="h-3 w-3" />
            Preview
          </button>
        </div>
      </div>

      {/* Editor Content */}
      <div className={cn('flex', mode === 'split' ? 'divide-x divide-gray-200' : '')}>
        {/* Markdown Input */}
        {(mode === 'edit' || mode === 'split') && (
          <div className={cn(mode === 'split' ? 'w-1/2' : 'w-full')}>
            <textarea
              id="markdown-textarea"
              value={content}
              onChange={(e) => onChange(e.target.value)}
              placeholder={placeholder}
              className={cn(
                'w-full resize-none bg-white px-4 py-3 font-mono text-sm focus:outline-none',
                error ? 'text-red-900' : 'text-gray-900'
              )}
              style={{ minHeight }}
            />
          </div>
        )}

        {/* Preview */}
        {(mode === 'preview' || mode === 'split') && (
          <div
            className={cn(
              'overflow-auto bg-white px-4 py-3',
              mode === 'split' ? 'w-1/2' : 'w-full'
            )}
            style={{ minHeight }}
          >
            {content ? (
              <div
                className="prose prose-sm max-w-none"
                dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
              />
            ) : (
              <p className="text-gray-400 italic">Nothing to preview...</p>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50 px-4 py-2 text-xs text-gray-500">
        <span>{content.length} characters</span>
        <span>Markdown supported</span>
      </div>
    </div>
  );
}

