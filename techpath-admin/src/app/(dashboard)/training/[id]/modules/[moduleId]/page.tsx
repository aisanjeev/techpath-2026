'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowUp, ArrowDown, Plus, X, Library, ArrowLeft } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { FormField } from '@/components/ui/FormField';
import { PageLoader } from '@/components/ui/Spinner';
import { AssetPickerModal } from '@/components/training/AssetPickerModal';
import { assetMeta } from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import type { TrainingModuleDetail } from '@/types/training';

export default function ModuleDetailPage({
  params,
}: {
  params: Promise<{ id: string; moduleId: string }>;
}) {
  const { id, moduleId } = use(params);
  const programId = Number(id);
  const mid = Number(moduleId);
  const router = useRouter();

  const [module, setModule] = useState<TrainingModuleDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [pickerOpen, setPickerOpen] = useState(false);
  const [saving, setSaving] = useState(false);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [minutes, setMinutes] = useState('');
  const [status, setStatus] = useState('draft');

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await trainingService.getModule(mid);
      setModule(data);
      setTitle(data.title);
      setDescription(data.description ?? '');
      setMinutes(data.estimated_minutes ? String(data.estimated_minutes) : '');
      setStatus(data.status);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load module');
      router.push(`/training/${programId}`);
    } finally {
      setLoading(false);
    }
  }, [mid, programId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  const saveDetails = async () => {
    setSaving(true);
    try {
      await trainingService.updateModule(mid, {
        title: title.trim(),
        description: description.trim() || undefined,
        estimated_minutes: minutes ? Number(minutes) : undefined,
        status: status as never,
      });
      toast.success('Module saved');
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not save');
    } finally {
      setSaving(false);
    }
  };

  const move = async (index: number, direction: -1 | 1) => {
    if (!module) return;
    const assets = [...module.assets];
    const target = index + direction;
    if (target < 0 || target >= assets.length) return;

    [assets[index], assets[target]] = [assets[target], assets[index]];
    setModule({ ...module, assets });

    try {
      await trainingService.reorderModuleAssets(
        mid,
        assets.map((a, i) => ({ id: a.id, display_order: i + 1 }))
      );
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not reorder');
      void load();
    }
  };

  const attach = async (assetId: number) => {
    try {
      await trainingService.attachAsset(mid, { asset_id: assetId });
      toast.success('Asset added to this module');
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not add the asset');
    }
  };

  const detach = async (assetId: number) => {
    try {
      await trainingService.detachAsset(mid, assetId);
      toast.success('Asset removed from this module');
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not remove the asset');
    }
  };

  if (loading || !module) return <PageLoader />;

  return (
    <div>
      <Link
        href={`/training/${programId}`}
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to programme
      </Link>

      <PageHeader
        title={module.title}
        description={`${module.assets.length} asset${module.assets.length === 1 ? '' : 's'} in this lecture`}
        actions={
          <Button onClick={() => setPickerOpen(true)}>
            <Plus className="mr-1 h-4 w-4" />
            Add asset
          </Button>
        }
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {module.assets.length === 0 ? (
            <Card className="p-12 text-center">
              <Library className="mx-auto h-10 w-10 text-gray-300" />
              <p className="mt-3 text-sm font-medium text-gray-900">No assets yet</p>
              <p className="mx-auto mt-1 max-w-sm text-sm text-gray-500">
                Add existing assets from the shared library, or create a new one. The same
                asset can be used in as many modules as you like.
              </p>
              <div className="mt-4 flex justify-center gap-2">
                <Button onClick={() => setPickerOpen(true)}>
                  <Plus className="mr-1 h-4 w-4" />
                  Add from library
                </Button>
                <Link href="/training/assets/create">
                  <Button variant="outline">Create new asset</Button>
                </Link>
              </div>
            </Card>
          ) : (
            <div className="space-y-2">
              {module.assets.map((link, index) => {
                const meta = assetMeta(link.asset.asset_type);
                const Icon = meta.icon;
                return (
                  <Card key={link.id} className="flex items-center gap-3 p-4">
                    <div className="flex flex-col">
                      <button
                        onClick={() => move(index, -1)}
                        disabled={index === 0}
                        className="rounded p-0.5 text-gray-400 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-30 disabled:hover:bg-transparent"
                        aria-label="Move up"
                      >
                        <ArrowUp className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => move(index, 1)}
                        disabled={index === module.assets.length - 1}
                        className="rounded p-0.5 text-gray-400 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-30 disabled:hover:bg-transparent"
                        aria-label="Move down"
                      >
                        <ArrowDown className="h-4 w-4" />
                      </button>
                    </div>

                    <span className="w-5 text-sm font-semibold text-gray-400">{index + 1}</span>
                    <Icon className="h-5 w-5 shrink-0 text-gray-400" />

                    <Link
                      href={`/training/assets/${link.asset.id}`}
                      className="min-w-0 flex-1"
                    >
                      <p className="truncate font-medium text-gray-900 hover:text-teal-700">
                        {link.asset.title}
                      </p>
                      <p className="text-xs text-gray-500">{meta.label}</p>
                    </Link>

                    {link.asset.status !== 'published' && (
                      <Badge variant="warning">{link.asset.status}</Badge>
                    )}

                    <button
                      onClick={() => detach(link.asset_id)}
                      className="rounded p-1 text-gray-400 hover:bg-red-50 hover:text-red-600"
                      title="Remove from this module (the asset stays in the library)"
                      aria-label="Remove from module"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </Card>
                );
              })}
            </div>
          )}
        </div>

        <div>
          <Card className="p-6">
            <h2 className="mb-4 text-sm font-semibold text-gray-900">Module details</h2>
            <div className="space-y-4">
              <FormField label="Title">
                <Input value={title} onChange={(e) => setTitle(e.target.value)} />
              </FormField>
              <FormField label="Description">
                <Textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                />
              </FormField>
              <FormField label="Estimated minutes">
                <Input
                  type="number"
                  min={0}
                  value={minutes}
                  onChange={(e) => setMinutes(e.target.value)}
                />
              </FormField>
              <FormField label="Status">
                <Select value={status} onChange={(e) => setStatus(e.target.value)}>
                  <option value="draft">Draft</option>
                  <option value="published">Published</option>
                  <option value="archived">Archived</option>
                </Select>
              </FormField>
              <Button onClick={saveDetails} disabled={saving} className="w-full">
                {saving ? 'Saving…' : 'Save details'}
              </Button>
            </div>
          </Card>
        </div>
      </div>

      <AssetPickerModal
        isOpen={pickerOpen}
        onClose={() => setPickerOpen(false)}
        excludeIds={module.assets.map((a) => a.asset_id)}
        onSelect={(asset) => attach(asset.id)}
      />
    </div>
  );
}
