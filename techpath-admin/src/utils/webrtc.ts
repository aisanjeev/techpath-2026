export class WHEPClient {
  private pc: RTCPeerConnection | null = null;
  private whepUrl: string;
  private onStateChange: (state: string) => void;
  private onTrack: (track: MediaStreamTrack, streams: readonly MediaStream[]) => void;
  private cancelled = false;
  private retryTimer: ReturnType<typeof setTimeout> | null = null;
  private attempt = 0;

  constructor(
    whepUrl: string, 
    onStateChange: (state: string) => void,
    onTrack: (track: MediaStreamTrack, streams: readonly MediaStream[]) => void
  ) {
    this.whepUrl = whepUrl;
    this.onStateChange = onStateChange;
    this.onTrack = onTrack;
  }

  async start() {
    this.cancelled = false;
    this.attempt = 0;
    return this.connect();
  }

  /** MediaMTX 404s a WHEP path that has no publisher yet. The trainer subscribes the
   *  moment they approve, but the student's WHIP publish only starts once they clear
   *  the browser mic prompt — seconds later, or never. So a failed subscribe is retried
   *  rather than treated as fatal; `stop()` (doubt completed) is what ends it. */
  private async connect(): Promise<void> {
    // A retried attempt reuses nothing: the old pc is already closed past setLocalDescription.
    if (this.pc) {
      this.pc.close();
      this.pc = null;
    }

    this.pc = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    });

    this.pc.onconnectionstatechange = () => {
      if (!this.pc || this.cancelled) return;
      const state = this.pc.connectionState;
      this.onStateChange(state);
      // A publisher that drops (student refreshed, network blipped) leaves the trainer
      // on a dead pc with no error — reconnect on the same terms as a failed subscribe.
      if (state === 'failed' || state === 'disconnected') {
        this.scheduleRetry();
      }
    };

    this.pc.ontrack = (event) => {
      this.onTrack(event.track, event.streams);
    };

    this.pc.addTransceiver('audio', { direction: 'recvonly' });

    try {
      const offer = await this.pc.createOffer();
      await this.pc.setLocalDescription(offer);

      if (this.cancelled) return;

      const response = await fetch(this.whepUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/sdp' },
        body: offer.sdp
      });

      if (!response.ok) {
        throw new Error(`Failed to subscribe: ${response.status}`);
      }

      const answerSdp = await response.text();
      if (this.cancelled) return;

      await this.pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
      this.attempt = 0;
    } catch (err) {
      if (this.cancelled) return;
      this.scheduleRetry();
    }
  }

  private scheduleRetry() {
    this.attempt += 1;
    // 1s, 2s, 4s, then hold at 5s — a student who takes half a minute to find the
    // mic prompt still gets picked up.
    const delay = Math.min(1000 * 2 ** (this.attempt - 1), 5000);
    this.onStateChange(this.attempt === 1 ? 'connecting' : 'retrying');

    if (this.pc) {
      this.pc.close();
      this.pc = null;
    }
    if (this.retryTimer) clearTimeout(this.retryTimer);
    this.retryTimer = setTimeout(() => {
      this.retryTimer = null;
      if (!this.cancelled) void this.connect();
    }, delay);
  }

  stop() {
    this.cancelled = true;
    if (this.retryTimer) {
      clearTimeout(this.retryTimer);
      this.retryTimer = null;
    }
    if (this.pc) {
      this.pc.close();
      this.pc = null;
    }
    this.onStateChange('disconnected');
  }
}
