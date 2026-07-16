/**
 * Client-side data export helpers.
 *
 * Produces real `.xlsx` files (Open XML SpreadsheetML packaged in a ZIP) and
 * `.json` files without any third-party dependency. The ZIP is written with the
 * "store" (no compression) method, which Excel, LibreOffice and Google Sheets
 * all open cleanly.
 */

export interface ExportColumn<T> {
  /** Column header shown in the first row. */
  header: string;
  /** Extracts the cell value for a given row. */
  accessor: (row: T) => string | number | boolean | null | undefined;
}

/** Triggers a browser download for the given blob. */
function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  // Revoke on the next tick so the download has a chance to start.
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/** Appends `YYYY-MM-DD` to a base name, e.g. `contacts` -> `contacts-2026-07-16`. */
export function withDateStamp(base: string): string {
  const stamp = new Date().toISOString().slice(0, 10);
  return `${base}-${stamp}`;
}

/** Exports any JSON-serialisable data as a pretty-printed `.json` file. */
export function exportToJson(data: unknown, filename: string): void {
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  downloadBlob(blob, filename.endsWith('.json') ? filename : `${filename}.json`);
}

/** Exports rows to a real `.xlsx` workbook. Every cell is written as text. */
export function exportToExcel<T>(
  rows: T[],
  columns: ExportColumn<T>[],
  filename: string,
  sheetName = 'Sheet1'
): void {
  const matrix: string[][] = [
    columns.map((c) => c.header),
    ...rows.map((row) =>
      columns.map((c) => {
        const value = c.accessor(row);
        return value === null || value === undefined ? '' : String(value);
      })
    ),
  ];

  const zipBytes = buildXlsx(matrix, sheetName);
  const blob = new Blob([zipBytes as BlobPart], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  });
  downloadBlob(blob, filename.endsWith('.xlsx') ? filename : `${filename}.xlsx`);
}

// ---------------------------------------------------------------------------
// XLSX (Open XML) generation
// ---------------------------------------------------------------------------

function escapeXml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    // Strip control characters that are illegal in XML 1.0.
    .replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, '');
}

/** Converts a 0-based column index to a spreadsheet letter (0 -> A, 26 -> AA). */
function columnLetter(index: number): string {
  let n = index + 1;
  let letters = '';
  while (n > 0) {
    const remainder = (n - 1) % 26;
    letters = String.fromCharCode(65 + remainder) + letters;
    n = Math.floor((n - 1) / 26);
  }
  return letters;
}

function buildSheetXml(matrix: string[][]): string {
  const rowsXml = matrix
    .map((row, rowIndex) => {
      const cellsXml = row
        .map((cell, colIndex) => {
          const ref = `${columnLetter(colIndex)}${rowIndex + 1}`;
          if (cell === '') return `<c r="${ref}"/>`;
          return `<c r="${ref}" t="inlineStr"><is><t xml:space="preserve">${escapeXml(cell)}</t></is></c>`;
        })
        .join('');
      return `<row r="${rowIndex + 1}">${cellsXml}</row>`;
    })
    .join('');

  return (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' +
    `<sheetData>${rowsXml}</sheetData>` +
    '</worksheet>'
  );
}

function buildXlsx(matrix: string[][], sheetName: string): Uint8Array {
  const safeSheetName = escapeXml(sheetName).slice(0, 31);

  const files: Record<string, string> = {
    '[Content_Types].xml':
      '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
      '<Default Extension="xml" ContentType="application/xml"/>' +
      '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' +
      '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' +
      '</Types>',
    '_rels/.rels':
      '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>' +
      '</Relationships>',
    'xl/workbook.xml':
      '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">' +
      `<sheets><sheet name="${safeSheetName}" sheetId="1" r:id="rId1"/></sheets>` +
      '</workbook>',
    'xl/_rels/workbook.xml.rels':
      '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>' +
      '</Relationships>',
    'xl/worksheets/sheet1.xml': buildSheetXml(matrix),
  };

  const encoder = new TextEncoder();
  const entries = Object.entries(files).map(([name, content]) => ({
    name,
    data: encoder.encode(content),
  }));

  return buildZip(entries);
}

