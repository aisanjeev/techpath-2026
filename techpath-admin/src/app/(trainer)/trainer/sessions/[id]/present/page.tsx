'use client';

import { use, useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  ArrowLeft,
  ArrowRight,
  ChevronLeft,
  Copy,
  Check,
  Radio,
  Maximize,
  Minimize,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { trainerService } from '@/services/trainer.service';
import { assetMeta } from '@/components/training/asset-type-registry';
import { AssetRenderer } from '@/components/training/AssetRenderer';
import { ClassroomPanel } from '@/components/training/ClassroomPanel';
import { useClassroomSocket } from '@/hooks/useClassroomSocket';
import type { ModuleAssetLink, TrainingSession } from '@/types/training';

export default function PresenterPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const sessionId = Number(id);
  const router = useRouter();

  const [session, setSession] = useState<TrainingSession | null>(null);
  const [assets, setAssets] = useState<ModuleAssetLink[]>([]);
  const [current, setCurrent] = useState(0);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [headerVisible, setHeaderVisible] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const isLive = session?.status === 'live';
  const { connected, subscribe } = useClassroomSocket(sessionId, isLive);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const s = await trainerService.getSession(sessionId);
      setSession(s);

      if (s.module_id) {
        const detail = await trainerService.getModule(s.module_id);
        setAssets(detail.assets);
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load');
      router.push(`/trainer/sessions/${sessionId}`);
    } finally {
      setLoading(false);
    }
  }, [sessionId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  // The trainer is the source of truth for what students see — every slide change
  // broadcasts. Skipped while not live (nothing is listening) and on the very first
  // load (no point re-announcing whatever the session already had before a refresh).
  const hasBroadcastInitial = useRef(false);
  useEffect(() => {
    if (!isLive || assets.length === 0) return;
    if (!hasBroadcastInitial.current) {
      hasBroadcastInitial.current = true;
      return;
    }
    const assetId = assets[current]?.asset.id;
    if (assetId) {
      void trainerService.setSlide(sessionId, assetId).catch(() => {
        toast.error('Could not sync this slide to students');
      });
    }
  }, [current, assets, isLive, sessionId]);

  const toggleFullscreen = () => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      document.documentElement.requestFullscreen().catch(() => {});
    }
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      // These shortcuts double-book keys that also need to work normally while typing
      // (space, F, arrow keys) — without this guard, typing a space into the poll
      // question or the live-code editor advances the slide instead of inserting a
      // space, since keydown bubbles to window from any focused input, textarea, or
      // Monaco's own hidden textarea.
      const target = e.target as HTMLElement | null;
      const isEditable =
        target?.tagName === 'INPUT' ||
        target?.tagName === 'TEXTAREA' ||
        target?.tagName === 'SELECT' ||
        target?.isContentEditable;
      if (isEditable) return;

      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        setCurrent((c) => Math.min(c + 1, assets.length - 1));
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        setCurrent((c) => Math.max(c - 1, 0));
      } else if (e.key === 'Escape') {
        if (document.fullscreenElement) {
          document.exitFullscreen();
        } else {
          setHeaderVisible((v) => !v);
        }
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [assets.length]);

  useEffect(() => {
    const onChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onChange);
    return () => document.removeEventListener('fullscreenchange', onChange);
  }, []);

  const copyCode = async () => {
    if (!session?.join_code) return;
    await navigator.clipboard.writeText(session.join_code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-950">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-gray-600 border-t-teal-500" />
      </div>
    );
  }

  if (!session || assets.length === 0) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4 bg-gray-950 text-gray-400">
        <p className="text-lg">No content to present.</p>
        <button
          onClick={() => router.push(`/trainer/sessions/${sessionId}`)}
          className="text-teal-400 underline"
        >
          Back to session
        </button>
      </div>
    );
  }

  const asset = assets[current].asset;
  const meta = assetMeta(asset.asset_type);
  const Icon = meta.icon;
  const isFirst = current === 0;
  const isLast = current === assets.length - 1;

  return (
    <div className="flex h-screen bg-gray-950 text-white select-none">
      <div className="flex min-w-0 flex-1 flex-col">
        {/* Header */}
        <header
          className={`flex shrink-0 items-center justify-between border-b border-gray-800 bg-gray-950/90 px-4 py-2 backdrop-blur transition-all duration-300 ${
            headerVisible
              ? 'translate-y-0 opacity-100'
              : '-translate-y-full opacity-0 pointer-events-none absolute w-full z-50'
          }`}
        >
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push(`/trainer/sessions/${sessionId}`)}
              className="flex items-center gap-1 rounded-lg px-2 py-1 text-sm text-gray-400 transition hover:bg-gray-800 hover:text-white"
            >
              <ChevronLeft className="h-4 w-4" />
              Exit
            </button>
            <div className="h-4 w-px bg-gray-700" />
            <div className="text-sm">
              <span className="font-medium text-gray-200">
                {session.title || session.module_title}
              </span>
              {session.batch_name && (
                <span className="ml-2 text-gray-500">· {session.batch_name}</span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3">
            {isLive && session.join_code && (
              <button
                onClick={copyCode}
                className="flex items-center gap-2 rounded-lg border border-teal-700 bg-teal-900/30 px-3 py-1 text-sm transition hover:bg-teal-900/50"
              >
                <Radio className="h-3 w-3 text-teal-400 animate-pulse" />
                <span className="font-mono font-bold tracking-wider text-teal-300">
                  {session.join_code}
                </span>
                {copied ? (
                  <Check className="h-3.5 w-3.5 text-green-400" />
                ) : (
                  <Copy className="h-3.5 w-3.5 text-gray-400" />
                )}
              </button>
            )}
            <button
              onClick={toggleFullscreen}
              className="rounded-lg p-1.5 text-gray-400 transition hover:bg-gray-800 hover:text-white"
              title={isFullscreen ? 'Exit fullscreen (F)' : 'Fullscreen (F)'}
            >
              {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
            </button>
          </div>
        </header>

        {/* Slide area */}
        <main
          className="relative flex flex-1 flex-col overflow-auto"
          onClick={() => setHeaderVisible((v) => !v)}
        >
          {/* Asset title bar */}
          <div className="sticky top-0 z-10 flex shrink-0 items-center gap-3 bg-gray-950/80 px-8 py-3 backdrop-blur">
            <Icon className="h-5 w-5 shrink-0 text-teal-500" />
            <h1 className="text-xl font-semibold text-white">{asset.title}</h1>
            <span className="text-sm text-gray-500">{meta.label}</span>
          </div>

          {/* main is now the flex context that lets file-embed slide types (ppt, pdf,
              video) actually claim remaining height via flex-1 — before this, main was
              plain block layout, so flex-1 on children below it was a no-op and those
              embeds silently sized to a tiny content-driven height instead of filling
              the available area. Long text content (markdown, quiz) still scrolls via
              main's own overflow-auto exactly as before. */}
          <AssetRenderer asset={asset} className="min-h-0 flex-1" />
        </main>

        {/* Navigation footer */}
        <footer className="flex shrink-0 items-center justify-between border-t border-gray-800 bg-gray-950/90 px-4 py-2 backdrop-blur">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setCurrent((c) => Math.max(c - 1, 0));
            }}
            disabled={isFirst}
            className="flex items-center gap-1 rounded-lg px-3 py-2 text-sm transition
            enabled:hover:bg-gray-800 enabled:text-gray-300 disabled:text-gray-700"
          >
            <ArrowLeft className="h-4 w-4" />
            Previous
          </button>

          {/* Progress */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-1">
              {assets.map((_, i) => (
                <button
                  key={i}
                  onClick={(e) => {
                    e.stopPropagation();
                    setCurrent(i);
                  }}
                  className={`h-1.5 rounded-full transition-all ${
                    i === current
                      ? 'w-6 bg-teal-500'
                      : i < current
                        ? 'w-1.5 bg-teal-700'
                        : 'w-1.5 bg-gray-700'
                  }`}
                  aria-label={`Go to slide ${i + 1}`}
                />
              ))}
            </div>
            <span className="text-xs tabular-nums text-gray-500">
              {current + 1} / {assets.length}
            </span>
          </div>

          <button
            onClick={(e) => {
              e.stopPropagation();
              setCurrent((c) => Math.min(c + 1, assets.length - 1));
            }}
            disabled={isLast}
            className="flex items-center gap-1 rounded-lg px-3 py-2 text-sm transition
            enabled:hover:bg-gray-800 enabled:text-gray-300 disabled:text-gray-700"
          >
            Next
            <ArrowRight className="h-4 w-4" />
          </button>
        </footer>
      </div>

      {isLive && (
        <ClassroomPanel
          sessionId={sessionId}
          connected={connected}
          subscribe={subscribe}
          assets={assets}
        />
      )}
    </div>
  );
}
