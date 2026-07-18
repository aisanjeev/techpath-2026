import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAuth, type Auth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.PUBLIC_FIREBASE_API_KEY,
  authDomain: import.meta.env.PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.PUBLIC_FIREBASE_APP_ID,
};

let _auth: Auth | null = null;

/**
 * Lazily initialise Firebase Auth.
 *
 * Kept lazy (NOT initialised at module load) so Astro's build-time prerendering never
 * executes initializeApp()/getAuth() — which throws `auth/invalid-api-key` when the
 * PUBLIC_FIREBASE_* vars are absent from the build environment. Every call site runs
 * client-side only (event handlers / useEffect), so this only ever executes in the
 * browser. Mirrors techpath-admin/src/lib/firebase.ts's lazy-singleton shape, just
 * reading Astro/Vite's import.meta.env instead of Next's process.env.
 */
export function getFirebaseAuth(): Auth {
  if (_auth) return _auth;
  const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
  _auth = getAuth(app);
  return _auth;
}
