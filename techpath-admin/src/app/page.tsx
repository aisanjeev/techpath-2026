'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth.store';
import { PageLoader } from '@/components/ui/Spinner';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, token } = useAuthStore();

  useEffect(() => {
    if (token && isAuthenticated) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  }, [token, isAuthenticated, router]);

  return <PageLoader />;
}
