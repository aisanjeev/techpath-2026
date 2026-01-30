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
import type { Course, CourseCategory, Skill, CourseCategoryTree, CurriculumModule, ProjectItem, FAQItem } from '@/types/api';

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
  const [curriculum, setCurriculum] = useState<CurriculumModule[]>(initialData?.curriculum || []);
  const [projects, setProjects] = useState<ProjectItem[]>(initialData?.projects || []);
  const [faqs, setFaqs] = useState<FAQItem[]>(initialData?.faqs || []);
  const [newTopicByModule, setNewTopicByModule] = useState<Record<number, string>>({});
  const [newSkillName, setNewSkillName] = useState('');
  const [addingSkill, setAddingSkill] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    getValues,
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
      curriculum: initialData?.curriculum || [],
      projects: initialData?.projects || [],
      faqs: initialData?.faqs || [],
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

  const addNewSkill = async () => {
    const name = newSkillName.trim();
    if (!name) return;
    setAddingSkill(true);
    try {
      const slug = slugify(name);
      const newSkill = await courseService.createSkill({ name, slug });
      setSkills((prev) => (prev.some((s) => s.id === newSkill.id) ? prev : [...prev, newSkill]));
      const nextIds = selectedSkills.includes(newSkill.id)
        ? selectedSkills
        : [...selectedSkills, newSkill.id];
      setSelectedSkills(nextIds);
      setValue('skill_ids', nextIds);
      setNewSkillName('');
    } catch (error) {
      console.error('Error creating skill:', error);
      const err = error as { response?: { status?: number } };
      if (err.response?.status === 409) {
        const existing = skills.find((s) => s.slug === slugify(name));
        if (existing) {
          const nextIds = selectedSkills.includes(existing.id)
            ? selectedSkills
            : [...selectedSkills, existing.id];
          setSelectedSkills(nextIds);
          setValue('skill_ids', nextIds);
          setNewSkillName('');
        }
      }
    } finally {
      setAddingSkill(false);
    }
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

  const addCurriculumModule = () => {
    const updated = [...curriculum, { title: '', topics: [] }];
    setCurriculum(updated);
    setValue('curriculum', updated);
  };

  const updateCurriculumModule = (index: number, field: 'title' | 'duration', value: string) => {
    const updated = curriculum.map((m, i) =>
      i === index ? { ...m, [field]: value } : m
    );
    setCurriculum(updated);
    setValue('curriculum', updated);
  };

  const updateCurriculumTopics = (moduleIndex: number, topics: string[]) => {
    setCurriculum((prev) => {
      const updated = prev.map((m, i) =>
        i === moduleIndex ? { ...m, topics } : m
      );
      setValue('curriculum', updated);
      return updated;
    });
  };

  const addTopicToModule = (moduleIndex: number, topic: string) => {
    if (!topic.trim()) return;
    setCurriculum((prev) => {
      const mod = prev[moduleIndex];
      const topics = [...(mod?.topics || []), topic.trim()];
      const updated = prev.map((m, i) =>
        i === moduleIndex ? { ...m, topics } : m
      );
      setValue('curriculum', updated);
      return updated;
    });
  };

  const removeTopicFromModule = (moduleIndex: number, topicIndex: number) => {
    setCurriculum((prev) => {
      const mod = prev[moduleIndex];
      const topics = (mod?.topics || []).filter((_, i) => i !== topicIndex);
      const updated = prev.map((m, i) =>
        i === moduleIndex ? { ...m, topics } : m
      );
      setValue('curriculum', updated);
      return updated;
    });
  };

  const removeCurriculumModule = (index: number) => {
    const updated = curriculum.filter((_, i) => i !== index);
    setCurriculum(updated);
    setValue('curriculum', updated);
  };

  const addProject = () => {
    const updated = [...projects, { title: '' }];
    setProjects(updated);
    setValue('projects', updated);
  };

  const updateProject = (index: number, field: 'title' | 'description', value: string) => {
    const updated = projects.map((p, i) =>
      i === index ? { ...p, [field]: value } : p
    );
    setProjects(updated);
    setValue('projects', updated);
  };

  const removeProject = (index: number) => {
    const updated = projects.filter((_, i) => i !== index);
    setProjects(updated);
    setValue('projects', updated);
  };

  const addFaq = () => {
    const updated = [...faqs, { question: '', answer: '' }];
    setFaqs(updated);
    setValue('faqs', updated);
  };
  const updateFaq = (index: number, field: 'question' | 'answer', value: string) => {
    const updated = faqs.map((f, i) =>
      i === index ? { ...f, [field]: value } : f
    );
    setFaqs(updated);
    setValue('faqs', updated);
  };
  const removeFaq = (index: number) => {
    const updated = faqs.filter((_, i) => i !== index);
    setFaqs(updated);
    setValue('faqs', updated);
  };

  const handleFormSubmit = async (data: CourseFormData) => {
    // Use form values (kept in sync via setValue) so we get latest curriculum/projects/faqs including topics
    const formCurriculum = getValues('curriculum') ?? curriculum;
    const formProjects = getValues('projects') ?? projects;
    const formFaqs = getValues('faqs') ?? faqs;
    const curriculumPayload = (Array.isArray(formCurriculum) ? formCurriculum : curriculum)
      .filter((m: CurriculumModule) => m?.title?.trim())
      .map((m: CurriculumModule) => ({
        title: (m.title || '').trim(),
        topics: Array.isArray(m.topics) ? m.topics : [],
        duration: m.duration?.trim() || undefined,
      }));
    const projectsPayload = (Array.isArray(formProjects) ? formProjects : projects)
      .filter((p: ProjectItem) => p?.title?.trim())
      .map((p: ProjectItem) => ({
        title: (p.title || '').trim(),
        description: p.description?.trim() || undefined,
      }));
    const faqsPayload = (Array.isArray(formFaqs) ? formFaqs : faqs)
      .filter((f: FAQItem) => f?.question?.trim() && f?.answer?.trim())
      .map((f: FAQItem) => ({
        question: (f.question || '').trim(),
        answer: (f.answer || '').trim(),
      }));
    await onSubmit({
      ...data,
      skill_ids: selectedSkills,
      learning_outcomes: learningOutcomes,
      prerequisites: prerequisites,
      curriculum: curriculumPayload,
      projects: projectsPayload,
      faqs: faqsPayload,
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

          <Card>
            <CardHeader>
              <CardTitle>Curriculum (Modules)</CardTitle>
              <p className="text-sm text-gray-500 mt-1">Add modules with title, topics, and optional duration.</p>
            </CardHeader>
            <CardContent className="space-y-4">
              {curriculum.map((module, modIndex) => (
                <div key={modIndex} className="rounded-lg border border-gray-200 bg-gray-50/50 p-4 space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <Input
                      value={module.title}
                      onChange={(e) => updateCurriculumModule(modIndex, 'title', e.target.value)}
                      placeholder="Module title (e.g. Introduction to Python)"
                      className="flex-1"
                    />
                    <Input
                      value={module.duration || ''}
                      onChange={(e) => updateCurriculumModule(modIndex, 'duration', e.target.value)}
                      placeholder="Duration (e.g. 1 week)"
                      className="w-28"
                    />
                    <button
                      type="button"
                      onClick={() => removeCurriculumModule(modIndex)}
                      className="text-red-500 hover:text-red-700 p-1"
                      title="Remove module"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="space-y-2">
                    <span className="text-xs font-medium text-gray-600">Topics</span>
                    <div className="flex flex-wrap gap-2">
                      {(module.topics || []).map((topic, topicIndex) => (
                        <span
                          key={topicIndex}
                          className="inline-flex items-center gap-1 rounded-full bg-teal-100 px-2 py-0.5 text-sm text-teal-800"
                        >
                          {topic}
                          <button
                            type="button"
                            onClick={() => removeTopicFromModule(modIndex, topicIndex)}
                            className="hover:text-teal-600"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </span>
                      ))}
                    </div>
                    <div className="flex gap-2">
                      <Input
                        value={newTopicByModule[modIndex] ?? ''}
                        onChange={(e) => setNewTopicByModule((prev) => ({ ...prev, [modIndex]: e.target.value }))}
                        placeholder="Add topic, press Enter"
                        className="flex-1"
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            const v = newTopicByModule[modIndex]?.trim();
                            if (v) {
                              addTopicToModule(modIndex, v);
                              setNewTopicByModule((prev) => ({ ...prev, [modIndex]: '' }));
                            }
                          }
                        }}
                      />
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => {
                          const v = newTopicByModule[modIndex]?.trim();
                          if (v) {
                            addTopicToModule(modIndex, v);
                            setNewTopicByModule((prev) => ({ ...prev, [modIndex]: '' }));
                          }
                        }}
                      >
                        <Plus className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
              <Button type="button" variant="outline" onClick={addCurriculumModule} className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add Module
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Frequently Asked Questions</CardTitle>
              <p className="text-sm text-gray-500 mt-1">Course-specific FAQs shown on the course detail page.</p>
            </CardHeader>
            <CardContent className="space-y-4">
              {faqs.map((faq, index) => (
                <div key={index} className="rounded-lg border border-gray-200 bg-gray-50/50 p-4 space-y-2">
                  <div className="flex gap-2">
                    <Input
                      value={faq.question}
                      onChange={(e) => updateFaq(index, 'question', e.target.value)}
                      placeholder="Question"
                      className="flex-1"
                    />
                    <button
                      type="button"
                      onClick={() => removeFaq(index)}
                      className="text-red-500 hover:text-red-700 p-1 shrink-0"
                      title="Remove FAQ"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                  <Textarea
                    value={faq.answer}
                    onChange={(e) => updateFaq(index, 'answer', e.target.value)}
                    placeholder="Answer"
                    rows={2}
                    className="resize-none"
                  />
                </div>
              ))}
              <Button type="button" variant="outline" onClick={addFaq} className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add FAQ
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Projects</CardTitle>
              <p className="text-sm text-gray-500 mt-1">Hands-on projects included in the course.</p>
            </CardHeader>
            <CardContent className="space-y-4">
              {projects.map((project, index) => (
                <div key={index} className="rounded-lg border border-gray-200 bg-gray-50/50 p-4 space-y-2">
                  <div className="flex gap-2">
                    <Input
                      value={project.title}
                      onChange={(e) => updateProject(index, 'title', e.target.value)}
                      placeholder="Project title"
                      className="flex-1"
                    />
                    <button
                      type="button"
                      onClick={() => removeProject(index)}
                      className="text-red-500 hover:text-red-700 p-1"
                      title="Remove project"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                  <Textarea
                    value={project.description || ''}
                    onChange={(e) => updateProject(index, 'description', e.target.value)}
                    placeholder="Brief description (optional)"
                    rows={2}
                    className="resize-none"
                  />
                </div>
              ))}
              <Button type="button" variant="outline" onClick={addProject} className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add Project
              </Button>
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
                <p className="text-xs text-amber-600 mt-1">Set to <strong>Published</strong> and keep <strong>Active</strong> on for the course to appear on the website.</p>
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
              <p className="text-sm text-gray-500 mt-1">Select existing skills or add a new one below.</p>
            </CardHeader>
            <CardContent className="space-y-4">
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
                {skills.length === 0 && (
                  <p className="text-sm text-gray-500">No skills yet. Add one below.</p>
                )}
              </div>
              <div className="flex gap-2 border-t border-gray-200 pt-4">
                <Input
                  value={newSkillName}
                  onChange={(e) => setNewSkillName(e.target.value)}
                  placeholder="New skill or tag name"
                  className="flex-1"
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addNewSkill())}
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={addNewSkill}
                  disabled={addingSkill || !newSkillName.trim()}
                  loading={addingSkill}
                >
                  <Plus className="h-4 w-4 mr-1" />
                  Add skill
                </Button>
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

