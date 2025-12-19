'use client';

import { useState, useRef, useCallback } from 'react';
import { Upload, X, Image as ImageIcon, Loader2, FolderOpen } from 'lucide-react';
import toast from 'react-hot-toast';
import { cn } from '@/lib/utils/cn';
import { mediaService } from '@/services/media.service';
import { Button } from './Button';
import { ImagePickerModal } from './ImagePickerModal';

interface ImageUploadProps {
  value?: string;
  onChange: (url: string, fileId?: number) => void;
  folder?: string;
  className?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: boolean;
  entityType?: string;
  entityId?: number;
  fieldName?: string;
}

export function ImageUpload({
  value,
  onChange,
  folder = 'images',
  className,
  placeholder = 'Click to upload or drag and drop',
  disabled = false,
  error = false,
  entityType,
  entityId,
  fieldName = 'featured_image',
}: ImageUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [pickerOpen, setPickerOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = useCallback(
    async (file: File) => {
      // Validate file type
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
      if (!validTypes.includes(file.type)) {
        toast.error('Please select a valid image file (JPEG, PNG, GIF, WebP)');
        return;
      }

      // Validate file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        toast.error('Image must be less than 5MB');
        return;
      }

      setIsUploading(true);
      try {
        const response = await mediaService.uploadImage(
          file,
          folder,
          entityType,
          entityId,
          fieldName
        );
        onChange(response.data.url, response.data.id);
        toast.success(response.is_duplicate ? 'Using existing file' : 'Image uploaded successfully');
      } catch (error) {
        console.error('Upload error:', error);
        toast.error('Failed to upload image');
      } finally {
        setIsUploading(false);
      }
    },
    [folder, onChange, entityType, entityId, fieldName]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
    // Reset input so same file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled && !isUploading) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (disabled || isUploading) return;

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleRemove = () => {
    onChange('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUploadClick = () => {
    if (!disabled && !isUploading) {
      fileInputRef.current?.click();
    }
  };

  const handleBrowseLibrary = () => {
    if (!disabled && !isUploading) {
      setPickerOpen(true);
    }
  };

  const handleSelectFromPicker = (url: string, fileId?: number) => {
    onChange(url, fileId);
  };

  return (
    <div className={cn('space-y-2', className)}>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/gif,image/webp"
        onChange={handleInputChange}
        className="hidden"
        disabled={disabled || isUploading}
      />

      {value ? (
        <div className="relative group">
          <div
            className={cn(
              'relative aspect-video w-full overflow-hidden rounded-lg border bg-gray-50',
              error ? 'border-red-500' : 'border-gray-300'
            )}
          >
            <img
              src={value}
              alt="Uploaded image"
              className="h-full w-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = '/placeholder-image.png';
              }}
            />
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
              <Button
                type="button"
                variant="secondary"
                size="sm"
                onClick={handleBrowseLibrary}
                disabled={isUploading}
              >
                <FolderOpen className="h-4 w-4" />
                Browse
              </Button>
              <Button
                type="button"
                variant="secondary"
                size="sm"
                onClick={handleUploadClick}
                disabled={isUploading}
              >
                {isUploading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Upload className="h-4 w-4" />
                )}
                Upload
              </Button>
              <Button
                type="button"
                variant="destructive"
                size="sm"
                onClick={handleRemove}
                disabled={isUploading}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          <div
            onClick={handleUploadClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={cn(
              'flex flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed p-6 transition-colors cursor-pointer',
              isDragging
                ? 'border-teal-500 bg-teal-50'
                : error
                ? 'border-red-500 bg-red-50'
                : 'border-gray-300 hover:border-teal-400 hover:bg-gray-50',
              (disabled || isUploading) && 'cursor-not-allowed opacity-50'
            )}
          >
            {isUploading ? (
              <>
                <Loader2 className="h-8 w-8 text-teal-500 animate-spin" />
                <p className="text-sm text-gray-600">Uploading...</p>
              </>
            ) : (
              <>
                <ImageIcon className="h-8 w-8 text-gray-400" />
                <div className="text-center">
                  <p className="text-sm font-medium text-gray-700">{placeholder}</p>
                  <p className="mt-1 text-xs text-gray-500">
                    PNG, JPG, GIF, WebP up to 5MB
                  </p>
                </div>
              </>
            )}
          </div>
          
          {/* Browse Library Button */}
          <button
            type="button"
            onClick={handleBrowseLibrary}
            disabled={disabled || isUploading}
            className={cn(
              'w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors',
              (disabled || isUploading) && 'cursor-not-allowed opacity-50'
            )}
          >
            <FolderOpen className="h-4 w-4" />
            Browse Media Library
          </button>
        </div>
      )}

      {/* Image Picker Modal */}
      <ImagePickerModal
        isOpen={pickerOpen}
        onClose={() => setPickerOpen(false)}
        onSelect={handleSelectFromPicker}
        folder={folder}
        entityType={entityType}
        entityId={entityId}
        fieldName={fieldName}
      />
    </div>
  );
}
