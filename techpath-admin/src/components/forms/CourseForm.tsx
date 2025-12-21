'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Plus, X, GraduationCap } from 'lucide-react';
import { courseSchema, type CourseFormData } from '@/lib/validations';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Switch } from '@/components/ui/Switch';
import { FormField } from '@/components/ui/FormField';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { MarkdownEditor } from '@/components/editors/MarkdownEditor';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { slugify } from '@/lib/utils/format';
import { courseService } from '@/services/course.service';
import type { Course, CourseCategory, Skill, CourseCategoryTree } from '@/types/api';

interface CourseFormProps {
  initialData?: Course;
  onSubmit: (data: CourseFormData) => Promise<void>;
  isLoading?: boolean;
}

export function CourseForm({ initialData, onSubmit, isLoading }: CourseFormProps) {
  const [categories, setCategories] = useState<CourseCategoryTree[]>([]);
  const [flatCategories, setFlatCategories] = useState<Array<{ id: number; name: string }>>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [selectedSkills, setSelectedSkills] = useState<number[]>(
    initialData?.skills.map((s) => s.id) || []
  );
  const [learningOutcomes, setLearningOutcomes] = useState<string[]>(
    initialData?.learning_outcomes || []
  );
  const [prerequisites, setPrerequisites] = useState<string[]>(
    initialData?.prerequisites || []
  );
  const [newOutcome, setNewOutcome] = useState('');
  const [newPrereq, setNewPrereq] = useState('');

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<CourseFormData>({
    resolver: zodResolver(courseSchema),
    defaultValues: {
      title: initialData?.title || '',
      slug: initialData?.slug || '',
      short_description: initialData?.short_description || '',
      description: initialData?.description || '',
      category_id: initialData?.category_id || 0,
      price: initialData?.price || 0,
      original_price: initialData?.original_price || undefined,
      emi_available: initialData?.emi_available ?? true,
      emi_amount: initialData?.emi_amount || undefined,
      currency: initialData?.currency || 'INR',
      duration: initialData?.duration || '',
      duration_hours: initialData?.duration_hours || undefined,
      batch_size: initialData?.batch_size || 20,
      level: initialData?.level || 'beginner',
      rating: initialData?.rating || 0,
      review_count: initialData?.review_count || 0,
      enrollment_count: initialData?.enrollment_count || 0,
      placement_rate: initialData?.placement_rate || undefined,
      featured_image: initialData?.featured_image || '',
      video_url: initialData?.video_url || '',
      instructor_name: initialData?.instructor_name || '',
      instructor_title: initialData?.instructor_title || '',
      instructor_bio: initialData?.instructor_bio || '',
      instructor_image: initialData?.instructor_image || '',
      certification_name: initialData?.certification_name || '',
      certification_authority: initialData?.certification_authority || '',
      meta_title: initialData?.meta_title || '',
      meta_description: initialData?.meta_description || '',
      next_batch_date: initialData?.next_batch_date || '',
      status: initialData?.status || 'draft',
      featured: initialData?.featured ?? false,
      is_active: initialData?.is_active ?? true,
      skill_ids: initialData?.skills.map((s) => s.id) || [],
      learning_outcomes: initialData?.learning_outcomes || [],
      prerequisites: initialData?.prerequisites || [],
    },
  });

  const title = watch('title');
  const description = watch('description');
  const status = watch('status');
  const isFeatured = watch('featured');
  const isActive = watch('is_active');
  const emiAvailable = watch('emi_available');
  const featuredImage = watch('featured_image');
  const instructorImage = watch('instructor_image');
  const categoryId = watch('category_id');

  useEffect(() => {
    async function fetchData() {
      try {
        const [categoriesData, skillsData] = await Promise.all([
          courseService.getCategoryTree(false),
          courseService.listSkills(),
        ]);
        setCategories(categoriesData);
        setSkills(skillsData);

        // Flatten categories for select dropdown
        const flattened = courseService.flattenCategoryTree(categoriesData);
        setFlatCategories(flattened.map((c) => ({ id: c.id, name: c.fullPath })));

        // Set default category if creating new course
        if (!initialData && categoriesData.length > 0 && flattened.length > 0) {
          setValue('category_id', flattened[0].id);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    fetchData();
  }, [initialData, setValue]);

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = e.target.value;
    setValue('title', newTitle);
    if (!initialData) {
      setValue('slug', slugify(newTitle));
    }
  };

  const handleSkillToggle = (skillId: number) => {
    const newSkills = selectedSkills.includes(skillId)
      ? selectedSkills.filter((id) => id !== skillId)
      : [...selectedSkills, skillId];
    setSelectedSkills(newSkills);
    setValue('skill_ids', newSkills);
  };

  const addLearningOutcome = () => {
    if (newOutcome.trim()) {
      const updated = [...learningOutcomes, newOutcome.trim()];
      setLearningOutcomes(updated);
      setValue('learning_outcomes', updated);
      setNewOutcome('');
    }
  };

  const removeLearningOutcome = (index: number) => {
    const updated = learningOutcomes.filter((_, i) => i !== index);
    setLearningOutcomes(updated);
    setValue('learning_outcomes', updated);
  };

  const addPrerequisite = () => {
    if (newPrereq.trim()) {
      const updated = [...prerequisites, newPrereq.trim()];
      setPrerequisites(updated);
      setValue('prerequisites', updated);
      setNewPrereq('');
    }
  };

  const removePrerequisite = (index: number) => {
    const updated = prerequisites.filter((_, i) => i !== index);
    setPrerequisites(updated);
    setValue('prerequisites', updated);
  };

  const handleFormSubmit = async (data: CourseFormData) => {
    await onSubmit({
      ...data,
      skill_ids: selectedSkills,
      learning_outcomes: learningOutcomes,
      prerequisites: prerequisites,
    });
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Course Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField label="Title" htmlFor="title" error={errors.title?.message} required>
                <Input
                  id="title"
                  {...register('title')}
                  onChange={handleTitleChange}
                  error={!!errors.title}
                  placeholder="e.g., AI/ML Engineering Bootcamp"
                />
              </FormField>

              <FormField label="Slug" htmlFor="slug" error={errors.slug?.message}>
                <Input
                  id="slug"
                  {...register('slug')}
                  error={!!errors.slug}
                  placeholder="ai-ml-bootcamp"
                />
              </FormField>

              <div className="grid grid-cols-2 gap-4">
                <FormField label="Category" htmlFor="category_id" error={errors.category_id?.message} required>
                  <Select
                    id="category_id"
                    {...register('category_id', { valueAsNumber: true })}
                    error={!!errors.category_id}
                    value={categoryId}
                    onChange={(e) => setValue('category_id', Number(e.target.value))}
                  >
                    {flatCategories.length === 0 && <option value="">No Categories</option>}
                    {flatCategories.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.name}
                      </option>
                    ))}
                  </Select>
                </FormField>

                <FormField label="Level" htmlFor="level" error={errors.level?.message}>
                  <Select id="level" {...register('level')} error={!!errors.level}>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </Select>
                </FormField>
              </div>

              <FormField label="Short Description" htmlFor="short_description" error={errors.short_description?.message}>
                <Textarea
                  id="short_description"
                  {...register('short_description')}
                  error={!!errors.short_description}
                  placeholder="Brief course summary (max 500 chars)"
                  rows={2}
                />
              </FormField>

              <FormField label="Full Description" htmlFor="description" error={errors.description?.message} required>
                <MarkdownEditor
                  content={description}
                  onChange={(c) => setValue('description', c)}
                  error={!!errors.description}
                  placeholder="Write detailed course description..."
                  minHeight="300px"
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Pricing & Duration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <FormField label="Price" htmlFor="price" error={errors.price?.message} required>
                  <Input
                    id="price"
                    type="number"
                    {...register('price', { valueAsNumber: true })}
                    error={!!errors.price}
                    placeholder="24999"
                  />
                </FormField>

                <FormField label="Original Price" htmlFor="original_price">
                  <Input
                    id="original_price"
                    type="number"
                    {...register('original_price', { valueAsNumber: true })}
                    placeholder="39999"
                  />
                </FormField>

                <FormField label="Currency" htmlFor="currency">
                  <Select id="currency" {...register('currency')}>
                    <option value="INR">INR</option>
                    <option value="USD">USD</option>
                  </Select>
                </FormField>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Switch
                  checked={emiAvailable}
                  onChange={(checked) => setValue('emi_available', checked)}
                  label="EMI Available"
                />
                {emiAvailable && (
                  <FormField label="EMI Amount" htmlFor="emi_amount">
                    <Input
                      id="emi_amount"
                      type="number"
                      {...register('emi_amount', { valueAsNumber: true })}
                      placeholder="2999"
                    />
                  </FormField>
                )}
              </div>

              <div className="grid grid-cols-3 gap-4">
                <FormField label="Duration" htmlFor="duration" error={errors.duration?.message} required>
                  <Input
                    id="duration"
                    {...register('duration')}
                    error={!!errors.duration}
                    placeholder="4 months"
                  />
                </FormField>

                <FormField label="Duration (Hours)" htmlFor="duration_hours">
                  <Input
                    id="duration_hours"
                    type="number"
                    {...register('duration_hours', { valueAsNumber: true })}
                    placeholder="120"
                  />
                </FormField>

                <FormField label="Batch Size" htmlFor="batch_size">
                  <Input
                    id="batch_size"
                    type="number"
                    {...register('batch_size', { valueAsNumber: true })}
                    placeholder="20"
                  />
                </FormField>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Stats & Ratings</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-4">
                <FormField label="Rating (0-5)" htmlFor="rating">
                  <Input
                    id="rating"
                    type="number"
                    step="0.1"
                    min="0"
                    max="5"
                    {...register('rating', { valueAsNumber: true })}
                    placeholder="4.9"
                  />
                </FormField>

                <FormField label="Reviews" htmlFor="review_count">
                  <Input
                    id="review_count"
                    type="number"
                    {...register('review_count', { valueAsNumber: true })}
                    placeholder="456"
                  />
                </FormField>

                <FormField label="Enrollments" htmlFor="enrollment_count">
                  <Input
                    id="enrollment_count"
                    type="number"
                    {...register('enrollment_count', { valueAsNumber: true })}
                    placeholder="1200"
                  />
                </FormField>

                <FormField label="Placement %" htmlFor="placement_rate">
                  <Input
                    id="placement_rate"
                    type="number"
                    min="0"
                    max="100"
                    {...register('placement_rate', { valueAsNumber: true })}
                    placeholder="94"
                  />
                </FormField>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Instructor</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <FormField label="Instructor Name" htmlFor="instructor_name">
                  <Input id="instructor_name" {...register('instructor_name')} placeholder="John Doe" />
                </FormField>

                <FormField label="Instructor Title" htmlFor="instructor_title">
                  <Input id="instructor_title" {...register('instructor_title')} placeholder="Senior AI Engineer at Google" />
                </FormField>
              </div>

              <FormField label="Instructor Bio" htmlFor="instructor_bio">
                <Textarea
                  id="instructor_bio"
                  {...register('instructor_bio')}
                  placeholder="Brief bio about the instructor..."
                  rows={3}
                />
              </FormField>

              <FormField label="Instructor Image" htmlFor="instructor_image">
                <ImageUpload
                  value={instructorImage}
                  onChange={(url) => setValue('instructor_image', url)}
                  folder="courses/instructors"
                  placeholder="Upload instructor photo"
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Learning Outcomes</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                {learningOutcomes.map((outcome, index) => (
                  <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <span className="flex-1 text-sm">{outcome}</span>
                    <button
                      type="button"
                      onClick={() => removeLearningOutcome(index)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <Input
                  value={newOutcome}
                  onChange={(e) => setNewOutcome(e.target.value)}
                  placeholder="Add learning outcome..."
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addLearningOutcome())}
                />
                <Button type="button" variant="outline" onClick={addLearningOutcome}>
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Prerequisites</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                {prerequisites.map((prereq, index) => (
                  <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <span className="flex-1 text-sm">{prereq}</span>
                    <button
                      type="button"
                      onClick={() => removePrerequisite(index)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <Input
                  value={newPrereq}
                  onChange={(e) => setNewPrereq(e.target.value)}
                  placeholder="Add prerequisite..."
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addPrerequisite())}
                />
                <Button type="button" variant="outline" onClick={addPrerequisite}>
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Publish Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField label="Status" htmlFor="status" error={errors.status?.message}>
                <Select id="status" {...register('status')} error={!!errors.status}>
                  <option value="draft">Draft</option>
                  <option value="published">Published</option>
                  <option value="archived">Archived</option>
                </Select>
              </FormField>

              <Switch
                checked={isFeatured}
                onChange={(checked) => setValue('featured', checked)}
                label="Featured Course"
              />

              <Switch
                checked={isActive}
                onChange={(checked) => setValue('is_active', checked)}
                label="Active"
                description="Inactive courses won't show on frontend"
              />

              <FormField label="Next Batch Date" htmlFor="next_batch_date">
                <Input
                  id="next_batch_date"
                  type="datetime-local"
                  {...register('next_batch_date')}
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Featured Image</CardTitle>
            </CardHeader>
            <CardContent>
              <ImageUpload
                value={featuredImage}
                onChange={(url) => setValue('featured_image', url)}
                folder="courses"
                error={!!errors.featured_image}
                placeholder="Upload course image"
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Video URL</CardTitle>
            </CardHeader>
            <CardContent>
              <FormField label="Intro Video URL" htmlFor="video_url" error={errors.video_url?.message}>
                <Input
                  id="video_url"
                  {...register('video_url')}
                  placeholder="https://youtube.com/watch?v=..."
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Skills / Tags</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {skills.map((skill) => (
                  <button
                    key={skill.id}
                    type="button"
                    onClick={() => handleSkillToggle(skill.id)}
                    className={`rounded-full px-3 py-1 text-sm transition-colors ${
                      selectedSkills.includes(skill.id)
                        ? 'bg-teal-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {skill.name}
                  </button>
                ))}
                {skills.length === 0 && <p className="text-sm text-gray-500">No skills available</p>}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Certification</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField label="Certificate Name" htmlFor="certification_name">
                <Input
                  id="certification_name"
                  {...register('certification_name')}
                  placeholder="AI/ML Professional"
                />
              </FormField>
              <FormField label="Issuing Authority" htmlFor="certification_authority">
                <Input
                  id="certification_authority"
                  {...register('certification_authority')}
                  placeholder="TechPath Academy"
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>SEO Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField label="Meta Title" htmlFor="meta_title" error={errors.meta_title?.message}>
                <Input
                  id="meta_title"
                  {...register('meta_title')}
                  placeholder="SEO title (max 70 chars)"
                />
              </FormField>
              <FormField label="Meta Description" htmlFor="meta_description" error={errors.meta_description?.message}>
                <Textarea
                  id="meta_description"
                  {...register('meta_description')}
                  placeholder="SEO description (max 160 chars)"
                  rows={3}
                />
              </FormField>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Button type="submit" className="w-full" loading={isLoading}>
                {initialData ? 'Update Course' : 'Create Course'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </form>
  );
}