// ---------------------------------------------------------------------------
// Minimal ZIP writer (store method only)
// ---------------------------------------------------------------------------

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(bytes: Uint8Array): number {
  let crc = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) {
    crc = (crc >>> 8) ^ CRC_TABLE[(crc ^ bytes[i]) & 0xff];
  }
  return (crc ^ 0xffffffff) >>> 0;
}

interface ZipEntry {
  name: string;
  data: Uint8Array;
}

function buildZip(entries: ZipEntry[]): Uint8Array {
  const encoder = new TextEncoder();
  const localChunks: Uint8Array[] = [];
  const centralChunks: Uint8Array[] = [];
  let offset = 0;

  for (const entry of entries) {
    const nameBytes = encoder.encode(entry.name);
    const crc = crc32(entry.data);
    const size = entry.data.length;

    const local = new Uint8Array(30 + nameBytes.length);
    const localView = new DataView(local.buffer);
    localView.setUint32(0, 0x04034b50, true); // local file header signature
    localView.setUint16(4, 20, true); // version needed
    localView.setUint16(6, 0, true); // flags
    localView.setUint16(8, 0, true); // compression method: store
    localView.setUint16(10, 0, true); // mod time
    localView.setUint16(12, 0, true); // mod date
    localView.setUint32(14, crc, true);
    localView.setUint32(18, size, true); // compressed size
    localView.setUint32(22, size, true); // uncompressed size
    localView.setUint16(26, nameBytes.length, true);
    localView.setUint16(28, 0, true); // extra field length
    local.set(nameBytes, 30);

    localChunks.push(local, entry.data);

    const central = new Uint8Array(46 + nameBytes.length);
    const centralView = new DataView(central.buffer);
    centralView.setUint32(0, 0x02014b50, true); // central dir signature
    centralView.setUint16(4, 20, true); // version made by
    centralView.setUint16(6, 20, true); // version needed
    centralView.setUint16(8, 0, true); // flags
    centralView.setUint16(10, 0, true); // compression method
    centralView.setUint16(12, 0, true); // mod time
    centralView.setUint16(14, 0, true); // mod date
    centralView.setUint32(16, crc, true);
    centralView.setUint32(20, size, true); // compressed size
    centralView.setUint32(24, size, true); // uncompressed size
    centralView.setUint16(28, nameBytes.length, true);
    centralView.setUint16(30, 0, true); // extra field length
    centralView.setUint16(32, 0, true); // comment length
    centralView.setUint16(34, 0, true); // disk number
    centralView.setUint16(36, 0, true); // internal attrs
    centralView.setUint32(38, 0, true); // external attrs
    centralView.setUint32(42, offset, true); // local header offset
    central.set(nameBytes, 46);

    centralChunks.push(central);
    offset += local.length + size;
  }

  const centralSize = centralChunks.reduce((sum, c) => sum + c.length, 0);
  const centralOffset = offset;

  const eocd = new Uint8Array(22);
  const eocdView = new DataView(eocd.buffer);
  eocdView.setUint32(0, 0x06054b50, true); // EOCD signature
  eocdView.setUint16(4, 0, true); // disk number
  eocdView.setUint16(6, 0, true); // central dir start disk
  eocdView.setUint16(8, entries.length, true); // entries on this disk
  eocdView.setUint16(10, entries.length, true); // total entries
  eocdView.setUint32(12, centralSize, true);
  eocdView.setUint32(16, centralOffset, true);
  eocdView.setUint16(20, 0, true); // comment length

  const all = [...localChunks, ...centralChunks, eocd];
  const totalLength = all.reduce((sum, c) => sum + c.length, 0);
  const output = new Uint8Array(totalLength);
  let pointer = 0;
  for (const chunk of all) {
    output.set(chunk, pointer);
    pointer += chunk.length;
  }
  return output;
}
