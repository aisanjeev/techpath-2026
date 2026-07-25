import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  activeModule: string;
  impersonateEmail: string;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setActiveModule: (module: string) => void;
  setImpersonateEmail: (email: string) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      theme: 'light',
      activeModule: 'dashboard',
      impersonateEmail: '',
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      setTheme: (theme) => set({ theme }),
      setActiveModule: (module) => set({ activeModule: module }),
      setImpersonateEmail: (email) => set({ impersonateEmail: email }),
    }),
    {
      name: 'ui-storage',
    }
  )
);

