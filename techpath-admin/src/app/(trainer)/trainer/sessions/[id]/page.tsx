'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowLeft,
  Play,
  Square,
  Radio,
  Copy,
  Check,
  Clock,
  Presentation,
  FileBarChart,
  Share2,
  ShieldOff,
  Eye,
  EyeOff,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { FormField } from '@/components/ui/FormField';
import { PageLoader } from '@/components/ui/Spinner';
import { trainerService } from '@/services/trainer.service';
import { assetMeta } from '@/components/training/asset-type-registry';
import type {
  AssetReleaseItem,
  ModuleAssetLink,
  SessionMaterialsStatus,
  TrainingModule,
  TrainingSession,
} from '@/types/training';

function elapsed(since: string): string {
  const secs = Math.floor((Date.now() - new Date(since).getTime()) / 1000);
  const mins = Math.floor(secs / 60);
  const hrs = Math.floor(mins / 60);
  return hrs > 0 ? `${hrs}h ${mins % 60}m` : `${mins}m ${secs % 60}s`;
}

export default function TrainerSessionPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const sessionId = Number(id);
  const router = useRouter();

  const [session, setSession] = useState<TrainingSession | null>(null);
  const [modules, setModules] = useState<TrainingModule[]>([]);
  const [assets, setAssets] = useState<ModuleAssetLink[]>([]);
  const [selectedModule, setSelectedModule] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [publishBusy, setPublishBusy] = useState(false);
  const [materialsStatus, setMaterialsStatus] = useState<SessionMaterialsStatus | null>(null);
  const [assetBusy, setAssetBusy] = useState<Record<number, boolean>>({});
  const [copied, setCopied] = useState(false);
  const [, setTick] = useState(0);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const s = await trainerService.getSession(sessionId);
      setSession(s);
      setSelectedModule(s.module_id != null ? String(s.module_id) : '');

      const mods = await trainerService.getBatchModules(s.batch_id);
      setModules(mods);

      if (s.module_id) {
        const detail = await trainerService.getModule(s.module_id);
        setAssets(detail.assets);
      }

      if (s.status === 'ended') {
        try {
          const status = await trainerService.getMaterialsStatus(sessionId);
          setMaterialsStatus(status);
        } catch {
          // Non-fatal — eye buttons will use isReleased=false as default
        }
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load the session');
      router.push('/trainer');
    } finally {
      setLoading(false);
    }
  }, [sessionId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  // Keep the elapsed clock moving while live.
  useEffect(() => {
    if (session?.status !== 'live') return;
    const timer = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(timer);
  }, [session?.status]);

  const start = async () => {
    if (!selectedModule) {
      toast.error('Choose a module to present');
      return;
    }
    setBusy(true);
    try {
      const live = await trainerService.startSession(sessionId, Number(selectedModule));
      setSession(live);
      const detail = await trainerService.getModule(Number(selectedModule));
      setAssets(detail.assets);
      toast.success('You are live');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not start');
    } finally {
      setBusy(false);
    }
  };

  const end = async () => {
    setBusy(true);
    try {
      setSession(await trainerService.endSession(sessionId));
      toast.success('Session ended');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not end the session');
    } finally {
      setBusy(false);
    }
  };

  const releaseAll = async () => {
    setPublishBusy(true);
    try {
      const updated = await trainerService.publishMaterials(sessionId);
      setSession(updated);
      const status = await trainerService.getMaterialsStatus(sessionId);
      setMaterialsStatus(status);
      toast.success('All materials released to students');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not release materials');
    } finally {
      setPublishBusy(false);
    }
  };

  const revokeAll = async () => {
    setPublishBusy(true);
    try {
      const updated = await trainerService.unpublishMaterials(sessionId);
      setSession(updated);
      const status = await trainerService.getMaterialsStatus(sessionId);
      setMaterialsStatus(status);
      toast.success('All materials revoked');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not revoke materials');
    } finally {
      setPublishBusy(false);
    }
  };

  const toggleAssetRelease = async (item: AssetReleaseItem) => {
    setAssetBusy((prev) => ({ ...prev, [item.asset_id]: true }));
    try {
      const status = item.is_released
        ? await trainerService.unreleaseAsset(sessionId, item.asset_id)
        : await trainerService.releaseAsset(sessionId, item.asset_id);
      setMaterialsStatus(status);
      // Keep session materials_published_at in sync with the response
      const anyReleased = status.assets.some((a) => a.is_released);
      setSession((prev) =>
        prev
          ? {
              ...prev,
              materials_published_at: anyReleased
                ? (prev.materials_published_at ?? new Date().toISOString())
                : null,
            }
          : prev
      );
      toast.success(
        item.is_released
          ? `"${item.asset_title}" hidden from students`
          : `"${item.asset_title}" released to students`
      );
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not update asset release');
    } finally {
      setAssetBusy((prev) => ({ ...prev, [item.asset_id]: false }));
    }
  };

  const copyCode = async () => {
    if (!session?.join_code) return;
    await navigator.clipboard.writeText(session.join_code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading || !session) return <PageLoader />;

  const isLive = session.status === 'live';
  const isEnded = session.status === 'ended';
  const releaseMap = new Map(
    (materialsStatus?.assets ?? []).map((a) => [a.asset_id, a])
  );
  const releasedCount = (materialsStatus?.assets ?? []).filter((a) => a.is_released).length;
  const totalCount = materialsStatus?.assets.length ?? 0;

  function accessSummary(): string {
    if (releasedCount === 0) return 'No materials released yet. Toggle individual assets in the content list, or use the buttons below.';
    if (releasedCount === totalCount) return 'All materials are visible to students in their portal.';
    return `${releasedCount} of ${totalCount} materials visible to students.`;
  }

  const releaseAllLabel = publishBusy ? 'Releasing...' : 'Release all';
  const revokeAllLabel = publishBusy ? 'Revoking...' : 'Revoke all';

  return (
    <div>
      <Link
        href={`/trainer/batches/${session.batch_id}`}
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to batch
      </Link>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {session.title || session.module_title || 'Session'}
          </h1>
          <p className="mt-1 text-sm text-gray-500">{session.batch_name}</p>
        </div>
        <div className="flex items-center gap-3">
          {isLive && session.started_at && (
            <span className="flex items-center gap-1 text-sm text-gray-500">
              <Clock className="h-4 w-4" />
              {elapsed(session.started_at)}
            </span>
          )}
          <Badge variant={isLive ? 'success' : session.status === 'ended' ? 'default' : 'info'}>
            {isLive && <Radio className="mr-1 inline h-3 w-3" />}
            {session.status}
          </Badge>
        </div>
      </div>

      {isLive && session.join_code && (
        <Card className="mb-6 border-teal-500 bg-teal-50 p-6 text-center">
          <p className="text-xs uppercase tracking-wide text-teal-700">
            Students join with this code
          </p>
          <div className="mt-2 flex items-center justify-center gap-3">
            <span className="font-mono text-4xl font-bold tracking-[0.3em] text-teal-800">
              {session.join_code}
            </span>
            <Button variant="ghost" size="icon" onClick={copyCode} aria-label="Copy join code">
              {copied ? (
                <Check className="h-4 w-4 text-teal-600" />
              ) : (
                <Copy className="h-4 w-4 text-teal-600" />
              )}
            </Button>
          </div>
        </Card>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-gray-900">
                Lecture content ({assets.length})
              </h2>
              {isEnded && totalCount > 0 && (
                <span className="text-xs text-gray-500">
                  {releasedCount}/{totalCount} released to students
                </span>
              )}
            </div>
            {assets.length === 0 ? (
              <p className="text-sm text-gray-500">
                {selectedModule
                  ? 'This module has no assets yet.'
                  : 'Choose a module to see its content.'}
              </p>
            ) : (
              <ol className="space-y-2">
                {assets.map((link, i) => {
                  const meta = assetMeta(link.asset.asset_type);
                  const Icon = meta.icon;
                  const releaseItem = releaseMap.get(link.asset_id);
                  const isReleased = releaseItem?.is_released ?? false;
                  const isBusy = assetBusy[link.asset_id] ?? false;
                  return (
                    <li
                      key={link.id}
                      className={`flex items-center gap-3 rounded-lg border p-3 transition-colors ${
                        isEnded
                          ? isReleased
                            ? 'border-teal-200 bg-teal-50'
                            : 'border-gray-200 bg-white'
                          : 'border-gray-200'
                      }`}
                    >
                      <span className="w-5 shrink-0 text-sm font-semibold text-gray-400">
                        {i + 1}
                      </span>
                      <Icon className="h-4 w-4 shrink-0 text-gray-400" />
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium text-gray-900">
                          {link.asset.title}
                        </p>
                        <p className="text-xs text-gray-500">{meta.label}</p>
                      </div>
                      {!link.is_required && <Badge variant="default">Optional</Badge>}
                      {isEnded && (
                        <button
                          onClick={() =>
                            toggleAssetRelease(
                              releaseItem ?? {
                                asset_id: link.asset_id,
                                asset_title: link.asset.title,
                                asset_type: link.asset.asset_type,
                                is_released: false,
                                display_order: link.display_order,
                              }
                            )
                          }
                          disabled={isBusy}
                          title={isReleased ? 'Hide from students' : 'Release to students'}
                          className={`shrink-0 rounded p-1 transition-colors ${
                            isBusy
                              ? 'opacity-50 cursor-not-allowed'
                              : isReleased
                              ? 'text-teal-600 hover:text-teal-800 hover:bg-teal-100'
                              : 'text-gray-400 hover:text-gray-700 hover:bg-gray-100'
                          }`}
                        >
                          {isReleased ? (
                            <Eye className="h-4 w-4" />
                          ) : (
                            <EyeOff className="h-4 w-4" />
                          )}
                        </button>
                      )}
                    </li>
                  );
                })}
              </ol>
            )}
          </Card>
        </div>

        <div className="space-y-4">
          <Card className="p-6">
            <h2 className="mb-4 text-sm font-semibold text-gray-900">Presenting</h2>

            <FormField label="Module">
              <Select
                value={selectedModule}
                onChange={async (e) => {
                  setSelectedModule(e.target.value);
                  if (e.target.value) {
                    const detail = await trainerService.getModule(Number(e.target.value));
                    setAssets(detail.assets);
                  } else {
                    setAssets([]);
                  }
                }}
                disabled={isLive}
              >
                <option value="">Choose a module…</option>
                {modules.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.title} ({m.asset_count})
                  </option>
                ))}
              </Select>
            </FormField>

            <div className="mt-4 space-y-2">
              {isEnded ? (
                <>
                  <p className="text-sm text-gray-500">This session has ended.</p>

                  <div className="rounded-lg border border-gray-200 bg-gray-50 p-3">
                    <p className="text-xs font-medium text-gray-700">Student access</p>
                    <p className="mt-0.5 text-xs text-gray-500">{accessSummary()}</p>
                    <div className="mt-2 flex gap-2">
                      <Button
                        variant="default"
                        onClick={releaseAll}
                        disabled={publishBusy || releasedCount === totalCount}
                        className="flex-1"
                        size="sm"
                      >
                        <Share2 className="mr-1 h-3 w-3" />
                        {releaseAllLabel}
                      </Button>
                      <Button
                        variant="outline"
                        onClick={revokeAll}
                        disabled={publishBusy || releasedCount === 0}
                        className="flex-1"
                        size="sm"
                      >
                        <ShieldOff className="mr-1 h-3 w-3" />
                        {revokeAllLabel}
                      </Button>
                    </div>
                  </div>

                  <Button
                    variant="outline"
                    onClick={() => router.push(`/trainer/sessions/${sessionId}/report`)}
                    className="w-full"
                  >
                    <FileBarChart className="mr-1 h-4 w-4" />
                    View report
                  </Button>
                </>
              ) : isLive ? (
                <>
                  <Button
                    onClick={() => router.push(`/trainer/sessions/${sessionId}/present`)}
                    className="w-full"
                  >
                    <Presentation className="mr-1 h-4 w-4" />
                    Open Presenter
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => router.push(`/trainer/sessions/${sessionId}/report`)}
                    className="w-full"
                  >
                    <FileBarChart className="mr-1 h-4 w-4" />
                    View report
                  </Button>
                  <Button
                    variant="destructive"
                    onClick={end}
                    disabled={busy}
                    className="w-full"
                  >
                    <Square className="mr-1 h-4 w-4" />
                    {busy ? 'Ending…' : 'End session'}
                  </Button>
                </>
              ) : (
                <Button
                  onClick={start}
                  disabled={busy || !selectedModule}
                  className="w-full"
                >
                  <Play className="mr-1 h-4 w-4" />
                  {busy ? 'Starting…' : 'Start presenting'}
                </Button>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
