'use client';

import { use, useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowUp, ArrowDown, Plus, Pencil, Trash2, Layers } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Input } from '@/components/ui/Input';
import { FormField } from '@/components/ui/FormField';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { PageLoader } from '@/components/ui/Spinner';
import { TrainingProgramForm } from '@/components/training/TrainingProgramForm';
import { slugify } from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import type { TrainingModule, TrainingProgramDetail } from '@/types/training';

export default function TrainingProgramDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const programId = Number(id);
  const router = useRouter();

  const [program, setProgram] = useState<TrainingProgramDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<'modules' | 'settings'>('modules');

  const [addOpen, setAddOpen] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newSlug, setNewSlug] = useState('');
  const [adding, setAdding] = useState(false);
  const [deleting, setDeleting] = useState<TrainingModule | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setProgram(await trainingService.getProgram(programId));
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load programme');
      router.push('/training');
    } finally {
      setLoading(false);
    }
  }, [programId, router]);

  useEffect(() => {
    void load();
  }, [load]);

  const move = async (index: number, direction: -1 | 1) => {
    if (!program) return;
    const modules = [...program.modules];
    const target = index + direction;
    if (target < 0 || target >= modules.length) return;

    [modules[index], modules[target]] = [modules[target], modules[index]];
    // Optimistic: the list reorders instantly, then we persist the whole ordering.
    setProgram({ ...program, modules });

    try {
      await trainingService.reorderModules(
        programId,
        modules.map((m, i) => ({ id: m.id, display_order: i + 1 }))
      );
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not reorder');
      void load();
    }
  };

  const addModule = async () => {
    if (!newTitle.trim()) return;
    setAdding(true);
    try {
      await trainingService.createModule(programId, {
        title: newTitle.trim(),
        slug: newSlug.trim() || slugify(newTitle),
      });
      toast.success('Module added');
      setAddOpen(false);
      setNewTitle('');
      setNewSlug('');
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not add module');
    } finally {
      setAdding(false);
    }
  };

  const deleteModule = async () => {
    if (!deleting) return;
    try {
      await trainingService.deleteModule(deleting.id);
      toast.success('Module deleted');
      setDeleting(null);
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not delete module');
    }
  };

  if (loading || !program) return <PageLoader />;

  return (
    <div>
      <PageHeader
        title={program.title}
        description={program.summary || `/${program.slug}`}
        actions={
          <Badge variant={program.status === 'published' ? 'success' : 'warning'}>
            {program.status}
          </Badge>
        }
      />

      <div className="mb-6 flex gap-1 border-b border-gray-200">
        {(['modules', 'settings'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={
              tab === t
                ? 'border-b-2 border-teal-600 px-4 py-2 text-sm font-medium text-teal-700'
                : 'px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700'
            }
          >
            {t === 'modules' ? `Modules (${program.modules.length})` : 'Settings'}
          </button>
        ))}
      </div>

      {tab === 'settings' ? (
        <TrainingProgramForm program={program} />
      ) : (
        <div>
          <div className="mb-4 flex justify-end">
            <Button onClick={() => setAddOpen(true)}>
              <Plus className="mr-1 h-4 w-4" />
              Add module
            </Button>
          </div>

          {program.modules.length === 0 ? (
            <Card className="p-12 text-center">
              <Layers className="mx-auto h-10 w-10 text-gray-300" />
              <p className="mt-3 text-sm font-medium text-gray-900">No modules yet</p>
              <p className="mt-1 text-sm text-gray-500">
                A module is roughly one lecture. Add one, then fill it with assets.
              </p>
              <Button className="mt-4" onClick={() => setAddOpen(true)}>
                <Plus className="mr-1 h-4 w-4" />
                Add the first module
              </Button>
            </Card>
          ) : (
            <div className="space-y-2">
              {program.modules.map((module, index) => (
                <Card key={module.id} className="flex items-center gap-4 p-4">
                  <div className="flex flex-col">
                    {/* Buttons rather than drag-and-drop: no dnd library in this app,
                        and adding one for this is not worth the dependency. */}
                    <button
                      onClick={() => move(index, -1)}
                      disabled={index === 0}
                      className="rounded p-0.5 text-gray-400 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-30 disabled:hover:bg-transparent"
                      aria-label="Move up"
                    >
                      <ArrowUp className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => move(index, 1)}
                      disabled={index === program.modules.length - 1}
                      className="rounded p-0.5 text-gray-400 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-30 disabled:hover:bg-transparent"
                      aria-label="Move down"
                    >
                      <ArrowDown className="h-4 w-4" />
                    </button>
                  </div>

                  <span className="w-6 text-sm font-semibold text-gray-400">{index + 1}</span>

                  <Link
                    href={`/training/${programId}/modules/${module.id}`}
                    className="min-w-0 flex-1"
                  >
                    <p className="truncate font-medium text-gray-900 hover:text-teal-700">
                      {module.title}
                    </p>
                    <p className="text-xs text-gray-500">
                      {module.asset_count} asset{module.asset_count === 1 ? '' : 's'}
                      {module.estimated_minutes ? ` · ${module.estimated_minutes} min` : ''}
                    </p>
                  </Link>

                  <Badge variant={module.status === 'published' ? 'success' : 'warning'}>
                    {module.status}
                  </Badge>

                  <div className="flex gap-1">
                    <Link href={`/training/${programId}/modules/${module.id}`}>
                      <Button variant="ghost" size="icon" aria-label="Edit module">
                        <Pencil className="h-4 w-4" />
                      </Button>
                    </Link>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setDeleting(module)}
                      aria-label="Delete module"
                    >
                      <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      <Modal isOpen={addOpen} onClose={() => setAddOpen(false)} title="Add a module">
        <div className="space-y-4">
          <FormField label="Title" required>
            <Input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Introduction to Python"
              autoFocus
            />
          </FormField>
          <FormField label="Slug" description="Leave blank to generate from the title">
            <Input
              value={newSlug}
              onChange={(e) => setNewSlug(e.target.value)}
              placeholder={slugify(newTitle) || 'introduction-to-python'}
            />
          </FormField>
          <div className="flex justify-end gap-3">
            <Button variant="outline" onClick={() => setAddOpen(false)}>
              Cancel
            </Button>
            <Button onClick={addModule} disabled={adding || !newTitle.trim()}>
              {adding ? 'Adding…' : 'Add module'}
            </Button>
          </div>
        </div>
      </Modal>

      <ConfirmModal
        isOpen={!!deleting}
        onClose={() => setDeleting(null)}
        onConfirm={deleteModule}
        title="Delete this module?"
        description={`"${deleting?.title}" will be removed. Its assets stay in the library and remain available to other modules.`}
        confirmText="Delete"
      />
    </div>
  );
}
