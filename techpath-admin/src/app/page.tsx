'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { firebaseAuth } from '@/lib/firebase';
import { PageLoader } from '@/components/ui/Spinner';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const unsub = onAuthStateChanged(firebaseAuth, (user) => {
      router.push(user ? '/dashboard' : '/login');
    });
    return () => unsub();
  }, [router]);

  return <PageLoader />;
}
