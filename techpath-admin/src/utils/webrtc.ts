export class WHEPClient {
  private pc: RTCPeerConnection | null = null;
  private whepUrl: string;
  private onStateChange: (state: string) => void;
  private onTrack: (track: MediaStreamTrack, streams: readonly MediaStream[]) => void;
  private cancelled = false;

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
    this.pc = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    });

    this.pc.onconnectionstatechange = () => {
      if (this.pc) this.onStateChange(this.pc.connectionState);
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
    } catch (err) {
      if (this.cancelled) return;
      this.onStateChange('error');
      this.stop();
    }
  }

  stop() {
    this.cancelled = true;
    if (this.pc) {
      this.pc.close();
      this.pc = null;
    }
    this.onStateChange('disconnected');
  }
}
