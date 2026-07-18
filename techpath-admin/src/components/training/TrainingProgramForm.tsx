'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { FormField } from '@/components/ui/FormField';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { slugify } from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import { courseService } from '@/services/course.service';
import type { DeliveryMode, TrainingProgram } from '@/types/training';

interface TrainingProgramFormProps {
  program?: TrainingProgram;
}

interface CourseOption {
  id: number;
  title: string;
}

export function TrainingProgramForm({ program }: TrainingProgramFormProps) {
  const router = useRouter();
  const isEdit = !!program;

  const [title, setTitle] = useState(program?.title ?? '');
  const [slug, setSlug] = useState(program?.slug ?? '');
  const [slugTouched, setSlugTouched] = useState(isEdit);
  const [summary, setSummary] = useState(program?.summary ?? '');
  const [description, setDescription] = useState(program?.description ?? '');
  const [courseId, setCourseId] = useState<string>(
    program?.course_id != null ? String(program.course_id) : ''
  );
  const [deliveryMode, setDeliveryMode] = useState<DeliveryMode>(
    program?.delivery_mode ?? 'offline'
  );
  const [level, setLevel] = useState(program?.level ?? '');
  const [duration, setDuration] = useState(program?.duration ?? '');
  const [tags, setTags] = useState((program?.tags ?? []).join(', '));
  const [status, setStatus] = useState(program?.status ?? 'draft');

  const [courses, setCourses] = useState<CourseOption[]>([]);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    courseService
      .list({ limit: 100 })
      .then((result) =>
        setCourses(result.items.map((c) => ({ id: c.id, title: c.title })))
      )
      .catch(() => {
        // Linking a course is optional, so a failure here shouldn't block authoring.
        setCourses([]);
      });
  }, []);

  // Auto-slug from the title until the user takes over.
  useEffect(() => {
    if (!slugTouched) setSlug(slugify(title));
  }, [title, slugTouched]);

  const validate = () => {
    const next: Record<string, string> = {};
    if (!title.trim()) next.title = 'Give the programme a title';
    if (!slug.trim()) next.slug = 'A slug is required';
    else if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug))
      next.slug = 'Use lowercase letters, numbers and hyphens only';
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    const payload = {
      title: title.trim(),
      slug: slug.trim(),
      summary: summary.trim() || undefined,
      description: description.trim() || undefined,
      course_id: courseId ? Number(courseId) : null,
      delivery_mode: deliveryMode,
      level: level || undefined,
      duration: duration.trim() || undefined,
      tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
      status,
    };

    setSaving(true);
    try {
      if (isEdit) {
        await trainingService.updateProgram(program.id, payload);
        toast.success('Programme updated');
        router.push(`/training/${program.id}`);
      } else {
        const created = await trainingService.createProgram(payload);
        toast.success('Programme created');
        router.push(`/training/${created.id}`);
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not save');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card className="p-6">
        <div className="space-y-4">
          <FormField label="Title" required error={errors.title}>
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Python Fundamentals"
              error={!!errors.title}
            />
          </FormField>

          <FormField label="Slug" required error={errors.slug}>
            <Input
              value={slug}
              onChange={(e) => {
                setSlugTouched(true);
                setSlug(e.target.value);
              }}
              placeholder="python-fundamentals"
              error={!!errors.slug}
            />
          </FormField>

          <FormField label="Summary" description="One line, shown in listings">
            <Input value={summary} onChange={(e) => setSummary(e.target.value)} />
          </FormField>

          <FormField label="Description">
            <Textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={5}
            />
          </FormField>
        </div>
      </Card>

      <Card className="p-6">
        <h2 className="mb-4 text-sm font-semibold text-gray-900">Delivery</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <FormField
            label="Linked course"
            description="Optional — leave blank for offline-only training with no public course page"
          >
            <Select value={courseId} onChange={(e) => setCourseId(e.target.value)}>
              <option value="">No linked course (standalone)</option>
              {courses.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </Select>
          </FormField>

          <FormField label="Delivery mode">
            <Select
              value={deliveryMode}
              onChange={(e) => setDeliveryMode(e.target.value as DeliveryMode)}
            >
              <option value="offline">Offline</option>
              <option value="online">Online</option>
              <option value="hybrid">Hybrid</option>
            </Select>
          </FormField>

          <FormField label="Level">
            <Select value={level} onChange={(e) => setLevel(e.target.value)}>
              <option value="">Not set</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </Select>
          </FormField>

          <FormField label="Duration">
            <Input
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              placeholder="8 weeks"
            />
          </FormField>

          <FormField label="Tags" description="Comma separated">
            <Input
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="python, beginner"
            />
          </FormField>

          <FormField label="Status">
            <Select value={status} onChange={(e) => setStatus(e.target.value as never)}>
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="archived">Archived</option>
            </Select>
          </FormField>
        </div>
      </Card>

      <div className="flex justify-end gap-3">
        <Button type="button" variant="outline" onClick={() => router.back()}>
          Cancel
        </Button>
        <Button type="submit" disabled={saving}>
          {saving ? 'Saving…' : isEdit ? 'Save changes' : 'Create program'}
        </Button>
      </div>
    </form>
  );
}
