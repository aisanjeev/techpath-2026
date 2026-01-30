'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth.store';
import { PageLoader } from '@/components/ui/Spinner';

export default function HomePage() {
  const router = useRouter();
  const { token } = useAuthStore();
  const [hasHydrated, setHasHydrated] = useState(false);

  useEffect(() => {
    const unsub = useAuthStore.persist?.onFinishHydration?.(() => setHasHydrated(true));
    if (useAuthStore.persist?.hasHydrated?.()) setHasHydrated(true);
    return () => unsub?.();
  }, []);

  useEffect(() => {
    if (!hasHydrated) return;
    if (token) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  }, [hasHydrated, token, router]);

  return <PageLoader />;
}
