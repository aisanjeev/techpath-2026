'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import { PageLoader } from '@/components/ui/Spinner';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const unsub = onAuthStateChanged(getFirebaseAuth(), (user) => {
      router.push(user ? '/dashboard' : '/login');
    });
    return () => unsub();
  }, [router]);

  return <PageLoader />;
}
