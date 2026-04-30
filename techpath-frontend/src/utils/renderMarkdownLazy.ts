/**
 * Render markdown to HTML with loading="lazy" and decoding="async" on all images.
 * Use for policy pages and any markdown body content.
 */
import { marked } from 'marked';

function addLazyToImages(html: string): string {
  return html.replace(
    /<img(?=\s)([^>]*?)>/gi,
    (match, attrs) => {
      if (/loading\s*=/i.test(attrs)) return match;
      return `<img${attrs} loading="lazy" decoding="async">`;
    }
  );
}

function wrapTables(html: string): string {
  return html.replace(
    /<table>/gi,
    '<div class="table-wrapper"><table>'
  ).replace(
    /<\/table>/gi,
    '</table></div>'
  );
}

export async function renderMarkdownWithLazyImages(markdown: string): Promise<string> {
  const html = await marked.parse(markdown);
  return wrapTables(addLazyToImages(html));
}
