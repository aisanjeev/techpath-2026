/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly PUBLIC_API_URL: string;
  readonly SITE_URL: string;
  /** "production" | "staging" | "development" — controls robots indexing */
  readonly PUBLIC_SITE_ENV: string;
  readonly PUBLIC_TURNSTILE_SITE_KEY?: string;
  readonly VITE_GA_TRACKING_ID?: string;
  readonly VITE_SENTRY_DSN?: string;
  /** Google Places API key — server-side only, no PUBLIC_ prefix */
  readonly GOOGLE_MAPS_API_KEY?: string;
  /** Google Place ID for Techpath Academy's Google Business Profile */
  readonly GOOGLE_REVIEWS_PLACE_ID?: string;
}

interface SpamProtection {
  attach(form: HTMLElement): void;
  payload(form: HTMLElement): { turnstile_token?: string; website?: string };
  reset(form: HTMLElement): void;
}

interface Window {
  __spamProtection?: SpamProtection;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare const __API_BASE_URL__: string;

