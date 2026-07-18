import { create } from 'zustand';
import type { TrainingSessionQuestionResponse, DoubtRequest } from '@/types/classroom';

interface ClassroomState {
  questions: TrainingSessionQuestionResponse[];
  questionsArePublic: boolean;
  setQuestions: (questions: TrainingSessionQuestionResponse[]) => void;
  addQuestion: (question: TrainingSessionQuestionResponse) => void;
  updateQuestionUpvotes: (questionId: number, upvotes: number) => void;
  markQuestionAnswered: (questionId: number) => void;
  setQuestionsArePublic: (isPublic: boolean) => void;
  clearQuestions: () => void;
  
  doubtRequests: DoubtRequest[];
  setDoubtRequests: (doubts: DoubtRequest[]) => void;
  addDoubtRequest: (doubt: DoubtRequest) => void;
  updateDoubtRequest: (doubtId: number, update: Partial<DoubtRequest>) => void;
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
  setQuestionsArePublic: (isPublic: boolean) => set({ questionsArePublic: isPublic }),
  clearQuestions: () => set({ questions: [], questionsArePublic: false }),
  
  doubtRequests: [],
  setDoubtRequests: (doubtRequests) => set({ doubtRequests }),
  addDoubtRequest: (doubt) => set((state) => {
    if (state.doubtRequests.some(d => d.id === doubt.id)) return state;
    return { doubtRequests: [...state.doubtRequests, doubt] };
  }),
  updateDoubtRequest: (doubtId, update) => set((state) => ({
    doubtRequests: state.doubtRequests.map(d => d.id === doubtId ? { ...d, ...update } : d)
  }))
}));
