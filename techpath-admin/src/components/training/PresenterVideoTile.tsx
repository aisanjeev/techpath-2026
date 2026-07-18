'use client';

import { useEffect, useRef, useState } from 'react';
import { Mic, MicOff, Monitor, PhoneOff, Radio, Video, VideoOff } from 'lucide-react';
import { trainerService } from '@/services/trainer.service';

interface Props {
  sessionId: number;
  /** The trainer-only WHIP publish URL, present only while the session is live and has
   *  a stream path minted (see TrainingSession.media.whip_url). */
  whipUrl?: string | null;
  /** Whether the session is currently live — publishing only ever runs while true. */
  isLive: boolean;
  /** Whether the trainer has chosen to broadcast camera/mic. Going live no longer implies
   *  this: capture and publishing only start once the trainer opts in, so a session can
   *  run slides-only with no camera prompt and no video frame for students. */
  broadcasting: boolean;
  /** Called with the new value after the broadcast toggle is persisted. */
  onBroadcastingChange: (broadcasting: boolean) => void;
  /** Whether the session is currently flagged to keep the recording. */
  keepRecording?: boolean;
  /** Callback when the recording flag is toggled successfully. */
  onToggleRecording?: (keep: boolean) => void;
}

// Publish lifecycle. Crucially, 'connecting' and 'live' are SEPARATE: WHIP signaling
// succeeding (a 201 + SDP answer) does NOT mean media is actually reaching the server —
// that only happens once the WebRTC peer connection reports `connected`, i.e. ICE
// completed over UDP. Conflating the two (showing "Live" on signaling success) hides
// the common failure where the media UDP port is firewalled: signaling works over
// HTTPS, the badge says "Live", but no student can ever see anything.
type PublishState = 'idle' | 'starting' | 'connecting' | 'live' | 'stalled' | 'error';

const ICE_SERVERS = [{ urls: 'stun:stun.l.google.com:19302' }];
// How long to wait in 'connecting' (signaling done, ICE negotiating) before warning the
// trainer that media isn't getting through. A healthy connection completes in ~1-3s;
// well past that means the media transport (UDP) almost certainly can't reach the server.
const ICE_CONNECT_TIMEOUT_MS = 12_000;

/**
 * Teacher-side camera/mic capture and WebRTC WHIP publish, ported from the
 * ClassroomBroadcaster class in CLASSROOM-WEBAPP-GUIDE.md into a React component. Media
 * never touches this app's backend — this posts the SDP offer straight to the
 * self-hosted MediaMTX server at `whipUrl` and renders the local preview directly from
 * the captured MediaStream. Mute/camera/screen-share toggles additionally call
 * trainerService.setMediaState so students' clients learn about the change (see
 * ClassroomVideoTile.jsx's `media_state_changed` handling) — that broadcast is best-
 * effort UI sync, independent of the local track mute this component always applies.
 */
