/**
 * Google Places API — fetch live reviews for Techpath Academy.
 *
 * Called server-side only (Astro SSR frontmatter).
 * GOOGLE_MAPS_API_KEY and GOOGLE_REVIEWS_PLACE_ID must be set in .env.local
 * WITHOUT the PUBLIC_ prefix so they are never exposed to the browser.
 *
 * An in-memory cache (1-hour TTL) prevents hitting the Google API on every
 * page request within the same Node.js process.
 */

export interface GoogleReview {
  author_name: string;
  author_url?: string;
  profile_photo_url: string;
  rating: number;
  /** e.g. "2 months ago" */
  relative_time_description: string;
  text: string;
  /** Unix timestamp */
  time: number;
}

export interface GooglePlaceData {
  name: string;
  rating: number;
  user_ratings_total: number;
  reviews: GoogleReview[];
}

// Module-level cache — shared across SSR requests in the same process.
let _cache: { data: GooglePlaceData; expiresAt: number } | null = null;
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

export async function fetchGoogleReviews(): Promise<GooglePlaceData | null> {
  // Return cached data if still fresh
  if (_cache && Date.now() < _cache.expiresAt) {
    return _cache.data;
  }

  const apiKey = import.meta.env.GOOGLE_MAPS_API_KEY;
  const placeId = import.meta.env.GOOGLE_REVIEWS_PLACE_ID;

  if (!apiKey || !placeId) {
    // Keys not configured — silently return null so the section is skipped
    return null;
  }

  try {
    const url = new URL('https://maps.googleapis.com/maps/api/place/details/json');
    url.searchParams.set('place_id', placeId);
    // Request only the fields we need to minimise billing cost
    url.searchParams.set('fields', 'name,rating,user_ratings_total,reviews');
    // Newest reviews first; "most_relevant" is the default
    url.searchParams.set('reviews_sort', 'newest');
    url.searchParams.set('language', 'en');
    url.searchParams.set('key', apiKey);

    const res = await fetch(url.toString(), {
      headers: { Accept: 'application/json' },
      // Abort if Google takes > 5 s (prevents slow page loads)
      signal: AbortSignal.timeout(5000),
    });

    if (!res.ok) {
      console.warn(`[GoogleReviews] Places API HTTP ${res.status}`);
      return null;
    }

    const json = await res.json();

    if (json.status !== 'OK' || !json.result) {
      console.warn(`[GoogleReviews] Places API status: ${json.status}`, json.error_message ?? '');
      return null;
    }

    const data = json.result as GooglePlaceData;

    // Cache the result for 1 hour
    _cache = { data, expiresAt: Date.now() + CACHE_TTL_MS };

    return data;
  } catch (err) {
    // Network error, timeout, etc. — fail gracefully
    console.warn('[GoogleReviews] Fetch failed:', err instanceof Error ? err.message : err);
    return null;
  }
}

/**
 * Build a direct link to the Google Maps listing (opens review panel).
 * Works with the Place ID from the environment variable.
 */
export function googleMapsReviewUrl(placeId?: string): string {
  if (!placeId) return 'https://www.google.com/maps/search/Techpath+Academy+Mughalsarai';
  return `https://www.google.com/maps/place/?q=place_id:${placeId}`;
}
