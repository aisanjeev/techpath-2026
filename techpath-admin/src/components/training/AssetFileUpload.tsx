'use client';

import { useRef, useState } from 'react';
import { Upload, X, CheckCircle2, FileWarning } from 'lucide-react';
import toast from 'react-hot-toast';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';
import { trainingService } from '@/services/training.service';
import { formatBytes } from '@/components/training/asset-type-registry';
import { cn } from '@/lib/utils/cn';
import type { AssetType, AssetTypeInfo } from '@/types/training';

interface AssetFileUploadProps {
  assetType: AssetType;
  rules?: AssetTypeInfo;
  value?: { id: number; filename: string; size: number } | null;
  onChange: (file: { id: number; filename: string; size: number; url: string } | null) => void;
}

/**
 * Drag-and-drop upload for file-backed assets.
 *
 * Shows real progress: these go up to 500MB, and a half-gigabyte upload with no
 * feedback is indistinguishable from a hang.
 */
export function AssetFileUpload({ assetType, rules, value, onChange }: AssetFileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const maxBytes = (rules?.max_size_mb ?? 10) * 1024 * 1024;
  const accept = rules?.allowed_extensions?.join(',') ?? undefined;

  const handleFile = async (file: File) => {
    setError(null);

    // Check locally first so an oversized file fails instantly instead of after a long
    // upload that the server was always going to reject.
    if (file.size > maxBytes) {
      const message = `That file is ${formatBytes(file.size)}. The limit for this type is ${rules?.max_size_mb}MB.`;
      setError(message);
      toast.error(message);
      return;
    }

    setUploading(true);
    setProgress(0);
    try {
      const result = await trainingService.uploadAssetFile(assetType, file, setProgress);
      onChange({
        id: result.data.id,
        filename: result.data.filename,
        size: result.data.size,
        url: result.data.url,
      });
      toast.success('File uploaded');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Upload failed';
      setError(message);
      toast.error(message);
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  if (value) {
    return (
      <div className="flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 px-4 py-3">
        <div className="flex min-w-0 items-center gap-3">
          <CheckCircle2 className="h-5 w-5 shrink-0 text-teal-600" />
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-gray-900">{value.filename}</p>
            <p className="text-xs text-gray-500">{formatBytes(value.size)}</p>
          </div>
        </div>
        <button
          type="button"
          onClick={() => onChange(null)}
          className="rounded p-1 text-gray-400 hover:bg-gray-200 hover:text-gray-600"
          aria-label="Remove file"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    );
  }

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          const file = e.dataTransfer.files?.[0];
          if (file) void handleFile(file);
        }}
        onClick={() => !uploading && inputRef.current?.click()}
        className={cn(
          'flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed px-6 py-8 transition-colors',
          dragging ? 'border-teal-500 bg-teal-50' : 'border-gray-300 hover:border-gray-400',
          uploading && 'cursor-wait opacity-75',
          error && 'border-red-300'
        )}
      >
        {uploading ? (
          <div className="w-full max-w-xs text-center">
            <Spinner size="md" />
            <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-gray-200">
              <div
                className="h-full bg-teal-600 transition-all duration-200"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="mt-2 text-xs text-gray-600">Uploading… {progress}%</p>
          </div>
        ) : (
          <>
            <Upload className="h-8 w-8 text-gray-400" />
            <p className="mt-2 text-sm font-medium text-gray-700">
              Drop a file here, or click to browse
            </p>
            {rules && (
              <p className="mt-1 text-xs text-gray-500">
                {rules.allowed_extensions.join(', ')} · up to {rules.max_size_mb}MB
              </p>
            )}
          </>
        )}
      </div>

      {error && (
        <p className="mt-2 flex items-center gap-1.5 text-xs text-red-600">
          <FileWarning className="h-3.5 w-3.5 shrink-0" />
          {error}
        </p>
      )}

      <input
        ref={inputRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) void handleFile(file);
          e.target.value = '';
        }}
      />
    </div>
  );
}
