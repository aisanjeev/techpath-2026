'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChevronRight, Plus, Search, X } from 'lucide-react';
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
import type {
  AssetType,
  AssetTypeInfo,
  ContentStatus,
  LectureAsset,
  TrainingModule,
  TrainingProgram,
} from '@/types/training';

type ProgramUsage = { program_id: number; program_title: string };
type ProgramMap = Record<string, ProgramUsage[]>;

/* ------------------------------------------------------------------ */
/*  Inline assign-to-program popover                                  */
/* ------------------------------------------------------------------ */

function AssignPopover({
  assetId,
  programs,
  onAttached,
  onClose,
}: {
  assetId: number;
  programs: TrainingProgram[];
  onAttached: () => void;
  onClose: () => void;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [selectedProgram, setSelectedProgram] = useState<TrainingProgram | null>(null);
  const [modules, setModules] = useState<TrainingModule[]>([]);
  const [loadingModules, setLoadingModules] = useState(false);
  const [attaching, setAttaching] = useState(false);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClose]);

  const pickProgram = async (p: TrainingProgram) => {
    setSelectedProgram(p);
    setLoadingModules(true);
    try {
      setModules(await trainingService.listModules(p.id));
    } catch {
      toast.error('Could not load modules');
    } finally {
      setLoadingModules(false);
    }
  };

  const attach = async (moduleId: number) => {
    setAttaching(true);
    try {
      await trainingService.attachAsset(moduleId, { asset_id: assetId });
      toast.success('Asset attached');
      onAttached();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not attach');
    } finally {
      setAttaching(false);
    }
  };

  return (
    <div
      ref={ref}
      className="absolute right-0 top-full z-50 mt-1 w-64 rounded-lg border border-gray-200 bg-white shadow-lg"
    >
      <div className="flex items-center justify-between border-b px-3 py-2">
        <span className="text-xs font-semibold text-gray-700">
          {selectedProgram ? selectedProgram.title : 'Select program'}
        </span>
        {selectedProgram ? (
          <button onClick={() => setSelectedProgram(null)} className="text-gray-400 hover:text-gray-600">
            <ChevronRight className="h-3 w-3 rotate-180" />
          </button>
        ) : (
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="h-3 w-3" />
          </button>
        )}
      </div>

      <div className="max-h-48 overflow-y-auto p-1">
        {!selectedProgram ? (
          programs.map((p) => (
            <button
              key={p.id}
              onClick={() => pickProgram(p)}
              className="flex w-full items-center justify-between rounded px-3 py-1.5 text-left text-sm text-gray-700 hover:bg-gray-50"
            >
              <span className="truncate">{p.title}</span>
              <ChevronRight className="h-3 w-3 shrink-0 text-gray-400" />
            </button>
          ))
        ) : loadingModules ? (
          <p className="px-3 py-2 text-xs text-gray-400">Loading modules…</p>
        ) : modules.length === 0 ? (
          <p className="px-3 py-2 text-xs text-gray-400">No modules in this program</p>
        ) : (
          modules.map((m) => (
            <button
              key={m.id}
              disabled={attaching}
              onClick={() => attach(m.id)}
              className="flex w-full items-center rounded px-3 py-1.5 text-left text-sm text-gray-700 hover:bg-blue-50 disabled:opacity-50"
            >
              <span className="truncate">{m.title}</span>
            </button>
          ))
        )}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main page                                                         */
/* ------------------------------------------------------------------ */

export default function AssetLibraryPage() {
  const router = useRouter();
  const [assets, setAssets] = useState<LectureAsset[]>([]);
  const [types, setTypes] = useState<AssetTypeInfo[]>([]);
  const [programs, setPrograms] = useState<TrainingProgram[]>([]);
  const [programMap, setProgramMap] = useState<ProgramMap>({});
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<AssetType | ''>('');
  const [statusFilter, setStatusFilter] = useState<ContentStatus | ''>('');
  const [programFilter, setProgramFilter] = useState<number | ''>('');
  const [deleting, setDeleting] = useState<LectureAsset | null>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);
  const [assigningAssetId, setAssigningAssetId] = useState<number | null>(null);

  const limit = 20;

  useEffect(() => {
    trainingService.assetTypes().then(setTypes).catch(() => undefined);
    trainingService
      .listPrograms({ limit: 100 })
      .then((r) => setPrograms(r.items))
      .catch(() => undefined);
  }, []);

  const loadProgramMap = useCallback(async (ids: number[]) => {
    if (!ids.length) { setProgramMap({}); return; }
    trainingService.bulkAssetPrograms(ids).then(setProgramMap).catch(() => undefined);
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await trainingService.listAssets({
        skip: (page - 1) * limit,
        limit,
        search: search || undefined,
        asset_type: typeFilter || undefined,
        status: statusFilter || undefined,
        program_id: programFilter || undefined,
      });
      setAssets(result.items);
      setTotal(result.total);
      loadProgramMap(result.items.map((a) => a.id));
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load assets');
    } finally {
      setLoading(false);
    }
  }, [page, search, typeFilter, statusFilter, programFilter, loadProgramMap]);

  useEffect(() => {
    const timer = setTimeout(load, search ? 250 : 0);
    return () => clearTimeout(timer);
  }, [load, search]);

  const handleStatusChange = async (asset: LectureAsset, newStatus: string) => {
    try {
      await trainingService.updateAsset(asset.id, { status: newStatus });
      setAssets((prev) => prev.map((a) => (a.id === asset.id ? { ...a, status: newStatus as ContentStatus } : a)));
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not update status');
    }
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteBusy(true);
    try {
      await trainingService.deleteAsset(deleting.id);
      toast.success('Asset deleted');
      setDeleting(null);
      void load();
    } catch (err) {
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
      key: 'programs',
      header: 'Used in',
      render: (a) => {
        const usages = programMap[String(a.id)] || [];
        return (
          <div className="relative flex flex-wrap items-center gap-1">
            {usages.length > 0 ? (
              <>
                {usages.slice(0, 2).map((u) => (
                  <Badge
                    key={u.program_id}
                    variant="info"
                    className="cursor-pointer"
                    onClick={(e) => {
                      e.stopPropagation();
                      router.push(`/training/${u.program_id}`);
                    }}
                  >
                    {u.program_title}
                  </Badge>
                ))}
                {usages.length > 2 && (
                  <span className="text-xs text-gray-400">+{usages.length - 2}</span>
                )}
              </>
            ) : (
              <span className="text-xs text-gray-400">Not used</span>
            )}
            <button
              onClick={(e) => {
                e.stopPropagation();
                setAssigningAssetId(assigningAssetId === a.id ? null : a.id);
              }}
              className="inline-flex h-5 w-5 items-center justify-center rounded-full border border-dashed border-gray-300 text-gray-400 hover:border-blue-400 hover:text-blue-500"
              title="Assign to a module"
            >
              <Plus className="h-3 w-3" />
            </button>
            {assigningAssetId === a.id && (
              <AssignPopover
                assetId={a.id}
                programs={programs}
                onAttached={() => {
                  setAssigningAssetId(null);
                  loadProgramMap(assets.map((x) => x.id));
                }}
                onClose={() => setAssigningAssetId(null)}
              />
            )}
          </div>
        );
      },
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
        <select
          value={a.status}
          onClick={(e) => e.stopPropagation()}
          onChange={(e) => handleStatusChange(a, e.target.value)}
          className={`cursor-pointer rounded-full border-0 px-2.5 py-0.5 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-blue-300 ${
            a.status === 'published'
              ? 'bg-green-100 text-green-800'
              : a.status === 'draft'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-gray-100 text-gray-800'
          }`}
        >
          <option value="draft">Draft</option>
          <option value="published">Published</option>
          <option value="archived">Archived</option>
        </select>
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
          value={programFilter}
          onChange={(e) => {
            setProgramFilter(e.target.value ? Number(e.target.value) : '');
            setPage(1);
          }}
          className="max-w-[200px]"
        >
          <option value="">All programs</option>
          {programs.map((p) => (
            <option key={p.id} value={p.id}>
              {p.title}
            </option>
          ))}
        </Select>
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
          value={statusFilter}
          onChange={(e) => {
            setStatusFilter(e.target.value as ContentStatus | '');
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
