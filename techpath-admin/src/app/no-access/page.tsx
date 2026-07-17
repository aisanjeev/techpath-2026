'use client';

import { useRouter } from 'next/navigation';
import { ShieldAlert } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { authService } from '@/services/auth.service';
import { useAuthStore } from '@/store/auth.store';

/**
 * Landing page for an authenticated account with no role.
 *
 * Signing in via Firebase without a matching TechPath record now provisions an inactive
 * "user" — deliberately inert. Bouncing them back to /login would look like a broken
 * password; this explains what actually happened.
 */
export default function NoAccessPage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();

  const handleLogout = async () => {
    try {
      await authService.logout();
    } finally {
      logout();
      router.push('/login');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-md rounded-xl border border-gray-200 bg-white p-8 text-center">
        <ShieldAlert className="mx-auto h-10 w-10 text-amber-500" />
        <h1 className="mt-4 text-lg font-semibold text-gray-900">No access yet</h1>
        <p className="mt-2 text-sm text-gray-600">
          Your account {user?.email ? <strong>{user.email}</strong> : ''} signed in, but it
          has not been given a role in TechPath yet.
        </p>
        <p className="mt-2 text-sm text-gray-500">
          An administrator needs to assign you a role and activate the account.
        </p>
        <Button variant="outline" className="mt-6 w-full" onClick={handleLogout}>
          Sign out
        </Button>
      </div>
    </div>
  );
}
