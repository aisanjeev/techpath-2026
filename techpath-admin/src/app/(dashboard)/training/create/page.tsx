'use client';

import { PageHeader } from '@/components/layout/PageHeader';
import { TrainingProgramForm } from '@/components/training/TrainingProgramForm';

export default function CreateTrainingProgramPage() {
  return (
    <div>
      <PageHeader
        title="New Training Program"
        description="Add modules and lecture assets once the programme exists"
      />
      <TrainingProgramForm />
    </div>
  );
}
