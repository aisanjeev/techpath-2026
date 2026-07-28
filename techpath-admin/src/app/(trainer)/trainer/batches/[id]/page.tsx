'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowLeft,
  Users,
  Play,
  AlertTriangle,
  Radio,
  BookOpen,
  Folder,
  GraduationCap,
  ChevronDown,
  ChevronUp,
  PlusCircle,
  UploadCloud,
  Settings,
  FileText,
  CheckCircle,
  List,
  LayoutGrid,
  ChevronRight,
  X,
  Search,
  ChevronLeft,
  Mail,
  Phone
} from 'lucide-react';
import toast from 'react-hot-toast';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { PageLoader } from '@/components/ui/Spinner';
import { trainerService } from '@/services/trainer.service';
import type {
  TrainerBatchSummary,
  TrainingModule,
  TrainingSession,
  TrainingStudent,
} from '@/types/training';

// Simple Circular Progress SVG Component
function CircularProgress({ percentage, label, subtext, size = 120, strokeWidth = 10, color = 'text-emerald-500' }: { percentage: number, label: string, subtext?: string, size?: number, strokeWidth?: number, color?: string }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="relative flex flex-col items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          className="text-gray-100"
          strokeWidth={strokeWidth}
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
        <circle
          className={`${color} transition-all duration-1000 ease-in-out`}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-xl font-bold text-gray-900">{percentage}%</span>
        {subtext && <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 max-w-[70%] leading-tight mt-1">{subtext}</span>}
      </div>
      {label && <p className="mt-2 text-xs font-medium text-gray-500">{label}</p>}
    </div>
  );
}

