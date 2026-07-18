import { useEffect, useRef } from 'react';
import { WHEPClient } from '@/utils/webrtc';
import { useClassroomStore } from '@/store/classroom.store';

interface DoubtAudioProps {
  whepUrl: string;
}

function DoubtAudioPlayer({ whepUrl }: DoubtAudioProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const clientRef = useRef<WHEPClient | null>(null);

  useEffect(() => {
    if (!audioRef.current) return;

    clientRef.current = new WHEPClient(
      whepUrl,
      (state) => {
        console.log(`Doubt audio state for ${whepUrl}: ${state}`);
      },
      (track, streams) => {
        if (audioRef.current && streams[0]) {
          audioRef.current.srcObject = streams[0];
        }
      }
    );

    clientRef.current.start().catch(console.error);

    return () => {
      if (clientRef.current) {
        clientRef.current.stop();
        clientRef.current = null;
      }
    };
  }, [whepUrl]);

  return <audio ref={audioRef} autoPlay />;
}

export function AudioMixer() {
  const doubtRequests = useClassroomStore((state) => state.doubtRequests);
  
  // Find all approved doubts with a valid whepUrl
  const activeDoubts = doubtRequests.filter(
    (d) => d.status === 'approved' && d.whep_url
  );

  return (
    <div style={{ display: 'none' }}>
      {activeDoubts.map((doubt) => (
        <DoubtAudioPlayer key={doubt.id} whepUrl={doubt.whep_url!} />
      ))}
    </div>
  );
}
