'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth.store';
import { useUIStore } from '@/store/ui.store';
import { Sidebar } from '@/components/layout/Sidebar';
import { TopNav } from '@/components/layout/TopNav';
import { PageLoader } from '@/components/ui/Spinner';
import { cn } from '@/lib/utils/cn';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { token, isAuthenticated, setLoading, isLoading } = useAuthStore();
  const { sidebarCollapsed } = useUIStore();

  useEffect(() => {
    // Check authentication
    if (!token) {
      router.push('/login');
      return;
    }
    setLoading(false);
  }, [token, router, setLoading]);

  if (isLoading || !isAuthenticated) {
    return <PageLoader />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div
        className={cn(
          'transition-all duration-300',
          sidebarCollapsed ? 'ml-16' : 'ml-64'
        )}
      >
        <TopNav />
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
}

