'use client';

import { useEffect, useState } from 'react';
import { BookOpen, X, ExternalLink } from 'lucide-react';
import { trainerService } from '@/services/trainer.service';
import type { TrainingModuleDetail, ModuleAssetLink } from '@/types/training';
import { Button } from '@/components/ui/Button';

interface SessionMaterialsModalProps {
  moduleId: number;
}

export function SessionMaterialsModal({ moduleId }: SessionMaterialsModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [moduleDetail, setModuleDetail] = useState<TrainingModuleDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && !moduleDetail) {
      setLoading(true);
      trainerService
        .getModule(moduleId)
        .then((detail) => setModuleDetail(detail))
        .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load materials'))
        .finally(() => setLoading(false));
    }
  }, [isOpen, moduleId, moduleDetail]);

  return (
    <>
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2"
        title="View Published Material"
      >
        <BookOpen className="h-4 w-4" />
        <span className="hidden sm:inline">Materials</span>
      </Button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl relative max-h-[90vh] flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-teal-600" />
                Session Materials
              </h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto">
              {loading ? (
                <div className="flex items-center justify-center p-8">
                  <div className="h-6 w-6 animate-spin rounded-full border-2 border-teal-600 border-t-transparent" />
                </div>
              ) : error ? (
                <p className="text-sm text-red-600 p-4">{error}</p>
              ) : !moduleDetail || moduleDetail.assets.length === 0 ? (
                <p className="text-sm text-gray-500 p-4 text-center">
                  No materials have been published for this module.
                </p>
              ) : (
                <ul className="space-y-3">
                  {moduleDetail.assets.map((link: ModuleAssetLink) => (
                    <li
                      key={link.id}
                      className="rounded-md border border-gray-100 p-3 shadow-sm hover:border-teal-100 transition-colors"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <p className="text-sm font-medium text-gray-900">{link.asset.title}</p>
                          <p className="text-xs text-gray-500 capitalize mt-1">
                            {link.asset.asset_type.replace('_', ' ')}
                            {link.is_required && ' • Required'}
                          </p>
                        </div>
                        {link.asset.external_url && (
                          <a
                            href={link.asset.external_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-teal-600 hover:text-teal-700 p-1"
                            title="Open material"
                          >
                            <ExternalLink className="h-4 w-4" />
                          </a>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            
            <div className="mt-6 flex justify-end">
              <Button onClick={() => setIsOpen(false)}>Close</Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
