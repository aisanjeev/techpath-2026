'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import { PageLoader } from '@/components/ui/Spinner';
import { authService } from '@/services/auth.service';
import { useAuthStore } from '@/store/auth.store';
import { landingPathForRole } from '@/lib/auth/roles';

export default function HomePage() {
  const router = useRouter();
  const { login } = useAuthStore();

  useEffect(() => {
    const unsub = onAuthStateChanged(getFirebaseAuth(), async (firebaseUser) => {
      if (!firebaseUser) {
        router.push('/login');
        return;
      }
      // A trainer belongs on /trainer, not the admin dashboard — so the role has to be
      // known before we can pick a destination.
      try {
        const user = await authService.getCurrentUser();
        login(user);
        router.push(landingPathForRole(user));
      } catch {
        router.push('/login');
      }
    });
    return () => unsub();
  }, [router, login]);

  return <PageLoader />;
}
