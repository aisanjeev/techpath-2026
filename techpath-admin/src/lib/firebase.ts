import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAuth, type Auth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET!,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID!,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID!,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
};

let _auth: Auth | null = null;

/**
 * Lazily initialise Firebase Auth.
 *
 * Kept lazy (NOT initialised at module load) so Next.js build-time
 * prerendering never executes initializeApp()/getAuth() — which throws
 * `auth/invalid-api-key` when the NEXT_PUBLIC_FIREBASE_* vars are absent from
 * the build environment. Every call site runs client-side only (event handlers
 * / useEffect / request interceptor), so this only ever executes in the browser.
 */
export function getFirebaseAuth(): Auth {
  if (_auth) return _auth;
  const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
  _auth = getAuth(app);
  return _auth;
}
