'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight, ChevronUp, ChevronDown, MoreHorizontal, Pencil, Trash2, Eye } from 'lucide-react';
import { cn } from '@/lib/utils/cn';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';

export interface Column<T> {
  key: string;
  header: string;
  sortable?: boolean;
  render?: (item: T) => React.ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  keyExtractor: (item: T) => string | number;
  onEdit?: (item: T) => void;
  onDelete?: (item: T) => void;
  onView?: (item: T) => void;
  pagination?: {
    page: number;
    limit: number;
    total: number;
    onPageChange: (page: number) => void;
    onLimitChange?: (limit: number) => void;
  };
  sorting?: {
    field: string;
    direction: 'asc' | 'desc';
    onSort: (field: string, direction: 'asc' | 'desc') => void;
  };
  emptyMessage?: string;
}

export function DataTable<T>({
  columns,
  data,
  loading,
  keyExtractor,
  onEdit,
  onDelete,
  onView,
  pagination,
  sorting,
  emptyMessage = 'No data found',
}: DataTableProps<T>) {
  const [openActionMenu, setOpenActionMenu] = useState<string | number | null>(null);

  const handleSort = (field: string) => {
    if (!sorting) return;
    const direction = sorting.field === field && sorting.direction === 'asc' ? 'desc' : 'asc';
    sorting.onSort(field, direction);
  };

  const totalPages = pagination ? Math.ceil(pagination.total / pagination.limit) : 1;

  const getValue = (item: T, key: string): unknown => {
    return key.split('.').reduce((obj: unknown, k: string) => {
      if (obj && typeof obj === 'object' && k in obj) {
        return (obj as Record<string, unknown>)[k];
      }
      return undefined;
    }, item);
  };

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 bg-white">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-gray-200 bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={cn(
                    'px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600',
                    column.sortable && 'cursor-pointer select-none hover:bg-gray-100',
                    column.className
                  )}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center gap-1">
                    {column.header}
                    {column.sortable && sorting?.field === column.key && (
                      sorting.direction === 'asc' ? (
                        <ChevronUp className="h-4 w-4" />
                      ) : (
                        <ChevronDown className="h-4 w-4" />
                      )
                    )}
                  </div>
                </th>
              ))}
              {(onEdit || onDelete || onView) && (
                <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-600">
                  Actions
                </th>
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan={columns.length + 1} className="px-4 py-12">
                  <div className="flex justify-center">
                    <Spinner size="lg" />
                  </div>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length + 1} className="px-4 py-12 text-center text-gray-500">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              data.map((item) => {
                const key = keyExtractor(item);
                return (
                  <tr key={key} className="hover:bg-gray-50">
                    {columns.map((column) => (
                      <td key={column.key} className={cn('px-4 py-3 text-sm', column.className)}>
                        {column.render
                          ? column.render(item)
                          : String(getValue(item, column.key) ?? '-')}
                      </td>
                    ))}
                    {(onEdit || onDelete || onView) && (
                      <td className="relative px-4 py-3 text-right">
                        <button
                          onClick={() => setOpenActionMenu(openActionMenu === key ? null : key)}
                          className="rounded p-1 hover:bg-gray-100"
                        >
                          <MoreHorizontal className="h-5 w-5 text-gray-500" />
                        </button>
                        {openActionMenu === key && (
                          <>
                            <div
                              className="fixed inset-0 z-10"
                              onClick={() => setOpenActionMenu(null)}
                            />
                            <div className="absolute right-4 z-20 mt-1 w-36 rounded-lg border border-gray-200 bg-white py-1 shadow-lg">
                              {onView && (
                                <button
                                  onClick={() => {
                                    onView(item);
                                    setOpenActionMenu(null);
                                  }}
                                  className="flex w-full items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                >
                                  <Eye className="h-4 w-4" />
                                  View
                                </button>
                              )}
                              {onEdit && (
                                <button
                                  onClick={() => {
                                    onEdit(item);
                                    setOpenActionMenu(null);
                                  }}
                                  className="flex w-full items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                >
                                  <Pencil className="h-4 w-4" />
                                  Edit
                                </button>
                              )}
                              {onDelete && (
                                <button
                                  onClick={() => {
                                    onDelete(item);
                                    setOpenActionMenu(null);
                                  }}
                                  className="flex w-full items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50"
                                >
                                  <Trash2 className="h-4 w-4" />
                                  Delete
                                </button>
                              )}
                            </div>
                          </>
                        )}
                      </td>
                    )}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && pagination.total > 0 && (
        <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50 px-4 py-3">
          <div className="text-sm text-gray-500">
            Showing {((pagination.page - 1) * pagination.limit) + 1} to{' '}
            {Math.min(pagination.page * pagination.limit, pagination.total)} of{' '}
            {pagination.total} results
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => pagination.onPageChange(pagination.page - 1)}
              disabled={pagination.page <= 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm text-gray-600">
              Page {pagination.page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => pagination.onPageChange(pagination.page + 1)}
              disabled={pagination.page >= totalPages}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

