'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { Search, Trash2, Eye, Image as ImageIcon, FileText, Upload, Loader2, File, FileType } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Spinner } from '@/components/ui/Spinner';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { mediaService, type MediaFileListItem, type MediaFileDetail } from '@/services/media.service';
import { formatDate } from '@/lib/utils/format';
import { cn } from '@/lib/utils/cn';

export default function MediaLibraryPage() {
  const [files, setFiles] = useState<MediaFileListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [selectedFile, setSelectedFile] = useState<MediaFileDetail | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; file: MediaFileListItem | null }>({
    open: false,
    file: null,
  });
  const [deleting, setDeleting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchFiles = useCallback(async () => {
    setLoading(true);
    try {
      const data = await mediaService.list({
        content_type: typeFilter || undefined,
        search: search || undefined,
        limit: 100,
      });
      setFiles(data);
    } catch (error) {
      console.error('Error fetching media files:', error);
      toast.error('Failed to load media files');
    } finally {
      setLoading(false);
    }
  }, [search, typeFilter]);

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  const handleViewDetails = async (file: MediaFileListItem) => {
    setDetailsLoading(true);
    setDetailsOpen(true);
    try {
      const details = await mediaService.getById(file.id);
      setSelectedFile(details);
    } catch (error) {
      console.error('Error fetching file details:', error);
      toast.error('Failed to load file details');
      setDetailsOpen(false);
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteModal.file) return;
    setDeleting(true);
    try {
      await mediaService.delete(deleteModal.file.id);
      toast.success('File deleted successfully');
      setDeleteModal({ open: false, file: null });
      fetchFiles();
    } catch (error: any) {
      console.error('Error deleting file:', error);
      toast.error(error.message || 'Failed to delete file');
    } finally {
      setDeleting(false);
    }
  };

  const handleCopyUrl = (url: string) => {
    navigator.clipboard.writeText(url);
    toast.success('URL copied to clipboard');
  };

  const handleFileUpload = async (file: File) => {
    // Define valid types
    const imageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    const documentTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
    ];
    const allValidTypes = [...imageTypes, ...documentTypes];

    // Validate file type
    if (!allValidTypes.includes(file.type)) {
      toast.error('Invalid file type. Allowed: Images (JPEG, PNG, GIF, WebP), PDF, Word, Text');
      return;
    }

    // Validate file size
    const isImage = imageTypes.includes(file.type);
    const maxSize = isImage ? 5 * 1024 * 1024 : 10 * 1024 * 1024; // 5MB for images, 10MB for docs
    if (file.size > maxSize) {
      toast.error(`File must be less than ${isImage ? '5MB' : '10MB'}`);
      return;
    }

    setUploading(true);
    try {
      let response;
      if (isImage) {
        response = await mediaService.uploadImage(file, 'images');
      } else {
        response = await mediaService.uploadFile(file, 'documents');
      }
      toast.success(response.is_duplicate ? 'File already exists in library' : 'File uploaded successfully');
      fetchFiles();
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles) {
      Array.from(selectedFiles).forEach(handleFileUpload);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!uploading) {
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

    if (uploading) return;

    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles) {
      Array.from(droppedFiles).forEach(handleFileUpload);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className="relative"
    >
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/gif,image/webp,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain,.pdf,.doc,.docx,.txt"
        onChange={handleInputChange}
        className="hidden"
        multiple
        disabled={uploading}
      />

      {/* Drag overlay */}
      {isDragging && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-teal-500/20 backdrop-blur-sm">
          <div className="rounded-xl border-4 border-dashed border-teal-500 bg-white p-12 shadow-2xl">
            <Upload className="mx-auto h-16 w-16 text-teal-500 mb-4" />
            <p className="text-xl font-semibold text-gray-900">Drop files here to upload</p>
            <p className="text-sm text-gray-500 mt-1">Images (5MB) • PDF, Word, Text (10MB)</p>
          </div>
        </div>
      )}

      <PageHeader
        title="Media Library"
        description="Manage all uploaded images and documents"
        actions={
          <Button
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            {uploading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Uploading...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Upload File
              </>
            )}
          </Button>
        }
      />

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search files..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="w-40"
        >
          <option value="">All Types</option>
          <option value="image">Images</option>
          <option value="document">Documents</option>
        </Select>
      </div>

      {/* File Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : files.length === 0 ? (
        <div
          onClick={() => fileInputRef.current?.click()}
          className={cn(
            'flex flex-col items-center justify-center py-16 text-center rounded-lg border-2 border-dashed cursor-pointer transition-colors',
            'border-gray-300 hover:border-teal-400 hover:bg-gray-50'
          )}
        >
          <Upload className="h-12 w-12 text-gray-400 mb-4" />
          <p className="text-gray-700 font-medium">Click to upload or drag and drop</p>
          <p className="text-sm text-gray-500 mt-1">Images (PNG, JPG, GIF, WebP) • Documents (PDF, Word, Text)</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {files.map((file) => (
            <div
              key={file.id}
              className="group relative bg-white rounded-lg border border-gray-200 overflow-hidden hover:border-teal-500 hover:shadow-md transition-all"
            >
              {/* Preview */}
              <div className="aspect-square bg-gray-100 flex items-center justify-center">
                {file.content_type.startsWith('image/') ? (
                  <img
                    src={file.url}
                    alt={file.alt_text || file.filename}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = '/placeholder-image.png';
                    }}
                  />
                ) : file.content_type === 'application/pdf' ? (
                  <div className="flex flex-col items-center">
                    <FileText className="h-12 w-12 text-red-500" />
                    <span className="text-xs text-red-500 font-medium mt-1">PDF</span>
                  </div>
                ) : file.content_type.includes('word') ? (
                  <div className="flex flex-col items-center">
                    <FileType className="h-12 w-12 text-blue-500" />
                    <span className="text-xs text-blue-500 font-medium mt-1">Word</span>
                  </div>
                ) : file.content_type === 'text/plain' ? (
                  <div className="flex flex-col items-center">
                    <File className="h-12 w-12 text-gray-500" />
                    <span className="text-xs text-gray-500 font-medium mt-1">Text</span>
                  </div>
                ) : (
                  <FileText className="h-12 w-12 text-gray-400" />
                )}
              </div>

              {/* Overlay on hover */}
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => handleViewDetails(file)}
                >
                  <Eye className="h-4 w-4" />
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => setDeleteModal({ open: true, file })}
                  disabled={file.usage_count > 0}
                  title={file.usage_count > 0 ? `Used in ${file.usage_count} place(s)` : 'Delete'}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>

              {/* File info */}
              <div className="p-2">
                <p className="text-xs font-medium text-gray-900 truncate" title={file.filename}>
                  {file.filename}
                </p>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-xs text-gray-500">
                    {mediaService.formatFileSize(file.size)}
                  </span>
                  {file.usage_count > 0 && (
                    <span className="text-xs text-teal-600 font-medium">
                      {file.usage_count} use{file.usage_count !== 1 ? 's' : ''}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* File Details Modal */}
      <Modal
        isOpen={detailsOpen}
        onClose={() => {
          setDetailsOpen(false);
          setSelectedFile(null);
        }}
        title="File Details"
        size="lg"
      >
        {detailsLoading ? (
          <div className="flex items-center justify-center py-8">
            <Spinner size="lg" />
          </div>
        ) : selectedFile ? (
          <div className="space-y-6">
            {/* Preview */}
            <div className="bg-gray-100 rounded-lg p-4 flex items-center justify-center">
              {selectedFile.content_type.startsWith('image/') ? (
                <img
                  src={selectedFile.url}
                  alt={selectedFile.alt_text || selectedFile.filename}
                  className="max-h-64 max-w-full object-contain rounded"
                />
              ) : selectedFile.content_type === 'application/pdf' ? (
                <div className="flex flex-col items-center">
                  <FileText className="h-24 w-24 text-red-500" />
                  <span className="text-sm text-red-500 font-medium mt-2">PDF Document</span>
                  <a
                    href={selectedFile.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 text-sm text-teal-600 hover:underline"
                  >
                    Open in new tab →
                  </a>
                </div>
              ) : selectedFile.content_type.includes('word') ? (
                <div className="flex flex-col items-center">
                  <FileType className="h-24 w-24 text-blue-500" />
                  <span className="text-sm text-blue-500 font-medium mt-2">Word Document</span>
                  <a
                    href={selectedFile.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 text-sm text-teal-600 hover:underline"
                  >
                    Download →
                  </a>
                </div>
              ) : selectedFile.content_type === 'text/plain' ? (
                <div className="flex flex-col items-center">
                  <File className="h-24 w-24 text-gray-500" />
                  <span className="text-sm text-gray-500 font-medium mt-2">Text File</span>
                  <a
                    href={selectedFile.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 text-sm text-teal-600 hover:underline"
                  >
                    Open in new tab →
                  </a>
                </div>
              ) : (
                <FileText className="h-24 w-24 text-gray-400" />
              )}
            </div>

            {/* Info */}
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Filename</p>
                <p className="font-medium">{selectedFile.filename}</p>
              </div>
              <div>
                <p className="text-gray-500">Type</p>
                <p className="font-medium">{mediaService.getFileTypeLabel(selectedFile.content_type)}</p>
              </div>
              <div>
                <p className="text-gray-500">Size</p>
                <p className="font-medium">{mediaService.formatFileSize(selectedFile.size)}</p>
              </div>
              {selectedFile.width && selectedFile.height && (
                <div>
                  <p className="text-gray-500">Dimensions</p>
                  <p className="font-medium">{selectedFile.width} × {selectedFile.height}</p>
                </div>
              )}
              <div>
                <p className="text-gray-500">Uploaded</p>
                <p className="font-medium">{formatDate(selectedFile.created_at)}</p>
              </div>
              <div>
                <p className="text-gray-500">Usages</p>
                <p className="font-medium">{selectedFile.usage_count} place(s)</p>
              </div>
            </div>

            {/* URL */}
            <div>
              <p className="text-sm text-gray-500 mb-1">URL</p>
              <div className="flex items-center gap-2">
                <Input
                  value={selectedFile.url}
                  readOnly
                  className="text-xs font-mono"
                />
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => handleCopyUrl(selectedFile.url)}
                >
                  Copy
                </Button>
              </div>
            </div>

            {/* Usages */}
            {selectedFile.usages.length > 0 && (
              <div>
                <p className="text-sm text-gray-500 mb-2">Used In</p>
                <div className="space-y-2">
                  {selectedFile.usages.map((usage) => (
                    <div
                      key={usage.id}
                      className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2 text-sm"
                    >
                      <span>
                        <span className="font-medium capitalize">{usage.entity_type.replace('_', ' ')}</span>
                        <span className="text-gray-500"> #{usage.entity_id}</span>
                        <span className="text-gray-400 ml-2">({usage.field_name})</span>
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : null}
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, file: null })}
        onConfirm={handleDelete}
        title="Delete File"
        description={`Are you sure you want to delete "${deleteModal.file?.filename}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

