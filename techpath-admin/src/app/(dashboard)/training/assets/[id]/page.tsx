'use client';

import { use, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Info } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { PageLoader } from '@/components/ui/Spinner';
import { LectureAssetForm } from '@/components/training/LectureAssetForm';
import { assetMeta } from '@/components/training/asset-type-registry';
import { trainingService } from '@/services/training.service';
import type { AssetUsage, LectureAsset } from '@/types/training';

export default function EditAssetPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const assetId = Number(id);
  const router = useRouter();

  const [asset, setAsset] = useState<LectureAsset | null>(null);
  const [usages, setUsages] = useState<AssetUsage[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      trainingService.getAsset(assetId),
      trainingService.getAssetUsages(assetId),
    ])
      .then(([a, u]) => {
        setAsset(a);
        setUsages(u);
      })
      .catch((err) => {
        toast.error(err instanceof Error ? err.message : 'Could not load the asset');
        router.push('/training/assets');
      })
      .finally(() => setLoading(false));
  }, [assetId, router]);

  if (loading || !asset) return <PageLoader />;

  const meta = assetMeta(asset.asset_type);

  return (
    <div>
      <Link
        href="/training/assets"
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to library
      </Link>

      <PageHeader
        title={asset.title}
        description={meta.label}
        actions={<Badge variant={asset.status === 'published' ? 'success' : 'warning'}>{asset.status}</Badge>}
      />

      {/* Assets are shared, so an edit here lands in every module using this one.
          Showing where it is used makes that a decision rather than a surprise. */}
      {usages.length > 0 && (
        <Card className="mb-6 border-blue-200 bg-blue-50 p-4">
          <div className="flex gap-3">
            <Info className="h-5 w-5 shrink-0 text-blue-600" />
            <div className="min-w-0">
              <p className="text-sm font-medium text-blue-900">
                Used in {usages.length} module{usages.length === 1 ? '' : 's'}
              </p>
              <p className="mt-0.5 text-xs text-blue-700">
                Changes here apply everywhere this asset is used.
              </p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {usages.map((u) => (
                  <Link
                    key={`${u.program_id}-${u.module_id}`}
                    href={`/training/${u.program_id}/modules/${u.module_id}`}
                    className="rounded-full border border-blue-200 bg-white px-2.5 py-1 text-xs text-blue-800 hover:border-blue-400"
                  >
                    {u.program_title} › {u.module_title}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </Card>
      )}

      <LectureAssetForm asset={asset} />
    </div>
  );
}
