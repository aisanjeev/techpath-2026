import { useCallback, useEffect, useRef, useState } from 'react';
import type { ClassroomEvent } from '@/types/classroom';

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';
const WS_BASE = API_BASE_URL.replace(/^http/, 'ws');

type EventHandler = (event: ClassroomEvent) => void;

/**
 * The student side of the classroom socket. Unlike the trainer's, the token here is
 * long-lived (minted once at identify-time) and just reused across reconnects rather
 * than re-minted — a dropped wifi connection on a phone shouldn't need a fresh
 * roster-email lookup to get back in.
 *
 * Receive-only by design — see the backend's classroom_ws.py docstring. Every action a
 * student takes (confusion, vote) goes through a normal REST call; this only delivers
 * what the trainer broadcasts.
 */
export function useClassroomSocket(
  sessionId: number | null,
  token: string | null,
  enabled: boolean
) {
  const [connected, setConnected] = useState(false);
  const [kicked, setKicked] = useState(false);
  const handlersRef = useRef<Set<EventHandler>>(new Set());
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const subscribe = useCallback((handler: EventHandler) => {
    handlersRef.current.add(handler);
    return () => {
      handlersRef.current.delete(handler);
    };
  }, []);

  useEffect(() => {
    if (!enabled || !sessionId || !token) return;

    let cancelled = false;

    const connect = () => {
      const ws = new WebSocket(
        `${WS_BASE}/api/v1/ws/classroom/${sessionId}?token=${encodeURIComponent(token)}`
      );
      wsRef.current = ws;

      ws.onopen = () => setConnected(true);

      ws.onmessage = (evt) => {
        try {
          const parsed = JSON.parse(evt.data) as ClassroomEvent;
          handlersRef.current.forEach((handler) => handler(parsed));
        } catch {
          // Not a frame this client understands — ignore rather than crash the socket.
        }
      };

      ws.onclose = (event) => {
        setConnected(false);
        wsRef.current = null;
        if (event.code === 4403) {
          // Trainer removed this participant. The token is still cryptographically
          // valid but now permanently rejected server-side, so looping reconnect
          // attempts would just spin forever — surface it instead and stop.
          setKicked(true);
          return;
        }
        if (!cancelled) {
          reconnectTimerRef.current = setTimeout(connect, 2000);
        }
      };

      ws.onerror = () => {
        ws.close();
      };
    };

    connect();

    return () => {
      cancelled = true;
      if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [sessionId, token, enabled]);

  return { connected, subscribe, kicked };
}
