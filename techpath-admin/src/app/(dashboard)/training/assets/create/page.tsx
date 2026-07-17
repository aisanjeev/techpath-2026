'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { LectureAssetForm } from '@/components/training/LectureAssetForm';

export default function CreateAssetPage() {
  return (
    <div>
      <PageHeader
        title="New Lecture Asset"
        description="Author it once — it can then be placed in any module"
      />
      <LectureAssetForm />
    </div>
  );
}
