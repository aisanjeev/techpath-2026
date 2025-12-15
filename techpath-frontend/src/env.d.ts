/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly SITE_URL: string;
  readonly VITE_GA_TRACKING_ID?: string;
  readonly VITE_SENTRY_DSN?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare const __API_BASE_URL__: string;

