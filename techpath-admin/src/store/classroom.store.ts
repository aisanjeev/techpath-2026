import { create } from 'zustand';
import type { TrainingSessionQuestionResponse } from '@/types/classroom';

interface ClassroomState {
  questions: TrainingSessionQuestionResponse[];
  questionsArePublic: boolean;
  setQuestions: (questions: TrainingSessionQuestionResponse[]) => void;
  addQuestion: (question: TrainingSessionQuestionResponse) => void;
  updateQuestionUpvotes: (questionId: number, upvotes: number) => void;
  markQuestionAnswered: (questionId: number) => void;
  setQuestionsArePublic: (isPublic: boolean) => void;
  clearQuestions: () => void;
}

export const useClassroomStore = create<ClassroomState>((set) => ({
  questions: [],
  questionsArePublic: false,
  setQuestions: (questions) => set({ questions }),
  addQuestion: (question) =>
    set((state) => ({ questions: [question, ...state.questions] })),
  updateQuestionUpvotes: (questionId, upvotes) =>
    set((state) => ({
      questions: state.questions.map((q) =>
        q.id === questionId ? { ...q, upvotes } : q
      ),
    })),
  markQuestionAnswered: (questionId) =>
    set((state) => ({
      questions: state.questions.map((q) =>
        q.id === questionId ? { ...q, is_answered: true } : q
      ),
    })),
  setQuestionsArePublic: (isPublic) => set({ questionsArePublic: isPublic }),
  clearQuestions: () => set({ questions: [], questionsArePublic: false }),
}));
