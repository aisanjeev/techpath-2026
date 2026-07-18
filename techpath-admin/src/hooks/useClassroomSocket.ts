'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import type { ClassroomEvent } from '@/types/classroom';
import { trainerService } from '@/services/trainer.service';

const WS_BASE = (process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000').replace(
  /^http/,
  'ws'
);

type EventHandler = (event: ClassroomEvent) => void;

/**
 * The trainer side of the classroom socket. Mints a fresh short-lived token on every
 * (re)connect rather than caching one — trainer WS tokens expire in 15 minutes, and a
 * dropped-wifi reconnect an hour into a session must not present a stale token.
 *
 * The socket is receive-only by design (see classroom_ws.py's docstring) — this hook
 * only ever delivers events via `subscribe`, it never sends anything.
 */
export function useClassroomSocket(sessionId: number, enabled: boolean) {
  const [connected, setConnected] = useState(false);
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
    if (!enabled || !sessionId) return;

    let cancelled = false;

    const connect = async () => {
      try {
        const { token } = await trainerService.mintWsToken(sessionId);
        if (cancelled) return;

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

        ws.onclose = () => {
          setConnected(false);
          wsRef.current = null;
          if (!cancelled) {
            reconnectTimerRef.current = setTimeout(connect, 2000);
          }
        };

        ws.onerror = () => {
          ws.close();
        };
      } catch {
        if (!cancelled) {
          reconnectTimerRef.current = setTimeout(connect, 3000);
        }
      }
    };

    void connect();

    return () => {
      cancelled = true;
      if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [sessionId, enabled]);

  return { connected, subscribe };
}
