'use client';

import { useUIStore } from '@/store/ui.store';
import { Sidebar } from '@/components/layout/Sidebar';
import { TopNav } from '@/components/layout/TopNav';
import { RoleGuard } from '@/components/auth/RoleGuard';
import { cn } from '@/lib/utils/cn';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { sidebarCollapsed } = useUIStore();

  return (
    <RoleGuard allow={['admin']}>
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
    </RoleGuard>
  );
}
