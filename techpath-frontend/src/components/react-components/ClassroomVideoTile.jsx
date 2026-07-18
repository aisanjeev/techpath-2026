import { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';

const ICE_SERVERS = [{ urls: 'stun:stun.l.google.com:19302' }];
const RETRY_DELAY_MS = 3000;
// After this many consecutive *signaling* failures (WHEP POST 404/error — "no stream
// at this path yet"), switch the displayed copy from "connecting" to a friendlier
// "still waiting" message. Retrying itself never stops while whepUrl is present — a
// 404 here means the trainer hasn't published yet, which can legitimately take a while
// (they still need to grant camera/mic permission), not that anything is broken.
const SIGNALING_FAILURES_BEFORE_WAITING_COPY = 3;
// After this many consecutive *ICE/transport* failures following a successful WHEP
// handshake (a real 201 + SDP answer, but the peer connection itself never connects),
// switch to the HLS fallback — this is the actual "network blocks WebRTC/UDP" signal
// (spec.md FR-012/SC-006). A signaling 404 never counts toward this: HLS would fail for
// the exact same reason WHEP did (no stream exists yet), so it isn't a useful fallback
// for that case.
const ICE_FAILURES_BEFORE_HLS = 2;

/**
 * Student-side live video viewer, ported from CLASSROOM-WEBAPP-GUIDE.md. Connects
 * directly to the self-hosted media server — this app's backend never sees the
 * audio/video bytes, only ever hands out URLs (see classroomService.getState()).
 *
 * Two distinct failure modes drive two different responses:
 * 1. Signaling failure (WHEP POST never gets a 2xx — no publisher at this path yet).
 *    The backend hands out whep_url the instant a session goes live, which is *before*
 *    the trainer's browser finishes its own getUserMedia -> WHIP handshake, so this is
 *    an expected, possibly-long-lived race, not a broken network. Retries indefinitely.
 * 2. ICE/transport failure *after* a successful WHEP handshake — signaling worked (a
 *    real SDP answer came back) but the peer connection itself never connects. That's
 *    the actual "this network can't do WebRTC/UDP" signal, and is what triggers the
 *    low-latency HLS fallback (`media.hls_url`, via hls.js or native Safari HLS).
 *
 * Also handles the trainer-drops-mid-session edge case: once already `playing`, any
 * ICE failure just retries WHEP indefinitely (the network already proved it works) —
 * shown as a distinct "Reconnecting…" state, not the initial "connecting" one.
 */
export default function ClassroomVideoTile({ media }) {
  const [state, setState] = useState('idle'); // idle | connecting | waiting | playing | reconnecting | error
  const videoRef = useRef(null);
  const tileRef = useRef(null);
  const peerConnectionRef = useRef(null);
  const hlsRef = useRef(null);
  const connectedUrlRef = useRef(null);
  const hasPlayedRef = useRef(false);
  const usingHlsRef = useRef(false);
  const retryTimerRef = useRef(null);
  const signalingFailuresRef = useRef(0);
  const iceFailuresRef = useRef(0);
  const [retryTick, setRetryTick] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);
  // The student's own speaker control (independent of the trainer's mic mute). Starts
  // unmuted; flips to muted only if the browser blocks audio autoplay (see the effect
  // below), in which case the control becomes a visible "tap to unmute" affordance.
  const [localMuted, setLocalMuted] = useState(false);

  const whepUrl = media?.whep_url ?? null;
  const hlsUrl = media?.hls_url ?? null;

  useEffect(() => {
    if (!whepUrl) {
      teardown();
      setState('idle');
      return undefined;
    }
    if (connectedUrlRef.current === whepUrl && state === 'playing') return undefined;

    let cancelled = false;

    function scheduleRetry(nextState) {
      if (retryTimerRef.current) return; // already scheduled
      connectedUrlRef.current = null;
      setState(nextState);
      retryTimerRef.current = setTimeout(() => {
        retryTimerRef.current = null;
        if (!cancelled) setRetryTick((t) => t + 1);
      }, RETRY_DELAY_MS);
    }

    /** The actual "this network can't do WebRTC" fallback — only reached after real
     *  ICE failures, never from a plain signaling 404 (see module docstring). */
    function startHlsFallback() {
      const video = videoRef.current;
      if (!video || !hlsUrl) {
        setState('error');
        return;
      }
      if (peerConnectionRef.current) {
        peerConnectionRef.current.onconnectionstatechange = null;
        peerConnectionRef.current.close();
        peerConnectionRef.current = null;
      }
      usingHlsRef.current = true;

      const onHlsFailure = () => {
        if (cancelled) return;
        // Neither transport is working right now — don't dead-end; fall back to
        // retrying the whole cycle from scratch after a delay, same as any other
        // failure, so the student's view self-heals once the trainer's stream (or
        // the network) recovers instead of requiring a page refresh.
        usingHlsRef.current = false;
        iceFailuresRef.current = 0;
        if (hlsRef.current) {
          hlsRef.current.destroy();
          hlsRef.current = null;
        }
        setState('error');
        scheduleRetry('error');
      };

      if (Hls.isSupported()) {
        const hls = new Hls({ lowLatencyMode: true });
        hlsRef.current = hls;
        hls.loadSource(hlsUrl);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          if (cancelled) return;
          hasPlayedRef.current = true;
          signalingFailuresRef.current = 0;
          iceFailuresRef.current = 0;
          setState('playing');
          void video.play().catch(() => {});
        });
        hls.on(Hls.Events.ERROR, (_evt, data) => {
          if (!data?.fatal) return;
          onHlsFailure();
        });
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // Native Safari HLS support — no hls.js needed.
        video.src = hlsUrl;
        video.addEventListener(
          'loadedmetadata',
          () => {
            if (cancelled) return;
            hasPlayedRef.current = true;
            signalingFailuresRef.current = 0;
            iceFailuresRef.current = 0;
            setState('playing');
            void video.play().catch(() => {});
          },
          { once: true }
        );
        video.addEventListener('error', onHlsFailure, { once: true });
      } else {
        setState('error');
      }
    }

    const connectWhep = async () => {
      setState((s) => {
        if (hasPlayedRef.current) return 'reconnecting';
        return signalingFailuresRef.current >= SIGNALING_FAILURES_BEFORE_WAITING_COPY
          ? 'waiting'
          : 'connecting';
      });
      try {
        const pc = new RTCPeerConnection({ iceServers: ICE_SERVERS });
        peerConnectionRef.current = pc;

        pc.ontrack = (event) => {
          if (videoRef.current && videoRef.current.srcObject !== event.streams[0]) {
            videoRef.current.srcObject = event.streams[0];
          }
        };

        pc.onconnectionstatechange = () => {
          if (cancelled) return;
          if (pc.connectionState !== 'failed' && pc.connectionState !== 'disconnected') return;

          // Reaching here means signaling already succeeded once for this attempt
          // (we got past setRemoteDescription below) — this is a genuine transport
          // failure, not "no stream yet".
          if (hasPlayedRef.current) {
            // Was working before; the network already proved itself, so just retry
            // WHEP rather than jumping to HLS.
            scheduleRetry('reconnecting');
            return;
          }
          iceFailuresRef.current += 1;
          if (iceFailuresRef.current >= ICE_FAILURES_BEFORE_HLS) {
            startHlsFallback();
          } else {
            scheduleRetry('connecting');
          }
        };

        pc.addTransceiver('video', { direction: 'recvonly' });
        pc.addTransceiver('audio', { direction: 'recvonly' });

        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        // Two distinct failure points below, deliberately not merged into one big
        // try/catch: a network-level failure reaching the server at all (can't resolve
        // DNS, connection refused/timed out) is a real connectivity signal — the guide's
        // fallback scenario is about the UDP media transport being blocked, and while
        // that's usually invisible at this HTTPS-signaling layer, a request that can't
        // even land here is at least as strong a sign something about this network is
        // wrong. A clean, reachable 404 ("no stream at this path yet") is not — it just
        // means the trainer hasn't published yet, and HLS would fail for that same
        // reason, so it must never count toward the HLS fallback.
        let response;
        try {
          response = await fetch(whepUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/sdp' },
            body: offer.sdp,
          });
        } catch (networkErr) {
          if (cancelled) return;
          if (hasPlayedRef.current) {
            scheduleRetry('reconnecting');
            return;
          }
          iceFailuresRef.current += 1;
          if (iceFailuresRef.current >= ICE_FAILURES_BEFORE_HLS) {
            startHlsFallback();
          } else {
            scheduleRetry('connecting');
          }
          return;
        }

        if (!response.ok) {
          if (cancelled) return;
          if (hasPlayedRef.current) {
            scheduleRetry('reconnecting');
            return;
          }
          signalingFailuresRef.current += 1;
          scheduleRetry(
            signalingFailuresRef.current >= SIGNALING_FAILURES_BEFORE_WAITING_COPY
              ? 'waiting'
              : 'connecting'
          );
          return;
        }

        const answerSdp = await response.text();
        if (cancelled) return;
        await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });

        connectedUrlRef.current = whepUrl;
        hasPlayedRef.current = true;
        signalingFailuresRef.current = 0;
        iceFailuresRef.current = 0;
        setState('playing');
      } catch {
        // setRemoteDescription itself rejected (malformed answer) — treat the same as
        // a signaling failure; a broken/unparseable answer isn't fixed by HLS either.
        if (cancelled) return;
        if (hasPlayedRef.current) {
          scheduleRetry('reconnecting');
          return;
        }
        signalingFailuresRef.current += 1;
        scheduleRetry(
          signalingFailuresRef.current >= SIGNALING_FAILURES_BEFORE_WAITING_COPY
            ? 'waiting'
            : 'connecting'
        );
      }
    };

    if (!usingHlsRef.current) {
      void connectWhep();
    }

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [whepUrl, retryTick]);

  useEffect(() => teardown, []);

  // Keep isFullscreen in sync with the browser (covers Esc / the OS exiting fullscreen,
  // not just our own button).
  useEffect(() => {
    const onChange = () => setIsFullscreen(document.fullscreenElement === tileRef.current);
    document.addEventListener('fullscreenchange', onChange);
    return () => document.removeEventListener('fullscreenchange', onChange);
  }, []);

  // Once media is actually playing, drive playback + honor the local mute state. If the
  // browser blocks autoplay-with-sound (no recent user gesture), fall back to muted so
  // the video still shows, and surface the unmute control instead of a silent black box.
  useEffect(() => {
    if (state !== 'playing') return;
    const video = videoRef.current;
    if (!video) return;
    video.muted = localMuted;
    void video.play().catch(() => {
      setLocalMuted(true);
      video.muted = true;
      void video.play().catch(() => {});
    });
  }, [state, localMuted]);

  const toggleFullscreen = () => {
    const el = tileRef.current;
    if (!el) return;
    if (document.fullscreenElement) {
      void document.exitFullscreen();
    } else {
      void el.requestFullscreen?.().catch(() => {});
    }
  };

  const toggleLocalMute = () => {
    const next = !localMuted;
    setLocalMuted(next);
    const video = videoRef.current;
    if (video) {
      video.muted = next;
      if (!next) void video.play().catch(() => {});
    }
  };

  function teardown() {
    if (retryTimerRef.current) {
      clearTimeout(retryTimerRef.current);
      retryTimerRef.current = null;
    }
    if (peerConnectionRef.current) {
      peerConnectionRef.current.onconnectionstatechange = null;
      peerConnectionRef.current.close();
      peerConnectionRef.current = null;
    }
    if (hlsRef.current) {
      hlsRef.current.destroy();
      hlsRef.current = null;
    }
    usingHlsRef.current = false;
    connectedUrlRef.current = null;
    hasPlayedRef.current = false;
    signalingFailuresRef.current = 0;
    iceFailuresRef.current = 0;
  }

  if (!whepUrl) {
    return (
      <div className="flex aspect-video w-full flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 bg-slate-900/40 text-center">
        <div className="mb-2 text-2xl">📷</div>
        <p className="text-sm text-slate-500">Waiting for your trainer's camera…</p>
      </div>
    );
  }

  return (
    <div
      ref={tileRef}
      className={`group relative bg-black shadow-xl ${
        isFullscreen
          ? 'flex h-screen w-screen items-center justify-center rounded-none'
          : 'overflow-hidden rounded-2xl border border-slate-800 ring-1 ring-white/5'
      }`}
    >
      <div className={`relative w-full bg-slate-900 ${isFullscreen ? 'h-full' : 'aspect-video'}`}>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className={`h-full w-full ${
            isFullscreen || media?.screen_sharing ? 'object-contain' : 'object-cover'
          } ${media?.camera_off || state !== 'playing' ? 'invisible' : ''}`}
        />

        {media?.camera_off && state === 'playing' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 text-slate-500">
            <svg className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25zM3 3l18 18" />
            </svg>
            <span className="text-sm">Camera is off</span>
          </div>
        )}
        {state === 'connecting' && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-primary-500" />
          </div>
        )}
        {state === 'waiting' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-center">
            <span className="h-9 w-9 animate-spin rounded-full border-2 border-slate-700 border-t-primary-500" />
            <p className="text-sm font-medium text-slate-300">Waiting for your trainer to go live…</p>
            <p className="max-w-xs text-xs text-slate-500">
              The video will appear here automatically the moment they start their camera.
            </p>
          </div>
        )}
        {state === 'reconnecting' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 text-center">
            <span className="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-amber-500" />
            <p className="text-sm text-slate-400">Reconnecting…</p>
          </div>
        )}
        {state === 'error' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-1 text-center">
            <div className="text-2xl">⚠️</div>
            <p className="text-sm text-slate-400">Couldn't connect to the live video. Retrying…</p>
          </div>
        )}

        {/* LIVE badge — top-left, glass pill */}
        {state === 'playing' && (
          <div className="pointer-events-none absolute left-3 top-3 flex items-center gap-1.5 rounded-full bg-black/55 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wide text-white backdrop-blur">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-red-500" />
            Live
            {media?.mic_muted && <span className="font-normal text-slate-300">· Trainer muted</span>}
          </div>
        )}

        {/* Player controls — bottom-right. Always visible on touch; hover-reveal on
            pointer devices so they don't clutter the video. */}
        {(state === 'playing' || isFullscreen) && (
          <div className="absolute inset-x-0 bottom-0 flex items-center justify-end gap-2 bg-gradient-to-t from-black/70 via-black/20 to-transparent p-3 opacity-100 transition-opacity duration-200 sm:opacity-0 sm:group-hover:opacity-100 sm:group-focus-within:opacity-100">
            <button
              onClick={toggleLocalMute}
              title={localMuted ? 'Unmute' : 'Mute'}
              aria-label={localMuted ? 'Unmute audio' : 'Mute audio'}
              className="flex h-9 items-center gap-1.5 rounded-lg bg-black/50 px-2.5 text-white backdrop-blur transition hover:bg-black/70"
            >
              {localMuted ? (
                <>
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 9.75L19.5 12m0 0l2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
                  </svg>
                  <span className="text-xs font-medium">Unmute</span>
                </>
              ) : (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
                </svg>
              )}
            </button>
            <button
              onClick={toggleFullscreen}
              title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
              aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
              className="flex h-9 w-9 items-center justify-center rounded-lg bg-black/50 text-white backdrop-blur transition hover:bg-black/70"
            >
              {isFullscreen ? (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 9V4.5M9 9H4.5M9 9L3.75 3.75M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 9h4.5M15 9V4.5M15 9l5.25-5.25M15 15h4.5M15 15v4.5m0-4.5l5.25 5.25" />
                </svg>
              ) : (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
                </svg>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
