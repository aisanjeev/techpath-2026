'use client';

import { useAuthStore } from '@/store/auth.store';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { FormField } from '@/components/ui/FormField';
import { User, Shield, Bell } from 'lucide-react';

export default function SettingsPage() {
  const { user } = useAuthStore();

  return (
    <div>
      <PageHeader
        title="Settings"
        description="Manage your account and preferences"
      />

      <div className="grid gap-6 md:grid-cols-2">
        {/* Profile Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-teal-100 text-teal-700">
                <User className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Profile</CardTitle>
                <CardDescription>Your personal information</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField label="Full Name" htmlFor="name">
              <Input
                id="name"
                defaultValue={user?.full_name || ''}
                placeholder="Your name"
              />
            </FormField>
            <FormField label="Email" htmlFor="email">
              <Input
                id="email"
                type="email"
                defaultValue={user?.email || ''}
                placeholder="your@email.com"
                disabled
              />
            </FormField>
            <Button>Update Profile</Button>
          </CardContent>
        </Card>

        {/* Security Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-100 text-orange-700">
                <Shield className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Security</CardTitle>
                <CardDescription>Manage your password</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField label="Current Password" htmlFor="current_password">
              <Input
                id="current_password"
                type="password"
                placeholder="••••••••"
              />
            </FormField>
            <FormField label="New Password" htmlFor="new_password">
              <Input
                id="new_password"
                type="password"
                placeholder="••••••••"
              />
            </FormField>
            <FormField label="Confirm Password" htmlFor="confirm_password">
              <Input
                id="confirm_password"
                type="password"
                placeholder="••••••••"
              />
            </FormField>
            <Button>Change Password</Button>
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card className="md:col-span-2">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-100 text-purple-700">
                <Bell className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Notifications</CardTitle>
                <CardDescription>Configure notification preferences</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <label className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Email Notifications</div>
                  <div className="text-sm text-gray-500">Receive email updates about new inquiries</div>
                </div>
                <input type="checkbox" className="h-5 w-5 rounded border-gray-300 text-teal-600" defaultChecked />
              </label>
              <label className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Weekly Reports</div>
                  <div className="text-sm text-gray-500">Get weekly summary of activities</div>
                </div>
                <input type="checkbox" className="h-5 w-5 rounded border-gray-300 text-teal-600" />
              </label>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