export function PresenterVideoTile({
  sessionId,
  whipUrl,
  isLive,
  broadcasting,
  onBroadcastingChange,
  keepRecording = false,
  onToggleRecording,
}: Props) {
  const [state, setState] = useState<PublishState>('idle');
  const [error, setError] = useState<string | null>(null);
  const [muted, setMuted] = useState(false);
  const [cameraOff, setCameraOff] = useState(false);
  const [screenSharing, setScreenSharing] = useState(false);
  const [isTogglingRecord, setIsTogglingRecord] = useState(false);
  const [isTogglingBroadcast, setIsTogglingBroadcast] = useState(false);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const localStreamRef = useRef<MediaStream | null>(null);
  const cameraTrackRef = useRef<MediaStreamTrack | null>(null);
  const peerConnectionRef = useRef<RTCPeerConnection | null>(null);
  const startedForUrlRef = useRef<string | null>(null);
  const stallTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    // getUserMedia is deliberately downstream of `broadcasting`: this effect not running
    // is what keeps the browser from ever prompting for camera/mic in a slides-only
    // session, so the gate has to live here rather than in the render below.
    if (!isLive || !broadcasting || !whipUrl) {
      stop();
      return;
    }
    if (startedForUrlRef.current === whipUrl && (state === 'live' || state === 'connecting')) {
      return;
    }

    let cancelled = false;

    const start = async () => {
      setState('starting');
      setError(null);
      try {
        const localStream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 1280 }, height: { ideal: 720 }, frameRate: { ideal: 30 } },
          audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true },
        });
        if (cancelled) {
          localStream.getTracks().forEach((t) => t.stop());
          return;
        }
        localStreamRef.current = localStream;
        cameraTrackRef.current = localStream.getVideoTracks()[0] ?? null;
        if (videoRef.current) videoRef.current.srcObject = localStream;

        const pc = new RTCPeerConnection({ iceServers: ICE_SERVERS });
        peerConnectionRef.current = pc;
        localStream.getTracks().forEach((track) => pc.addTrack(track, localStream));

        // The single source of truth for whether media is actually flowing. Signaling
        // success below only gets us to 'connecting'; this is what promotes to 'live'.
        pc.onconnectionstatechange = () => {
          if (cancelled) return;
          const cs = pc.connectionState;
          if (cs === 'connected') {
            clearStallTimer();
            setState('live');
            setError(null);
          } else if (cs === 'failed') {
            clearStallTimer();
            setState('stalled');
            setError(
              'Your video isn’t reaching the server. This usually means the media port ' +
                '(UDP) is blocked on your network or the streaming server.'
            );
          }
        };

        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        const response = await fetch(whipUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/sdp' },
          body: offer.sdp,
        });
        if (!response.ok) {
          throw new Error(`Failed to publish stream: ${response.status} ${response.statusText}`);
        }
        const answerSdp = await response.text();
        if (cancelled) return;
        await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });

        // Signaling is done — but do NOT claim "Live" yet. Wait for the connection to
        // actually establish (onconnectionstatechange above), and warn if it never does.
        startedForUrlRef.current = whipUrl;
        setState('connecting');
        clearStallTimer();
        stallTimerRef.current = setTimeout(() => {
          if (cancelled) return;
          setState((s) => (s === 'connecting' ? 'stalled' : s));
          setError((e) =>
            e ??
            'Still connecting… your video may not be reaching the server. Check that the ' +
              'streaming server allows WebRTC media (UDP) from your network.'
          );
        }, ICE_CONNECT_TIMEOUT_MS);
      } catch (err) {
        if (cancelled) return;
        setState('error');
        setError(err instanceof Error ? err.message : 'Could not start camera/microphone');
        stop();
      }
    };

    void start();

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLive, broadcasting, whipUrl]);

  function clearStallTimer() {
    if (stallTimerRef.current) {
      clearTimeout(stallTimerRef.current);
      stallTimerRef.current = null;
    }
  }

  function stop() {
    clearStallTimer();
    if (peerConnectionRef.current) {
      peerConnectionRef.current.onconnectionstatechange = null;
      peerConnectionRef.current.close();
      peerConnectionRef.current = null;
    }
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((track) => track.stop());
      localStreamRef.current = null;
    }
    cameraTrackRef.current = null;
    startedForUrlRef.current = null;
    setScreenSharing(false);
    // Mute/camera flags describe tracks that no longer exist — carrying them into the
    // next broadcast would show the trainer as muted the moment they go live again.
    setMuted(false);
    setCameraOff(false);
    setState((s) => (s === 'error' ? s : 'idle'));
  }

  useEffect(() => stop, []);

  // Controls act on local tracks, so they work as soon as capture is running — they must
  // not be gated on the connection actually establishing (a stalled publish should still
  // let the trainer mute/turn off camera).
  const hasStream = state === 'connecting' || state === 'live' || state === 'stalled';

  const toggleAudio = () => {
    const stream = localStreamRef.current;
    if (!stream) return;
    const next = !muted;
    stream.getAudioTracks().forEach((track) => {
      track.enabled = !next;
    });
    setMuted(next);
    void trainerService.setMediaState(sessionId, { mic_muted: next }).catch(() => {});
  };

  const toggleVideo = () => {
    const stream = localStreamRef.current;
    if (!stream) return;
    const next = !cameraOff;
    stream.getVideoTracks().forEach((track) => {
      track.enabled = !next;
    });
    setCameraOff(next);
    void trainerService.setMediaState(sessionId, { camera_off: next }).catch(() => {});
  };

  const startScreenShare = async () => {
    const pc = peerConnectionRef.current;
    if (!pc) return;
    try {
      const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
      const screenTrack = screenStream.getVideoTracks()[0];

      const videoSender = pc.getSenders().find((s) => s.track?.kind === 'video');
      if (videoSender) await videoSender.replaceTrack(screenTrack);
      if (videoRef.current) videoRef.current.srcObject = screenStream;

      screenTrack.onended = () => {
        void stopScreenShare();
      };

      setScreenSharing(true);
      void trainerService.setMediaState(sessionId, { screen_sharing: true }).catch(() => {});
    } catch {
      // Trainer cancelled the share picker — no-op, same as the guide's behavior.
    }
  };

  const stopScreenShare = async () => {
    const pc = peerConnectionRef.current;
    const cameraTrack = cameraTrackRef.current;
    if (pc && cameraTrack) {
      const sender = pc.getSenders().find((s) => s.track?.kind === 'video');
      if (sender) await sender.replaceTrack(cameraTrack);
    }
    if (videoRef.current && localStreamRef.current) {
      videoRef.current.srcObject = localStreamRef.current;
    }
    setScreenSharing(false);
    void trainerService.setMediaState(sessionId, { screen_sharing: false }).catch(() => {});
  };

  const handleToggleRecording = async () => {
    if (isTogglingRecord) return;
    setIsTogglingRecord(true);
    try {
      const updated = await trainerService.toggleRecording(sessionId, !keepRecording);
      if (onToggleRecording) {
        onToggleRecording(updated.keep_recording);
      }
    } catch {
      setError('Failed to toggle recording');
    } finally {
      setIsTogglingRecord(false);
    }
  };

  const handleToggleBroadcast = async () => {
    if (isTogglingBroadcast) return;
    const next = !broadcasting;
    setIsTogglingBroadcast(true);
    setError(null);
    try {
      await trainerService.setMediaState(sessionId, { broadcasting: next });
      // Only after the server agrees, so students and the presenter can't disagree about
      // whether a stream exists. The parent flipping `broadcasting` is what actually
      // starts or tears down capture (see the effect above).
      onBroadcastingChange(next);
    } catch {
      setError(next ? 'Could not go live' : 'Could not stop the broadcast');
    } finally {
      setIsTogglingBroadcast(false);
    }
  };

  if (!isLive) return null;

  // Not broadcasting: no <video> element at all, just the control to start. Students see
  // no video frame either (the classroom hides the tile on broadcasting=false).
  if (!broadcasting) {
    return (
      <div className="rounded-xl border border-gray-800 bg-gray-900/90 p-3 backdrop-blur">
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <VideoOff className="h-4 w-4 shrink-0" />
          <span>Camera off — students see slides only</span>
        </div>
        {error && <p className="mt-1.5 text-xs text-amber-400">{error}</p>}
        <button
          onClick={handleToggleBroadcast}
          disabled={isTogglingBroadcast || !whipUrl}
          title={whipUrl ? 'Start your camera and microphone' : 'Live media is unavailable'}
          className="mt-2 flex w-full items-center justify-center gap-1.5 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white transition hover:bg-teal-500 disabled:opacity-40"
        >
          <Radio className="h-4 w-4" />
          {isTogglingBroadcast ? 'Starting…' : 'Go live with video'}
        </button>
      </div>
    );
  }

  const badge =
    state === 'live'
      ? { text: 'Live', dot: 'text-red-500' }
      : state === 'connecting'
        ? { text: 'Connecting…', dot: 'text-amber-500' }
        : state === 'starting'
          ? { text: 'Starting…', dot: 'text-gray-500' }
          : state === 'stalled'
            ? { text: 'Not connected', dot: 'text-red-500' }
            : state === 'error'
              ? { text: 'Error', dot: 'text-red-500' }
              : { text: 'Off', dot: 'text-gray-500' };

  return (
    <div className="overflow-hidden rounded-xl border border-gray-800 bg-black">
      <div className="relative aspect-video w-full bg-gray-900">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className={`h-full w-full object-cover ${cameraOff && !screenSharing ? 'invisible' : ''}`}
        />
        {cameraOff && !screenSharing && (
          <div className="absolute inset-0 flex items-center justify-center text-sm text-gray-500">
            Camera off
          </div>
        )}
        <div className="absolute left-2 top-2 flex items-center gap-1.5 rounded-full bg-black/60 px-2 py-1 text-[10px] font-medium uppercase tracking-wide text-white">
          <Radio className={`h-3 w-3 ${badge.dot}`} />
          {badge.text}
        </div>
        {keepRecording && (
          <div className="absolute right-2 top-2 flex items-center gap-1.5 rounded-full bg-black/60 px-2 py-1 text-[10px] font-medium uppercase tracking-wide text-white">
            <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
            REC
          </div>
        )}
      </div>
      {error && <p className="px-3 py-1.5 text-xs text-amber-400">{error}</p>}
      <div className="flex items-center gap-2 border-t border-gray-800 px-3 py-2">
        <button
          onClick={toggleAudio}
          disabled={!hasStream}
          title={muted ? 'Unmute' : 'Mute'}
          className="rounded-md p-1.5 text-gray-400 transition hover:bg-gray-800 hover:text-white disabled:opacity-40"
        >
          {muted ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
        </button>
        <button
          onClick={toggleVideo}
          disabled={!hasStream}
          title={cameraOff ? 'Turn camera on' : 'Turn camera off'}
          className="rounded-md p-1.5 text-gray-400 transition hover:bg-gray-800 hover:text-white disabled:opacity-40"
        >
          {cameraOff ? <VideoOff className="h-4 w-4" /> : <Video className="h-4 w-4" />}
        </button>
        <button
          onClick={() => (screenSharing ? void stopScreenShare() : void startScreenShare())}
          disabled={!hasStream}
          title={screenSharing ? 'Stop sharing screen' : 'Share screen'}
          className={`rounded-md p-1.5 transition hover:bg-gray-800 hover:text-white disabled:opacity-40 ${
            screenSharing ? 'text-teal-400' : 'text-gray-400'
          }`}
        >
          <Monitor className="h-4 w-4" />
        </button>
        <button
          onClick={handleToggleBroadcast}
          disabled={isTogglingBroadcast}
          title="Stop broadcasting — releases the camera and hides the video for students"
          className="rounded-md p-1.5 text-gray-400 transition hover:bg-red-500/10 hover:text-red-400 disabled:opacity-40"
        >
          <PhoneOff className="h-4 w-4" />
        </button>
        <div className="ml-auto">
          <button
            onClick={handleToggleRecording}
            disabled={!hasStream || isTogglingRecord}
            title={keepRecording ? 'Stop Recording' : 'Start Recording'}
            className={`flex items-center gap-1.5 rounded-md px-2 py-1.5 text-xs font-medium transition disabled:opacity-40 ${
              keepRecording
                ? 'bg-red-500/10 text-red-500 hover:bg-red-500/20'
                : 'text-gray-400 hover:bg-gray-800 hover:text-white'
            }`}
          >
            <div className={`h-2.5 w-2.5 rounded-full ${keepRecording ? 'bg-red-500' : 'bg-gray-400'}`} />
            {keepRecording ? 'Recording' : 'Record'}
          </button>
        </div>
      </div>
    </div>
  );
}