export default function TrainerBatchPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const batchId = Number(id);
  const router = useRouter();

  const [batch, setBatch] = useState<TrainerBatchSummary | null>(null);
  const [modules, setModules] = useState<TrainingModule[]>([]);
  const [students, setStudents] = useState<TrainingStudent[]>([]);
  const [sessions, setSessions] = useState<TrainingSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState<number | null>(null);
  const [showRosterModal, setShowRosterModal] = useState(false);
  const [rosterSearch, setRosterSearch] = useState('');
  const [rosterPage, setRosterPage] = useState(1);
  const ROSTER_PAGE_SIZE = 10;

  const [openPrograms, setOpenPrograms] = useState<Record<number, boolean>>({});
  const [openModules, setOpenModules] = useState<Record<number, boolean>>({});

  const toggleProgram = (progId: number) => {
    setOpenPrograms((prev) => ({ ...prev, [progId]: !prev[progId] }));
  };

  const toggleModule = (e: React.MouseEvent, moduleId: number) => {
    e.stopPropagation();
    setOpenModules((prev) => ({ ...prev, [moduleId]: !prev[moduleId] }));
  };

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [b, m, s, sess] = await Promise.all([
        trainerService.getBatch(batchId),
        trainerService.getBatchModules(batchId),
        trainerService.getBatchStudents(batchId),
        trainerService.getBatchSessions(batchId),
      ]);
      setBatch(b);
      setModules(m);
      setStudents(s);
      setSessions(sess);
      
      if (b.programs && b.programs.length > 0) {
        setOpenPrograms({ [b.programs[0].id]: true });
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load the batch');
      router.push('/trainer');
    } finally {
      setLoading(false);
    }
  }, [batchId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  const presentModule = async (module: TrainingModule) => {
    setStarting(module.id);
    try {
      const existing = sessions.find(
        (s) => s.module_id === module.id && s.status !== 'ended'
      );
      const session =
        existing ??
        (await trainerService.createSession({
          batch_id: batchId,
          module_id: module.id,
          title: module.title,
        }));

      const live = await trainerService.startSession(session.id, module.id);
      toast.success('Session is live');
      router.push(`/trainer/sessions/${live.id}`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not start the session');
    } finally {
      setStarting(null);
    }
  };

  if (loading || !batch) return <PageLoader />;

  const liveSession = sessions.find((s) => s.status === 'live');
  const overallProgress = batch.module_count > 0 
    ? Math.round((batch.completed_module_count / batch.module_count) * 100) 
    : 0;

  return (
    <div className="max-w-7xl mx-auto pb-12">
      <Link
        href="/trainer"
        className="mb-4 inline-flex items-center gap-1 text-sm font-semibold text-emerald-600 hover:text-emerald-700 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Batches
      </Link>

      {/* Header */}
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">{batch.name}</h1>
          <div className="mt-2 flex flex-wrap items-center gap-4 text-sm text-gray-500 font-medium">
            <span className="flex items-center gap-1.5"><Users className="w-4 h-4" /> {students.length} Students</span>
            <span>·</span>
            <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-gray-400" /> {batch.mode}</span>
            {batch.location && (
               <>
                 <span>·</span>
                 <span>{batch.location}</span>
               </>
            )}
            <span>·</span>
            <span>Batch ID: {batch.code || batch.external_id}</span>
          </div>
        </div>
        <Badge className="bg-emerald-50 text-emerald-700 hover:bg-emerald-50 px-4 py-1.5 text-sm font-semibold rounded-full border-none shadow-sm">
          {batch.status === 'running' ? 'Running' : batch.status}
        </Badge>
      </div>

      {liveSession && (
        <Card className="mb-8 border-emerald-500 bg-emerald-50/50 p-4 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100">
                 <Radio className="h-5 w-5 text-emerald-600 animate-pulse" />
              </div>
              <div>
                <p className="text-sm font-bold text-emerald-900">
                  Live Session: {liveSession.module_title ?? liveSession.title}
                </p>
                <p className="text-xs font-medium text-emerald-700 mt-0.5">
                  Join code <span className="font-mono bg-white px-1.5 py-0.5 rounded text-emerald-900 shadow-sm border border-emerald-100">{liveSession.join_code}</span>
                </p>
              </div>
            </div>
            <Link href={`/trainer/sessions/${liveSession.id}`}>
              <Button className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold shadow-sm">Resume Session</Button>
            </Link>
          </div>
        </Card>
      )}

      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <Card className="p-5 flex flex-col justify-center border-emerald-100 bg-white shadow-sm hover:border-emerald-200 transition-colors">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg">
              <GraduationCap className="w-4 h-4" />
            </div>
            <p className="text-[11px] font-bold text-emerald-600 uppercase tracking-widest">Total Programs</p>
          </div>
          <p className="text-3xl font-bold text-gray-900 mt-2">{batch.programs.length}</p>
          <p className="text-xs font-medium text-gray-500 mt-1">Active Programs</p>
        </Card>

        <Card className="p-5 flex flex-col justify-center border-blue-100 bg-white shadow-sm hover:border-blue-200 transition-colors">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
              <BookOpen className="w-4 h-4" />
            </div>
            <p className="text-[11px] font-bold text-blue-600 uppercase tracking-widest">Total Modules</p>
          </div>
          <p className="text-3xl font-bold text-gray-900 mt-2">{batch.module_count}</p>
          <p className="text-xs font-medium text-gray-500 mt-1">Across Programs</p>
        </Card>

        <Card className="p-5 flex flex-col justify-center border-amber-100 bg-white shadow-sm hover:border-amber-200 transition-colors">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-amber-50 text-amber-600 rounded-lg">
              <Folder className="w-4 h-4" />
            </div>
            <p className="text-[11px] font-bold text-amber-600 uppercase tracking-widest">Total Assets</p>
          </div>
          <p className="text-3xl font-bold text-gray-900 mt-2">{batch.asset_count}</p>
          <p className="text-xs font-medium text-gray-500 mt-1">Study Materials</p>
        </Card>

        <Card className="p-5 flex flex-col justify-center items-center border-purple-100 bg-purple-50/20 shadow-sm hover:border-purple-200 transition-colors">
          <p className="text-[11px] font-bold text-purple-600 uppercase tracking-widest mb-3 self-start w-full text-center">Overall Progress</p>
          <CircularProgress percentage={overallProgress} label="" subtext="Completed" color="text-purple-600" size={80} strokeWidth={6} />
        </Card>
      </div>

      <div className="grid gap-8 lg:grid-cols-3 xl:grid-cols-4">
        {/* Main Content: Curriculum */}
        <div className="lg:col-span-2 xl:col-span-3">
          <div className="flex items-center justify-between mb-4 px-2">
             <div>
                <h2 className="text-xl font-bold text-gray-900 tracking-tight">Curriculum Programs</h2>
                <p className="text-sm text-gray-500 mt-1">Expand a program to view modules and assets</p>
             </div>
          </div>

          {!batch.programs || batch.programs.length === 0 ? (
            <Card className="p-12 text-center border-dashed border-2 border-gray-200">
              <AlertTriangle className="mx-auto h-12 w-12 text-amber-400 mb-4" />
              <h3 className="text-xl font-bold text-gray-900">No training programs linked</h3>
              <p className="mx-auto mt-2 max-w-sm text-sm text-gray-500">
                An admin needs to link this batch to a training program before there is anything to present.
              </p>
            </Card>
          ) : (
            <div className="space-y-6">
              {batch.programs.map((prog, idx) => {
                const isOpen = openPrograms[prog.id];
                const progModules = modules.filter(m => m.program_id === prog.id);
                // Assign a color theme based on index for the left accent border
                const colors = ['bg-emerald-500', 'bg-purple-500', 'bg-blue-500', 'bg-amber-500'];
                const accentColor = colors[idx % colors.length];

                return (
                  <Card key={prog.id} className="overflow-hidden border-gray-200 shadow-sm transition-shadow hover:shadow-md rounded-2xl">
                    {/* Accordion Header */}
                    <div 
                      className="flex items-stretch cursor-pointer relative bg-white hover:bg-gray-50 transition-colors"
                      onClick={() => toggleProgram(prog.id)}
                    >
                      <div className={`w-2 flex-shrink-0 ${accentColor}`} />
                      <div className="flex-1 p-5 md:p-6 flex flex-col md:flex-row md:items-center gap-6 justify-between">
                        <div className="flex items-start gap-4 flex-1">
                           <div className={`p-3 rounded-xl shadow-sm border ${accentColor.replace('bg-', 'border-').replace('500', '100')} ${accentColor.replace('bg-', 'bg-').replace('500', '50')} ${accentColor.replace('bg-', 'text-')}`}>
                             <GraduationCap className="w-5 h-5" />
                           </div>
                           <div className="pt-0.5">
                             <div className="flex items-center gap-3 flex-wrap">
                               <h3 className="text-lg font-bold text-gray-900 tracking-tight">{prog.title}</h3>
                               {prog.level && (
                                 <Badge className="bg-emerald-50 text-emerald-700 border border-emerald-100 font-semibold text-[10px] px-2 py-0.5 rounded-full uppercase tracking-wider">
                                   {prog.level}
                                 </Badge>
                               )}
                             </div>
                             <p className="mt-1 text-xs font-medium text-gray-500 max-w-2xl leading-relaxed">
                               {prog.summary || 'Comprehensive training program designed to take students from basics to advanced levels.'}
                             </p>
                           </div>
                        </div>

                        <div className="flex items-center gap-6 mt-4 md:mt-0 pl-14 md:pl-0 pr-2">
                           <div className="flex items-center gap-2 text-gray-600">
                              <BookOpen className="w-5 h-5 text-gray-300" />
                              <div className="flex flex-col">
                                 <span className="text-lg font-bold leading-none text-gray-900">{prog.module_count}</span>
                                 <span className="text-[9px] font-bold uppercase tracking-wider text-gray-500 mt-0.5">Modules</span>
                              </div>
                           </div>
                           <div className="flex items-center gap-2 text-gray-600">
                              <Folder className="w-5 h-5 text-gray-300" />
                              <div className="flex flex-col">
                                 <span className="text-lg font-bold leading-none text-gray-900">{prog.asset_count}</span>
                                 <span className="text-[9px] font-bold uppercase tracking-wider text-gray-500 mt-0.5">Assets</span>
                              </div>
                           </div>
                           <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center ml-2 transition-transform duration-200 shadow-sm border border-gray-200 hover:bg-gray-200">
                              {isOpen ? <ChevronUp className="w-5 h-5 text-gray-600" /> : <ChevronDown className="w-5 h-5 text-gray-600" />}
                           </div>
                        </div>
                      </div>
                    </div>

                    {/* Accordion Body */}
                    {isOpen && (
                      <div className="border-t border-gray-100 bg-gray-50 p-5 md:p-8 ml-2">
                        {progModules.length === 0 ? (
                          <div className="text-center py-10 bg-white rounded-xl border border-dashed border-gray-200">
                            <p className="text-base font-bold text-gray-900">No modules yet</p>
                            <p className="mt-1 text-sm text-gray-500">An admin needs to add modules to this program.</p>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            {progModules.map((module, mIdx) => {
                              const isModOpen = openModules[module.id];
                              return (
                              <div key={module.id} className="flex flex-col rounded-xl border border-gray-200 bg-white hover:border-emerald-300 hover:shadow-sm transition-all group overflow-hidden">
                                <div 
                                  className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-3 cursor-pointer"
                                  onClick={(e) => toggleModule(e, module.id)}
                                >
                                  <div className="flex items-center gap-4 flex-1 min-w-0">
                                    <span className="w-8 text-sm font-bold text-emerald-600 font-mono tracking-tighter">
                                      {String(mIdx + 1).padStart(2, '0')}
                                    </span>
                                    <div className="min-w-0 flex-1">
                                      <p className="truncate text-sm font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors">
                                        {module.title}
                                      </p>
                                    </div>
                                  </div>
                                  <div className="flex items-center gap-4 pl-12 sm:pl-0">
                                    <div className="flex items-center gap-1.5 text-xs font-semibold text-gray-500 min-w-[80px]">
                                      <Folder className="w-3.5 h-3.5 text-gray-400" />
                                      {module.asset_count} asset{module.asset_count !== 1 && 's'}
                                    </div>
                                    <div className="flex items-center gap-2">
                                      <Button
                                        variant="outline"
                                        className="border-emerald-200 text-emerald-700 hover:bg-emerald-50 hover:text-emerald-800 transition-colors font-semibold shadow-sm h-8 px-3 text-xs"
                                        onClick={(e) => {
                                          e.stopPropagation();
                                          void presentModule(module);
                                        }}
                                        disabled={starting !== null || module.asset_count === 0}
                                      >
                                        <Play className="mr-1.5 h-3.5 w-3.5 fill-emerald-700/20" />
                                        {starting === module.id ? 'Starting…' : 'Present'}
                                      </Button>
                                      <button 
                                        className="p-1.5 text-gray-400 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors border border-transparent hover:border-gray-200"
                                      >
                                        {isModOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                                      </button>
                                    </div>
                                  </div>
                                </div>
                                {isModOpen && (
                                  <div className="p-4 bg-gray-50 border-t border-gray-100 text-sm text-gray-600">
                                    <div className="mb-4">
                                      <p className="font-semibold text-gray-800 mb-1">Module Description</p>
                                      <p>{module.description || 'No detailed description provided for this module.'}</p>
                                      {module.estimated_minutes && (
                                        <p className="mt-2 text-xs font-semibold text-gray-500">Estimated Duration: {module.estimated_minutes} mins</p>
                                      )}
                                    </div>

                                    <div>
                                      <p className="font-semibold text-gray-800 mb-2">Assets ({module.asset_count})</p>
                                      {(module as any).assets && (module as any).assets.length > 0 ? (
                                        <div className="space-y-2">
                                          {(module as any).assets.map((assetLink: any) => (
                                            <div key={assetLink.id} className="flex items-center justify-between p-2.5 bg-white border border-gray-200 rounded-lg shadow-sm">
                                              <div className="flex items-center gap-3">
                                                <div className="p-1.5 bg-emerald-50 text-emerald-600 rounded-md">
                                                  <Folder className="w-4 h-4" />
                                                </div>
                                                <div>
                                                  <p className="text-sm font-semibold text-gray-900">{assetLink.asset?.title || 'Unknown Asset'}</p>
                                                  <p className="text-xs text-gray-500 uppercase tracking-wider">{assetLink.asset?.kind}</p>
                                                </div>
                                              </div>
                                            </div>
                                          ))}
                                        </div>
                                      ) : (
                                        <p className="text-gray-500 italic text-xs">No assets have been added to this module yet.</p>
                                      )}
                                    </div>
                                  </div>
                                )}
                              </div>
                            )})}
                          </div>
                        )}
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          
          {/* Roster Card */}
          <Card className="p-0 overflow-hidden border-gray-200 shadow-sm rounded-2xl">
            <div className="p-5 border-b border-gray-100 flex items-center justify-between bg-white">
              <h3 className="font-bold text-gray-900 flex items-center gap-2 text-base">
                Roster ({students.length})
              </h3>
            </div>
            <div className="max-h-[320px] overflow-y-auto p-2 bg-gray-50/30">
              {students.length === 0 ? (
                <p className="text-sm font-medium text-gray-500 p-6 text-center">No students on this batch yet.</p>
              ) : (
                <ul className="space-y-1">
                  {students.map((s) => (
                    <li key={s.id} className="flex items-center justify-between p-3 hover:bg-white hover:shadow-sm rounded-xl transition-all border border-transparent hover:border-gray-100">
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="w-9 h-9 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs shrink-0 shadow-inner">
                          {s.name.substring(0, 2).toUpperCase()}
                        </div>
                        <div className="min-w-0">
                          <p className="truncate text-sm font-bold text-gray-900">{s.name}</p>
                          <p className="truncate text-xs font-medium text-gray-500">{s.email}</p>
                        </div>
                      </div>
                      {s.status !== 'active' && (
                        <Badge variant={s.status === 'dropped' ? 'error' : 'warning'} className="text-[10px] font-bold px-2 py-0.5 shadow-sm">
                          {s.status}
                        </Badge>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div className="p-4 border-t border-gray-100 bg-white">
               <Button variant="outline" className="w-full text-sm font-bold text-gray-700 bg-white hover:bg-gray-50 border-gray-200 shadow-sm h-10" onClick={() => { setShowRosterModal(true); setRosterSearch(''); setRosterPage(1); }}>
                  View All Students <ArrowLeft className="w-4 h-4 ml-2 rotate-180" />
               </Button>
            </div>
          </Card>

          {/* Program Progress Card */}
          <Card className="p-6 border-gray-200 shadow-sm rounded-2xl bg-white">
             <h3 className="font-bold text-gray-900 mb-8 text-base">Program Progress</h3>
             <div className="flex justify-center mb-8">
                <CircularProgress 
                  percentage={overallProgress} 
                  label="" 
                  subtext="Overall Progress" 
                  size={160} 
                  strokeWidth={14} 
                  color="text-emerald-500" 
                />
             </div>
             <div className="space-y-3 pt-4 border-t border-gray-100">
                <div className="flex items-center justify-between text-sm p-2 rounded-lg">
                   <div className="flex items-center gap-3 text-gray-600 font-semibold">
                      <CheckCircle className="w-5 h-5 text-emerald-500" />
                      Completed Modules
                   </div>
                   <span className="font-black text-gray-900 text-base">{batch.completed_module_count}</span>
                </div>
                <div className="flex items-center justify-between text-sm p-2 rounded-lg">
                   <div className="flex items-center gap-3 text-gray-600 font-semibold">
                      <Folder className="w-5 h-5 text-amber-500 fill-amber-100" />
                      Pending Modules
                   </div>
                   <span className="font-black text-gray-900 text-base">{Math.max(0, batch.module_count - batch.completed_module_count)}</span>
                </div>
             </div>
          </Card>



        </div>
      </div>
      {/* Roster Modal */}
      {showRosterModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={() => setShowRosterModal(false)}>
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
          <div
            className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden border border-gray-200"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-5 border-b border-gray-100">
              <div>
                <h2 className="text-lg font-bold text-gray-900">All Students</h2>
                <p className="text-sm text-gray-500 mt-0.5">{students.length} student{students.length !== 1 ? 's' : ''} enrolled</p>
              </div>
              <button
                onClick={() => setShowRosterModal(false)}
                className="p-2 hover:bg-gray-100 rounded-xl transition-colors text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Search */}
            <div className="px-5 py-3 border-b border-gray-100 bg-gray-50/50">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by name, email, or phone..."
                  value={rosterSearch}
                  onChange={(e) => { setRosterSearch(e.target.value); setRosterPage(1); }}
                  className="w-full pl-10 pr-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-400 transition-all placeholder:text-gray-400"
                />
              </div>
            </div>

            {/* Student List */}
            <div className="flex-1 overflow-y-auto p-3">
              {(() => {
                const filtered = students.filter((s) => {
                  const q = rosterSearch.toLowerCase();
                  return (
                    s.name.toLowerCase().includes(q) ||
                    (s.email && s.email.toLowerCase().includes(q)) ||
                    (s.phone && s.phone.toLowerCase().includes(q)) ||
                    (s.roll_no && s.roll_no.toLowerCase().includes(q))
                  );
                });
                const totalPages = Math.max(1, Math.ceil(filtered.length / ROSTER_PAGE_SIZE));
                const safePage = Math.min(rosterPage, totalPages);
                const paged = filtered.slice((safePage - 1) * ROSTER_PAGE_SIZE, safePage * ROSTER_PAGE_SIZE);

                if (filtered.length === 0) {
                  return (
                    <div className="flex flex-col items-center justify-center py-12 text-gray-400">
                      <Users className="w-10 h-10 mb-3" />
                      <p className="text-sm font-semibold">No students found</p>
                      <p className="text-xs mt-1">Try a different search term</p>
                    </div>
                  );
                }

                return (
                  <>
                    <ul className="space-y-1">
                      {paged.map((s, idx) => (
                        <li
                          key={s.id}
                          className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition-all border border-transparent hover:border-gray-100 group"
                        >
                          <div className="flex items-center gap-3 min-w-0">
                            <div className="relative">
                              <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs shrink-0 shadow-inner">
                                {s.name.substring(0, 2).toUpperCase()}
                              </div>
                              <div className={`absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white ${
                                s.status === 'active' ? 'bg-emerald-400' :
                                s.status === 'dropped' ? 'bg-red-400' : 'bg-amber-400'
                              }`} />
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center gap-2">
                                <p className="truncate text-sm font-bold text-gray-900">{s.name}</p>
                                {s.roll_no && (
                                  <span className="text-[10px] font-semibold text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">{s.roll_no}</span>
                                )}
                              </div>
                              <div className="flex items-center gap-3 mt-0.5">
                                {s.email && (
                                  <span className="flex items-center gap-1 text-xs text-gray-500 truncate">
                                    <Mail className="w-3 h-3 shrink-0" />{s.email}
                                  </span>
                                )}
                                {s.phone && (
                                  <span className="flex items-center gap-1 text-xs text-gray-500">
                                    <Phone className="w-3 h-3 shrink-0" />{s.phone}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                          <Badge
                            variant={s.status === 'active' ? 'success' : s.status === 'dropped' ? 'error' : 'warning'}
                            className="text-[10px] font-bold px-2 py-0.5 shadow-sm capitalize"
                          >
                            {s.status || 'active'}
                          </Badge>
                        </li>
                      ))}
                    </ul>

                    {/* Pagination */}
                    {totalPages > 1 && (
                      <div className="flex items-center justify-between pt-4 px-2 mt-2 border-t border-gray-100">
                        <p className="text-xs text-gray-500 font-medium">
                          Showing {(safePage - 1) * ROSTER_PAGE_SIZE + 1}–{Math.min(safePage * ROSTER_PAGE_SIZE, filtered.length)} of {filtered.length}
                        </p>
                        <div className="flex items-center gap-1">
                          <button
                            disabled={safePage <= 1}
                            onClick={() => setRosterPage((p) => Math.max(1, p - 1))}
                            className="p-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                          >
                            <ChevronLeft className="w-4 h-4" />
                          </button>
                          {Array.from({ length: totalPages }, (_, i) => i + 1).map((pg) => (
                            <button
                              key={pg}
                              onClick={() => setRosterPage(pg)}
                              className={`w-8 h-8 rounded-lg text-xs font-bold transition-colors ${
                                pg === safePage
                                  ? 'bg-emerald-500 text-white shadow-sm'
                                  : 'text-gray-600 hover:bg-gray-100'
                              }`}
                            >
                              {pg}
                            </button>
                          ))}
                          <button
                            disabled={safePage >= totalPages}
                            onClick={() => setRosterPage((p) => Math.min(totalPages, p + 1))}
                            className="p-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                          >
                            <ChevronRight className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    )}
                  </>
                );
              })()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
