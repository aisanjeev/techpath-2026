export class WHIPClient {
  constructor(endpoint, onStateChange) {
    this.endpoint = endpoint;
    this.onStateChange = onStateChange || (() => {}); // 'connecting' | 'connected' | 'error' | 'disconnected'
    this.peerConnection = null;
    this.stream = null;
  }

  async start(audioConstraints = true) {
    this.onStateChange('connecting');
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: audioConstraints, video: false });
      this.peerConnection = new RTCPeerConnection();
      
      this.stream.getTracks().forEach(track => {
        this.peerConnection.addTrack(track, this.stream);
      });

      const offer = await this.peerConnection.createOffer();
      await this.peerConnection.setLocalDescription(offer);

      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/sdp' },
        body: offer.sdp,
      });

      if (!response.ok) {
        throw new Error(`WHIP connection failed with ${response.status}`);
      }

      const answerSdp = await response.text();
      await this.peerConnection.setRemoteDescription({ type: 'answer', sdp: answerSdp });
      
      this.peerConnection.onconnectionstatechange = () => {
        if (this.peerConnection.connectionState === 'connected') {
          this.onStateChange('connected');
        } else if (['failed', 'closed', 'disconnected'].includes(this.peerConnection.connectionState)) {
          this.onStateChange('disconnected');
          this.stop();
        }
      };
      
    } catch (err) {
      this.onStateChange('error');
      this.stop();
      throw err;
    }
  }

  stop() {
    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop());
      this.stream = null;
    }
    if (this.peerConnection) {
      this.peerConnection.close();
      this.peerConnection = null;
    }
    this.onStateChange('disconnected');
  }
}
