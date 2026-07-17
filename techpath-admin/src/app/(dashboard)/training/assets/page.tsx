'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { DataTable, type Column } from '@/components/tables/DataTable';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { ConfirmModal } from '@/components/ui/Modal';
import { assetMeta } from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import type { AssetType, AssetTypeInfo, ContentStatus, LectureAsset } from '@/types/training';

export default function AssetLibraryPage() {
  const router = useRouter();
  const [assets, setAssets] = useState<LectureAsset[]>([]);
  const [types, setTypes] = useState<AssetTypeInfo[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<AssetType | ''>('');
  const [status, setStatus] = useState<ContentStatus | ''>('');
  const [deleting, setDeleting] = useState<LectureAsset | null>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);

  const limit = 20;

  useEffect(() => {
    trainingService.assetTypes().then(setTypes).catch(() => undefined);
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await trainingService.listAssets({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        asset_type: typeFilter || undefined,
        status: status || undefined,
      });
      setAssets(result.items);
      setTotal(result.total);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load assets');
    } finally {
      setLoading(false);
    }
  }, [page, search, typeFilter, status]);

  useEffect(() => {
    const timer = setTimeout(load, search ? 250 : 0);
    return () => clearTimeout(timer);
  }, [load, search]);

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteBusy(true);
    try {
      await trainingService.deleteAsset(deleting.id);
      toast.success('Asset deleted');
      setDeleting(null);
      void load();
    } catch (err) {
      // The API refuses to delete an asset that modules still teach from, and says
      // how many. Surfacing that verbatim is more useful than a generic failure.
      toast.error(err instanceof Error ? err.message : 'Could not delete');
    } finally {
      setDeleteBusy(false);
    }
  };

  const columns: Column<LectureAsset>[] = [
    {
      key: 'title',
      header: 'Asset',
      render: (a) => {
        const meta = assetMeta(a.asset_type);
        const Icon = meta.icon;
        return (
          <div className="flex items-center gap-3">
            <Icon className="h-4 w-4 shrink-0 text-gray-400" />
            <div className="min-w-0">
              <p className="truncate font-medium text-gray-900">{a.title}</p>
              {a.description && (
                <p className="truncate text-xs text-gray-500">{a.description}</p>
              )}
            </div>
          </div>
        );
      },
    },
    {
      key: 'asset_type',
      header: 'Type',
      render: (a) => <span className="text-gray-600">{assetMeta(a.asset_type).label}</span>,
    },
    {
      key: 'tags',
      header: 'Tags',
      render: (a) =>
        a.tags.length ? (
          <div className="flex flex-wrap gap-1">
            {a.tags.slice(0, 3).map((t) => (
              <Badge key={t} variant="default">
                {t}
              </Badge>
            ))}
            {a.tags.length > 3 && (
              <span className="text-xs text-gray-400">+{a.tags.length - 3}</span>
            )}
          </div>
        ) : (
          <span className="text-xs text-gray-400">—</span>
        ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (a) => (
        <Badge variant={a.status === 'published' ? 'success' : a.status === 'draft' ? 'warning' : 'default'}>
          {a.status}
        </Badge>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Asset Library"
        description="Reusable lecture blocks. One asset can appear in any number of modules."
        actions={
          <Button onClick={() => router.push('/training/assets/create')}>
            <Plus className="mr-1 h-4 w-4" />
            New asset
          </Button>
        }
      />

      <div className="mb-4 flex flex-wrap gap-2">
        <div className="relative min-w-[220px] flex-1 max-w-sm">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search assets…"
            className="pl-9"
          />
        </div>
        <Select
          value={typeFilter}
          onChange={(e) => {
            setTypeFilter(e.target.value as AssetType | '');
            setPage(1);
          }}
          className="max-w-[190px]"
        >
          <option value="">All types</option>
          {types.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </Select>
        <Select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value as ContentStatus | '');
            setPage(1);
          }}
          className="max-w-[170px]"
        >
          <option value="">All statuses</option>
          <option value="draft">Draft</option>
          <option value="published">Published</option>
          <option value="archived">Archived</option>
        </Select>
      </div>

      <DataTable
        columns={columns}
        data={assets}
        loading={loading}
        keyExtractor={(a) => a.id}
        onEdit={(a) => router.push(`/training/assets/${a.id}`)}
        onDelete={(a) => setDeleting(a)}
        pagination={{ page, limit, total, onPageChange: setPage }}
        emptyMessage="No assets yet. Create markdown, PDFs, videos, quizzes and more."
      />

      <ConfirmModal
        isOpen={!!deleting}
        onClose={() => setDeleting(null)}
        onConfirm={handleDelete}
        title="Delete this asset?"
        description={`"${deleting?.title}" will be permanently deleted. If any module still uses it, the delete will be refused — detach it first, or archive it instead.`}
        confirmText="Delete"
        loading={deleteBusy}
      />
    </div>
  );
}
