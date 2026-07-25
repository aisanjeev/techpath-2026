'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { LogOut, Presentation, Eye } from 'lucide-react';
import { usePathname, useRouter } from 'next/navigation';
import { RoleGuard } from '@/components/auth/RoleGuard';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/auth.store';
import { useUIStore } from '@/store/ui.store';
import { authService } from '@/services/auth.service';
import { usersService } from '@/services/users.service';
import type { AdminUser } from '@/types/api';

export default function TrainerLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, logout } = useAuthStore();
  const { impersonateEmail, setImpersonateEmail } = useUIStore();
  const isPresenter = pathname.endsWith('/present');
  const isAdmin = user?.role === 'admin';

  const [trainers, setTrainers] = useState<AdminUser[]>([]);

  useEffect(() => {
    if (!isAdmin) return;
    usersService
      .list({ role: 'trainer', limit: 50 })
      .then((r) => setTrainers(r.items))
      .catch(() => undefined);
  }, [isAdmin]);

  useEffect(() => {
    return () => setImpersonateEmail('');
  }, [setImpersonateEmail]);

  const handleLogout = async () => {
    try {
      await authService.logout();
    } finally {
      logout();
      router.push('/login');
    }
  };

  if (isPresenter) {
    return <RoleGuard allow={['trainer', 'admin']}>{children}</RoleGuard>;
  }

  return (
    <RoleGuard allow={['trainer', 'admin']}>
      <div className="min-h-screen bg-gray-50">
        <header className="sticky top-0 z-30 border-b border-gray-200 bg-white">
          <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
            <Link href="/trainer" className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-white">
                <Presentation className="h-4 w-4" />
              </div>
              <div>
                <span className="text-lg font-semibold text-gray-900">TechPath</span>
                <span className="ml-2 text-sm text-gray-400">Trainer</span>
              </div>
            </Link>

            <div className="flex items-center gap-4">
              {isAdmin && (
                <div className="flex items-center gap-2">
                  <Eye className="h-4 w-4 text-gray-400" />
                  <select
                    value={impersonateEmail}
                    onChange={(e) => setImpersonateEmail(e.target.value)}
                    className="rounded-lg border border-gray-200 bg-gray-50 px-2.5 py-1 text-sm text-gray-700 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
                  >
                    <option value="">All batches (admin)</option>
                    {trainers.map((t) => (
                      <option key={t.id} value={t.email}>
                        {t.name} ({t.email})
                      </option>
                    ))}
                  </select>
                </div>
              )}
              {isAdmin && (
                <Link href="/dashboard" className="text-sm text-gray-500 hover:text-gray-700">
                  Admin panel
                </Link>
              )}
              <span className="hidden text-sm text-gray-600 sm:inline">{user?.name}</span>
              <Button variant="ghost" size="icon" onClick={handleLogout} aria-label="Sign out">
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </div>
    </RoleGuard>
  );
}
