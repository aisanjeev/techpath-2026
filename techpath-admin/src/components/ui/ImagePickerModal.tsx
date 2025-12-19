'use client';

import { useState, useCallback, useEffect } from 'react';
import { Upload, Search, Check, Image as ImageIcon, Loader2, X } from 'lucide-react';
import toast from 'react-hot-toast';
import { cn } from '@/lib/utils/cn';
import { Modal } from './Modal';
import { Button } from './Button';
import { Input } from './Input';
import { Spinner } from './Spinner';
import { mediaService, type MediaFileListItem } from '@/services/media.service';

interface ImagePickerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (url: string, fileId?: number) => void;
  folder?: string;
  entityType?: string;
  entityId?: number;
  fieldName?: string;
}

export function ImagePickerModal({
  isOpen,
  onClose,
  onSelect,
  folder = 'images',
  entityType,
  entityId,
  fieldName,
}: ImagePickerModalProps) {
  const [activeTab, setActiveTab] = useState<'library' | 'upload'>('library');
  const [files, setFiles] = useState<MediaFileListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedFile, setSelectedFile] = useState<MediaFileListItem | null>(null);
  const [uploading, setUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const fetchFiles = useCallback(async () => {
    setLoading(true);
    try {
      const data = await mediaService.list({
        content_type: 'image',
        search: search || undefined,
        limit: 100,
      });
      setFiles(data);
    } catch (error) {
      console.error('Error fetching media files:', error);
    } finally {
      setLoading(false);
    }
  }, [search]);

  useEffect(() => {
    if (isOpen) {
      fetchFiles();
      setSelectedFile(null);
    }
  }, [isOpen, fetchFiles]);

  const handleFileUpload = async (file: File) => {
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

    setUploading(true);
    try {
      const response = await mediaService.uploadImage(
        file,
        folder,
        entityType,
        entityId,
        fieldName
      );
      
      toast.success(response.is_duplicate ? 'Using existing file' : 'Image uploaded successfully');
      onSelect(response.data.url, response.data.id);
      onClose();
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Failed to upload image');
    } finally {
      setUploading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleSelectFromLibrary = () => {
    if (selectedFile) {
      onSelect(selectedFile.url, selectedFile.id);
      onClose();
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Select Image" size="xl">
      <div className="space-y-4">
        {/* Tabs */}
        <div className="flex border-b border-gray-200">
          <button
            type="button"
            onClick={() => setActiveTab('library')}
            className={cn(
              'flex-1 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'library'
                ? 'border-teal-600 text-teal-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            )}
          >
            <div className="flex items-center justify-center gap-2">
              <ImageIcon className="h-4 w-4" />
              Browse Library
            </div>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('upload')}
            className={cn(
              'flex-1 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'upload'
                ? 'border-teal-600 text-teal-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            )}
          >
            <div className="flex items-center justify-center gap-2">
              <Upload className="h-4 w-4" />
              Upload New
            </div>
          </button>
        </div>

        {/* Library Tab */}
        {activeTab === 'library' && (
          <div className="space-y-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <Input
                placeholder="Search images..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Grid */}
            <div className="h-80 overflow-y-auto">
              {loading ? (
                <div className="flex items-center justify-center h-full">
                  <Spinner size="lg" />
                </div>
              ) : files.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <ImageIcon className="h-12 w-12 text-gray-300 mb-2" />
                  <p className="text-gray-500">No images found</p>
                  <button
                    type="button"
                    onClick={() => setActiveTab('upload')}
                    className="mt-2 text-sm text-teal-600 hover:underline"
                  >
                    Upload a new image
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-4 gap-3">
                  {files.map((file) => (
                    <button
                      key={file.id}
                      type="button"
                      onClick={() => setSelectedFile(file)}
                      className={cn(
                        'relative aspect-square rounded-lg overflow-hidden border-2 transition-all',
                        selectedFile?.id === file.id
                          ? 'border-teal-600 ring-2 ring-teal-600/20'
                          : 'border-gray-200 hover:border-gray-300'
                      )}
                    >
                      <img
                        src={file.url}
                        alt={file.alt_text || file.filename}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = '/placeholder-image.png';
                        }}
                      />
                      {selectedFile?.id === file.id && (
                        <div className="absolute inset-0 bg-teal-600/20 flex items-center justify-center">
                          <div className="bg-teal-600 rounded-full p-1">
                            <Check className="h-4 w-4 text-white" />
                          </div>
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Selected file info & action */}
            <div className="flex items-center justify-between border-t border-gray-200 pt-4">
              <div className="text-sm text-gray-500">
                {selectedFile ? (
                  <span>
                    Selected: <span className="font-medium text-gray-900">{selectedFile.filename}</span>
                    {selectedFile.width && selectedFile.height && (
                      <span className="ml-2">({selectedFile.width}×{selectedFile.height})</span>
                    )}
                  </span>
                ) : (
                  'Select an image from the library'
                )}
              </div>
              <Button
                onClick={handleSelectFromLibrary}
                disabled={!selectedFile}
              >
                Use Selected
              </Button>
            </div>
          </div>
        )}

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="space-y-4">
            <input
              type="file"
              id="image-upload-input"
              accept="image/jpeg,image/png,image/gif,image/webp"
              onChange={handleFileSelect}
              className="hidden"
              disabled={uploading}
            />

            <div
              onClick={() => !uploading && document.getElementById('image-upload-input')?.click()}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={cn(
                'flex flex-col items-center justify-center gap-4 rounded-lg border-2 border-dashed p-12 transition-colors cursor-pointer',
                isDragging
                  ? 'border-teal-500 bg-teal-50'
                  : 'border-gray-300 hover:border-teal-400 hover:bg-gray-50',
                uploading && 'cursor-not-allowed opacity-50'
              )}
            >
              {uploading ? (
                <>
                  <Loader2 className="h-12 w-12 text-teal-500 animate-spin" />
                  <p className="text-sm text-gray-600">Uploading...</p>
                </>
              ) : (
                <>
                  <Upload className="h-12 w-12 text-gray-400" />
                  <div className="text-center">
                    <p className="text-sm font-medium text-gray-700">
                      Click to upload or drag and drop
                    </p>
                    <p className="mt-1 text-xs text-gray-500">
                      PNG, JPG, GIF, WebP up to 5MB
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
}

