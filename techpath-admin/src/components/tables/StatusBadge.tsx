import { Badge } from '@/components/ui/Badge';

type Status = 'draft' | 'published' | 'archived' | 'new' | 'in_progress' | 'resolved' | 'closed';

interface StatusBadgeProps {
  status: Status;
}

const statusConfig: Record<Status, { label: string; variant: 'default' | 'success' | 'warning' | 'error' | 'info' | 'purple' }> = {
  draft: { label: 'Draft', variant: 'default' },
  published: { label: 'Published', variant: 'success' },
  archived: { label: 'Archived', variant: 'warning' },
  new: { label: 'New', variant: 'info' },
  in_progress: { label: 'In Progress', variant: 'purple' },
  resolved: { label: 'Resolved', variant: 'success' },
  closed: { label: 'Closed', variant: 'default' },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status] || { label: status, variant: 'default' as const };
  return <Badge variant={config.variant}>{config.label}</Badge>;
}

interface ActiveBadgeProps {
  active: boolean;
}

export function ActiveBadge({ active }: ActiveBadgeProps) {
  return (
    <Badge variant={active ? 'success' : 'default'}>
      {active ? 'Active' : 'Inactive'}
    </Badge>
  );
}

interface FeaturedBadgeProps {
  featured: boolean;
}

export function FeaturedBadge({ featured }: FeaturedBadgeProps) {
  if (!featured) return null;
  return <Badge variant="purple">Featured</Badge>;
}

