'use client';

import { Fragment } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils/cn';
import { Button } from './Button';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl',
  '2xl': 'max-w-4xl',
};

export function Modal({ isOpen, onClose, title, description, children, size = 'md' }: ModalProps) {
  if (!isOpen) return null;

  return (
    <Fragment>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className={cn(
            'relative w-full rounded-xl bg-white shadow-xl',
            sizeClasses[size]
          )}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          {(title || description) && (
            <div className="border-b border-gray-200 px-6 py-4">
              {title && (
                <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
              )}
              {description && (
                <p className="mt-1 text-sm text-gray-500">{description}</p>
              )}
            </div>
          )}

          {/* Close button */}
          <Button
            variant="ghost"
            size="icon"
            className="absolute right-4 top-4"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </Button>

          {/* Content */}
          <div className="p-6">{children}</div>
        </div>
      </div>
    </Fragment>
  );
}

export interface ConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  description: string;
  confirmText?: string;
  cancelText?: string;
  variant?: 'danger' | 'warning' | 'info';
  loading?: boolean;
  disabled?: boolean;
}

export function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'danger',
  loading,
  disabled,
}: ConfirmModalProps) {
  const buttonVariant = variant === 'danger' ? 'destructive' : 'default';

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title} size="sm">
      <p className="text-sm text-gray-600">{description}</p>
      <div className="mt-6 flex justify-end gap-3">
        <Button variant="outline" onClick={onClose} disabled={loading}>
          {cancelText}
        </Button>
        <Button variant={buttonVariant} onClick={onConfirm} loading={loading} disabled={disabled || loading}>
          {confirmText}
        </Button>
      </div>
    </Modal>
  );
}

