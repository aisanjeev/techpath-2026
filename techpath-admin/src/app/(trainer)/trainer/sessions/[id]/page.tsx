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
  ModuleAssetLink,
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

  const togglePublish = async () => {
    setPublishBusy(true);
    try {
      const updated = session?.materials_published_at
        ? await trainerService.unpublishMaterials(sessionId)
        : await trainerService.publishMaterials(sessionId);
      setSession(updated);
      toast.success(
        updated.materials_published_at
          ? 'Materials published — attendees can now see them in their portal'
          : 'Materials unpublished'
      );
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not update publish status');
    } finally {
      setPublishBusy(false);
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
            <h2 className="mb-4 text-sm font-semibold text-gray-900">
              Lecture content ({assets.length})
            </h2>
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
                  return (
                    <li
                      key={link.id}
                      className="flex items-center gap-3 rounded-lg border border-gray-200 p-3"
                    >
                      <span className="w-5 text-sm font-semibold text-gray-400">{i + 1}</span>
                      <Icon className="h-4 w-4 shrink-0 text-gray-400" />
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium text-gray-900">
                          {link.asset.title}
                        </p>
                        <p className="text-xs text-gray-500">{meta.label}</p>
                      </div>
                      {!link.is_required && <Badge variant="default">Optional</Badge>}
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
              {session.status === 'ended' ? (
                <>
                  <p className="text-sm text-gray-500">This session has ended.</p>

                  <div className="rounded-lg border border-gray-200 bg-gray-50 p-3">
                    <p className="text-xs font-medium text-gray-700">
                      {session.materials_published_at
                        ? 'Materials are published'
                        : 'Materials not shared yet'}
                    </p>
                    <p className="mt-0.5 text-xs text-gray-500">
                      {session.materials_published_at
                        ? 'Attendees can sign in to their student portal to view and download this session’s content.'
                        : 'Publish to let every student who attended view and download this session’s content later.'}
                    </p>
                    <Button
                      variant={session.materials_published_at ? 'outline' : 'default'}
                      onClick={togglePublish}
                      disabled={publishBusy}
                      className="mt-2 w-full"
                      size="sm"
                    >
                      {session.materials_published_at ? (
                        <>
                          <ShieldOff className="mr-1 h-4 w-4" />
                          {publishBusy ? 'Unpublishing…' : 'Unpublish materials'}
                        </>
                      ) : (
                        <>
                          <Share2 className="mr-1 h-4 w-4" />
                          {publishBusy ? 'Publishing…' : 'Publish materials to students'}
                        </>
                      )}
                    </Button>
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
