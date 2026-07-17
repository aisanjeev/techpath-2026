'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { Search, Plus } from 'lucide-react';
import toast from 'react-hot-toast';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Badge } from '@/components/ui/Badge';
import { Spinner } from '@/components/ui/Spinner';
import { ASSET_TYPE_META, assetMeta } from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import { cn } from '@/lib/utils/cn';
import type { AssetType, AssetTypeInfo, LectureAsset } from '@/types/training';

interface AssetPickerModalProps {
  isOpen: boolean;
  onClose: () => void;
  /** Assets already attached — shown but not selectable. */
  excludeIds?: number[];
  onSelect: (asset: LectureAsset) => void;
}

/**
 * Browse the shared asset library and place an existing asset into a module.
 *
 * This is what makes the library a library rather than a per-module upload box: the
 * default action for adding content is picking something that already exists.
 */
export function AssetPickerModal({
  isOpen,
  onClose,
  excludeIds = [],
  onSelect,
}: AssetPickerModalProps) {
  const [assets, setAssets] = useState<LectureAsset[]>([]);
  const [types, setTypes] = useState<AssetTypeInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<AssetType | ''>('');

  useEffect(() => {
    if (!isOpen) return;
    trainingService.assetTypes().then(setTypes).catch(() => undefined);
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    setLoading(true);
    // Debounce so typing doesn't fire a request per keystroke.
    const timer = setTimeout(() => {
      trainingService
        .listAssets({
          limit: 50,
          search: search || undefined,
          asset_type: typeFilter || undefined,
        })
        .then((result) => setAssets(result.items))
        .catch(() => toast.error('Could not load the asset library'))
        .finally(() => setLoading(false));
    }, 250);
    return () => clearTimeout(timer);
  }, [isOpen, search, typeFilter]);

  const excluded = useMemo(() => new Set(excludeIds), [excludeIds]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Add an asset" size="lg">
      <div className="space-y-4">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search the library…"
              className="pl-9"
            />
          </div>
          <Select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value as AssetType | '')}
            className="max-w-[190px]"
          >
            <option value="">All types</option>
            {types.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </Select>
        </div>

        <div className="max-h-[420px] space-y-2 overflow-y-auto">
          {loading ? (
            <div className="flex justify-center py-10">
              <Spinner size="lg" />
            </div>
          ) : assets.length === 0 ? (
            <div className="py-10 text-center">
              <p className="text-sm text-gray-500">
                {search || typeFilter
                  ? 'Nothing matches those filters.'
                  : 'The asset library is empty.'}
              </p>
              <Link href="/training/assets/create">
                <Button variant="outline" size="sm" className="mt-3">
                  <Plus className="mr-1 h-4 w-4" />
                  Create an asset
                </Button>
              </Link>
            </div>
          ) : (
            assets.map((asset) => {
              const meta = assetMeta(asset.asset_type);
              const Icon = meta.icon;
              const isAttached = excluded.has(asset.id);
              return (
                <button
                  key={asset.id}
                  type="button"
                  disabled={isAttached}
                  onClick={() => {
                    onSelect(asset);
                    onClose();
                  }}
                  className={cn(
                    'flex w-full items-center gap-3 rounded-lg border px-4 py-3 text-left transition-colors',
                    isAttached
                      ? 'cursor-not-allowed border-gray-100 bg-gray-50 opacity-60'
                      : 'border-gray-200 hover:border-teal-500 hover:bg-teal-50'
                  )}
                >
                  <Icon className="h-5 w-5 shrink-0 text-gray-400" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-gray-900">{asset.title}</p>
                    <p className="truncate text-xs text-gray-500">
                      {meta.label}
                      {asset.description ? ` · ${asset.description}` : ''}
                    </p>
                  </div>
                  {asset.status !== 'published' && (
                    <Badge variant={asset.status === 'draft' ? 'warning' : 'default'}>
                      {asset.status}
                    </Badge>
                  )}
                  {isAttached && <Badge variant="info">Added</Badge>}
                </button>
              );
            })
          )}
        </div>

        <p className="text-xs text-gray-500">
          Assets are shared. Adding one here places the same asset — editing it later
          updates every module that uses it.
        </p>
      </div>
    </Modal>
  );
}
