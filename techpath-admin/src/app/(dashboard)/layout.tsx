'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import { useAuthStore } from '@/store/auth.store';
import { useUIStore } from '@/store/ui.store';
import { authService } from '@/services/auth.service';
import { Sidebar } from '@/components/layout/Sidebar';
import { TopNav } from '@/components/layout/TopNav';
import { PageLoader } from '@/components/ui/Spinner';
import { cn } from '@/lib/utils/cn';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { user, login, logout, setLoading, isLoading } = useAuthStore();
  const { sidebarCollapsed } = useUIStore();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(getFirebaseAuth(), async (firebaseUser) => {
      if (!firebaseUser) {
        logout();
        router.push('/login');
        setChecked(true);
        return;
      }

      // Fetch backend user profile if not already loaded
      if (!user) {
        try {
          const backendUser = await authService.getCurrentUser();
          login(backendUser);
        } catch {
          logout();
          router.push('/login');
        }
      } else {
        setLoading(false);
      }

      setChecked(true);
    });

    return () => unsubscribe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!checked || isLoading) {
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
