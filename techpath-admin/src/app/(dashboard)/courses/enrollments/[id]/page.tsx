'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Phone, Mail, Linkedin, Calendar, User, Briefcase, GraduationCap, MessageSquare } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Breadcrumb } from '@/components/layout/Breadcrumb';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Input } from '@/components/ui/Input';
import { FormField } from '@/components/ui/FormField';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { PageLoader } from '@/components/ui/Spinner';
import { courseService } from '@/services/course.service';
import { formatDateTime, formatRelativeTime } from '@/lib/utils/format';
import type { CourseEnrollment } from '@/types/api';

const statusColors: Record<string, string> = {
  new: 'bg-blue-100 text-blue-800',
  contacted: 'bg-yellow-100 text-yellow-800',
  interested: 'bg-purple-100 text-purple-800',
  enrolled: 'bg-green-100 text-green-800',
  not_interested: 'bg-gray-100 text-gray-800',
  closed: 'bg-red-100 text-red-800',
};

export default function EnrollmentDetailPage() {
  const router = useRouter();
  const params = useParams();
  const [enrollment, setEnrollment] = useState<CourseEnrollment | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [formData, setFormData] = useState({
    status: '',
    notes: '',
    assigned_to: '',
    next_followup_at: '',
  });

  const enrollmentId = Number(params.id);

  useEffect(() => {
    async function fetchEnrollment() {
      try {
        const data = await courseService.getEnrollment(enrollmentId);
        setEnrollment(data);
        setFormData({
          status: data.status,
          notes: data.notes || '',
          assigned_to: data.assigned_to || '',
          next_followup_at: data.next_followup_at ? data.next_followup_at.slice(0, 16) : '',
        });
      } catch (error) {
        console.error('Error fetching enrollment:', error);
        toast.error('Enrollment not found');
        router.push('/courses/enrollments');
      } finally {
        setLoading(false);
      }
    }

    if (enrollmentId) {
      fetchEnrollment();
    }
  }, [enrollmentId, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!enrollment) return;

    setSaving(true);
    try {
      await courseService.updateEnrollment(enrollment.id, {
        status: formData.status as CourseEnrollment['status'],
        notes: formData.notes || undefined,
        assigned_to: formData.assigned_to || undefined,
        next_followup_at: formData.next_followup_at || undefined,
      });
      toast.success('Enrollment updated successfully');
      router.push('/courses/enrollments');
    } catch (error) {
      console.error('Error updating enrollment:', error);
      toast.error('Failed to update enrollment');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <PageLoader />;
  }

  if (!enrollment) {
    return null;
  }

  return (
    <div>
      <Breadcrumb
        items={[
          { label: 'Courses', href: '/courses' },
          { label: 'Enrollments', href: '/courses/enrollments' },
          { label: enrollment.name },
        ]}
      />
      <PageHeader
        title={`Lead: ${enrollment.name}`}
        description={`Received ${formatRelativeTime(enrollment.created_at)}`}
      />

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Lead Information */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Contact Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                    <User className="h-5 w-5 text-gray-500" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Name</div>
                    <div className="font-medium">{enrollment.name}</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                    <Mail className="h-5 w-5 text-gray-500" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Email</div>
                    <a href={`mailto:${enrollment.email}`} className="font-medium text-teal-600 hover:underline">
                      {enrollment.email}
                    </a>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                    <Phone className="h-5 w-5 text-gray-500" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Phone</div>
                    <a href={`tel:${enrollment.phone}`} className="font-medium text-teal-600 hover:underline">
                      {enrollment.phone}
                    </a>
                  </div>
                </div>
                {enrollment.linkedin_url && (
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                      <Linkedin className="h-5 w-5 text-gray-500" />
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">LinkedIn</div>
                      <a href={enrollment.linkedin_url} target="_blank" rel="noopener noreferrer" className="font-medium text-teal-600 hover:underline">
                        View Profile
                      </a>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Professional Background</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {enrollment.current_role && (
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                      <Briefcase className="h-5 w-5 text-gray-500" />
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Current Role</div>
                      <div className="font-medium">{enrollment.current_role}</div>
                    </div>
                  </div>
                )}
                {enrollment.experience && (
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                      <Calendar className="h-5 w-5 text-gray-500" />
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Experience</div>
                      <div className="font-medium">{enrollment.experience}</div>
                    </div>
                  </div>
                )}
                {enrollment.education && (
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                      <GraduationCap className="h-5 w-5 text-gray-500" />
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Education</div>
                      <div className="font-medium">{enrollment.education}</div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {enrollment.course && (
            <Card>
              <CardHeader>
                <CardTitle>Course Interest</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-4">
                  {enrollment.course.featured_image ? (
                    <img
                      src={enrollment.course.featured_image}
                      alt={enrollment.course.title}
                      className="h-16 w-24 rounded object-cover"
                    />
                  ) : (
                    <div className="h-16 w-24 rounded bg-gray-100 flex items-center justify-center">
                      <GraduationCap className="h-8 w-8 text-gray-400" />
                    </div>
                  )}
                  <div>
                    <div className="font-medium text-lg">{enrollment.course.title}</div>
                    <div className="text-sm text-gray-500">
                      {enrollment.course.duration} • {enrollment.course.level}
                    </div>
                    {enrollment.preferred_batch && (
                      <div className="text-sm text-gray-500">
                        Preferred batch: {enrollment.preferred_batch}
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {enrollment.message && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5" />
                  Message
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 whitespace-pre-wrap">{enrollment.message}</p>
              </CardContent>
            </Card>
          )}

          {/* Source Info */}
          {(enrollment.source || enrollment.utm_source) && (
            <Card>
              <CardHeader>
                <CardTitle>Source Tracking</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  {enrollment.source && (
                    <div>
                      <span className="text-gray-500">Source:</span>{' '}
                      <span className="font-medium">{enrollment.source}</span>
                    </div>
                  )}
                  {enrollment.utm_source && (
                    <div>
                      <span className="text-gray-500">UTM Source:</span>{' '}
                      <span className="font-medium">{enrollment.utm_source}</span>
                    </div>
                  )}
                  {enrollment.utm_medium && (
                    <div>
                      <span className="text-gray-500">UTM Medium:</span>{' '}
                      <span className="font-medium">{enrollment.utm_medium}</span>
                    </div>
                  )}
                  {enrollment.utm_campaign && (
                    <div>
                      <span className="text-gray-500">UTM Campaign:</span>{' '}
                      <span className="font-medium">{enrollment.utm_campaign}</span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Status & Actions */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Lead Status</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <FormField label="Status" htmlFor="status">
                  <Select
                    id="status"
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="new">New</option>
                    <option value="contacted">Contacted</option>
                    <option value="interested">Interested</option>
                    <option value="enrolled">Enrolled</option>
                    <option value="not_interested">Not Interested</option>
                    <option value="closed">Closed</option>
                  </Select>
                </FormField>

                <FormField label="Assigned To" htmlFor="assigned_to">
                  <Input
                    id="assigned_to"
                    value={formData.assigned_to}
                    onChange={(e) => setFormData({ ...formData, assigned_to: e.target.value })}
                    placeholder="Counselor name"
                  />
                </FormField>

                <FormField label="Next Follow-up" htmlFor="next_followup_at">
                  <Input
                    id="next_followup_at"
                    type="datetime-local"
                    value={formData.next_followup_at}
                    onChange={(e) => setFormData({ ...formData, next_followup_at: e.target.value })}
                  />
                </FormField>

                <FormField label="Internal Notes" htmlFor="notes">
                  <Textarea
                    id="notes"
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    placeholder="Add notes about this lead..."
                    rows={5}
                  />
                </FormField>

                <Button type="submit" className="w-full" loading={saving}>
                  Update Lead
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Timeline</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Received</span>
                <span>{formatDateTime(enrollment.created_at)}</span>
              </div>
              {enrollment.last_contacted_at && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Last Contacted</span>
                  <span>{formatDateTime(enrollment.last_contacted_at)}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-500">Last Updated</span>
                <span>{formatDateTime(enrollment.updated_at)}</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <Button variant="secondary" className="w-full" onClick={() => router.push('/courses/enrollments')}>
                Back to Enrollments
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

