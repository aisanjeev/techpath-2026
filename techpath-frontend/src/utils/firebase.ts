/**
 * Firebase client SDK — shared initialisation for the public frontend.
 * Only initialise once (singleton pattern) so hot-reloads don't create
 * duplicate apps.
 */
import { initializeApp, getApps, getApp, type FirebaseApp } from 'firebase/app';
import { getAnalytics, type Analytics } from 'firebase/analytics';

const firebaseConfig = {
  apiKey: import.meta.env.PUBLIC_FIREBASE_API_KEY,
  authDomain: import.meta.env.PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.PUBLIC_FIREBASE_APP_ID,
  measurementId: import.meta.env.PUBLIC_FIREBASE_MEASUREMENT_ID,
};

// Singleton Firebase app
const app: FirebaseApp =
  getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

export { app };

/**
 * Returns the Analytics instance.
 * Must be called in browser context only (Analytics is not available on server).
 */
export function getFirebaseAnalytics(): Analytics | null {
  if (typeof window === 'undefined') return null;
  try {
    return getAnalytics(app);
  } catch {
    return null;
  }
}
