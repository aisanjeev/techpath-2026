import { Mic, MicOff } from 'lucide-react';
import { useClassroomStore } from '@/store/classroom.store';
import { trainerService } from '@/services/trainer.service';
import toast from 'react-hot-toast';
import { useState } from 'react';

interface Props {
  sessionId: number;
}

export function DoubtQueue({ sessionId }: Props) {
  const doubtRequests = useClassroomStore((state) => state.doubtRequests);
  const [busyId, setBusyId] = useState<number | null>(null);

  const pendingOrApproved = doubtRequests.filter(d => d.status === 'pending' || d.status === 'approved');

  if (pendingOrApproved.length === 0) return null;

  const handleApprove = async (doubtId: number) => {
    setBusyId(doubtId);
    try {
      await trainerService.approveDoubt(sessionId, doubtId);
      toast.success('Doubt audio approved');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not approve doubt');
    } finally {
      setBusyId(null);
    }
  };

  const handleStop = async (doubtId: number) => {
    setBusyId(doubtId);
    try {
      await trainerService.stopDoubt(sessionId, doubtId);
      toast.success('Doubt audio stopped');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not stop doubt');
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="rounded-xl border border-teal-900/40 bg-teal-950/20 p-3 mt-4">
      <p className="mb-2 flex items-center gap-1.5 text-xs font-medium uppercase tracking-wide text-teal-500">
        <Mic className="h-3.5 w-3.5" />
        Doubt Audio Requests ({pendingOrApproved.length})
      </p>
      <div className="space-y-1">
        {pendingOrApproved.map((d) => (
          <div
            key={d.id}
            className="flex items-center justify-between gap-2 rounded-lg px-2 py-1.5 bg-gray-900/40"
          >
            <div className="flex flex-col">
               <span className="truncate text-sm text-gray-200">{d.display_name}</span>
               {d.status === 'approved' && <span className="text-[10px] text-teal-400 animate-pulse">Live</span>}
            </div>
            <div className="flex gap-2 shrink-0">
              {d.status === 'pending' ? (
                <button
                  onClick={() => handleApprove(d.id)}
                  disabled={busyId === d.id}
                  className="rounded-md border border-teal-800 px-2 py-1 text-[11px] font-medium text-teal-400 transition hover:bg-teal-900/40 disabled:opacity-50"
                >
                  Enable Mic
                </button>
              ) : (
                <button
                  onClick={() => handleStop(d.id)}
                  disabled={busyId === d.id}
                  className="flex items-center gap-1 rounded-md border border-red-800 bg-red-500/10 px-2 py-1 text-[11px] font-medium text-red-400 transition hover:bg-red-900/40 disabled:opacity-50"
                >
                  <MicOff className="h-3 w-3" /> Stop Mic
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
