'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { getFirebaseAuth } from '@/lib/firebase';
import { useAuthStore } from '@/store/auth.store';
import { authService } from '@/services/auth.service';
import { PageLoader } from '@/components/ui/Spinner';
import { hasRole, landingPathForRole } from '@/lib/auth/roles';
import type { Role } from '@/types/api';

interface RoleGuardProps {
  allow: Role[];
  children: React.ReactNode;
}

/**
 * Gates a route group on Firebase auth plus a backend role.
 *
 * This is presentation only — the API enforces roles itself. Its job is to stop a
 * trainer landing on an admin screen full of failed requests, and to send each role
 * somewhere useful.
 */
export function RoleGuard({ allow, children }: RoleGuardProps) {
  const router = useRouter();
  const { user, login, logout, isLoading, setLoading } = useAuthStore();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(getFirebaseAuth(), async (firebaseUser) => {
      if (!firebaseUser) {
        logout();
        router.push('/login');
        setChecked(true);
        return;
      }

      let current = user;
      if (!current) {
        try {
          current = await authService.getCurrentUser();
          login(current);
        } catch {
          // A 401 here is the expected path for an account that exists in Firebase but
          // is inactive in TechPath — an unrecognised sign-in, awaiting an admin.
          logout();
          router.push('/login');
          setChecked(true);
          return;
        }
      } else {
        setLoading(false);
      }

      if (!hasRole(current, ...allow)) {
        router.replace(landingPathForRole(current));
        setChecked(true);
        return;
      }

      setChecked(true);
    });

    return () => unsubscribe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!checked || isLoading) {
    return <PageLoader />;
  }

  // Redirecting; render nothing rather than flashing a screen they can't use.
  if (!hasRole(user, ...allow)) {
    return <PageLoader />;
  }

  return <>{children}</>;
}
