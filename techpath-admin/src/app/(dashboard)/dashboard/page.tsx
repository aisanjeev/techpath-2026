'use client';

import { useEffect, useState } from 'react';
import { Briefcase, FileText, FolderKanban, Mail, TrendingUp, Users } from 'lucide-react';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { servicesService } from '@/services/services.service';
import { blogService } from '@/services/blog.service';
import { caseStudiesService } from '@/services/case-studies.service';
import { contactsService } from '@/services/contacts.service';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ElementType;
  description?: string;
  trend?: { value: number; positive: boolean };
}

function StatCard({ title, value, icon: Icon, description, trend }: StatCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">{title}</CardTitle>
        <Icon className="h-5 w-5 text-teal-600" />
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold text-gray-900">{value}</div>
        {description && (
          <p className="mt-1 text-xs text-gray-500">{description}</p>
        )}
        {trend && (
          <div className={`mt-2 flex items-center gap-1 text-xs ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
            <TrendingUp className={`h-3 w-3 ${!trend.positive && 'rotate-180'}`} />
            <span>{trend.value}% from last month</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function DashboardPage() {
  const [stats, setStats] = useState({
    services: 0,
    blogPosts: 0,
    caseStudies: 0,
    contacts: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const [servicesRes, blogRes, caseStudiesRes, contactsRes] = await Promise.all([
          servicesService.list({ limit: 1 }),
          blogService.list({ limit: 1 }),
          caseStudiesService.list({ limit: 1 }),
          contactsService.list({ limit: 1 }),
        ]);

        setStats({
          services: servicesRes.total,
          blogPosts: blogRes.total,
          caseStudies: caseStudiesRes.total,
          contacts: contactsRes.total,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, []);

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Overview of your content and activity"
      />

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Services"
          value={loading ? '...' : stats.services}
          icon={Briefcase}
          description="Active services"
        />
        <StatCard
          title="Blog Posts"
          value={loading ? '...' : stats.blogPosts}
          icon={FileText}
          description="Published articles"
        />
        <StatCard
          title="Case Studies"
          value={loading ? '...' : stats.caseStudies}
          icon={FolderKanban}
          description="Success stories"
        />
        <StatCard
          title="Contact Inquiries"
          value={loading ? '...' : stats.contacts}
          icon={Mail}
          description="Total inquiries"
        />
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">Quick Actions</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <QuickActionCard
            href="/services/create"
            icon={Briefcase}
            title="Add Service"
            description="Create a new service offering"
          />
          <QuickActionCard
            href="/blog/create"
            icon={FileText}
            title="Write Blog Post"
            description="Publish a new article"
          />
          <QuickActionCard
            href="/case-studies/create"
            icon={FolderKanban}
            title="Add Case Study"
            description="Share a success story"
          />
          <QuickActionCard
            href="/contacts"
            icon={Mail}
            title="View Inquiries"
            description="Manage contact requests"
          />
        </div>
      </div>
    </div>
  );
}

interface QuickActionCardProps {
  href: string;
  icon: React.ElementType;
  title: string;
  description: string;
}

function QuickActionCard({ href, icon: Icon, title, description }: QuickActionCardProps) {
  return (
    <a
      href={href}
      className="group flex items-center gap-4 rounded-xl border border-gray-200 bg-white p-4 transition-all hover:border-teal-300 hover:shadow-md"
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-teal-50 text-teal-600 transition-colors group-hover:bg-teal-100">
        <Icon className="h-6 w-6" />
      </div>
      <div>
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
    </a>
  );
}

