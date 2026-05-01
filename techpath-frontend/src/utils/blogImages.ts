/**
 * Resolves image references stored as strings (markdown frontmatter or API
 * payloads) into bundled, hashed URLs from `src/assets/images/**`.
 *
 * Frontmatter / API can store either a basename ("ai-guide.webp") or a legacy
 * path like "/images/trusted/foo.png". We look up by basename across all
 * subfolders. Absolute http(s) URLs and unmatched references pass through.
 */
const allAssetImages = import.meta.glob<string>(
  '/src/assets/images/**/*.{png,jpg,jpeg,webp,avif,svg}',
  { eager: true, query: '?url', import: 'default' }
);

const byBasename = new Map<string, string>();
for (const [path, url] of Object.entries(allAssetImages)) {
  const basename = path.split('/').pop();
  if (basename) byBasename.set(basename, url);
}

function resolve(ref: string | undefined | null): string | undefined {
  if (!ref) return undefined;
  if (/^https?:\/\//i.test(ref) || ref.startsWith('//')) return ref;
  const basename = ref.split('/').pop();
  if (!basename) return undefined;
  return byBasename.get(basename) ?? ref;
}

export const resolveBlogImage = resolve;
export const resolveAssetImage = resolve;
