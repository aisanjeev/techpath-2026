'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import {
  LayoutDashboard,
  Briefcase,
  FileText,
  LayoutTemplate,
  FolderKanban,
  Mail,
  Settings,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Image,
  GraduationCap,
  User,
  Key,
  Sliders,
  Presentation,
  Library,
  Users,
  UserCog,
  BookOpen,
} from 'lucide-react';
import { cn } from '@/lib/utils/cn';
import { useUIStore } from '@/store/ui.store';
import { useAuthStore } from '@/store/auth.store';
import { hasRole } from '@/lib/auth/roles';
import type { Role } from '@/types/api';

interface NavChild {
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  roles?: Role[];
}

interface NavItem {
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  /** Who may see this. Omitted means admin-only — deny by default, so a new item
   *  can never leak to other roles just because someone forgot to set this. */
  roles?: Role[];
  children?: NavChild[];
}

const navItems: NavItem[] = [
  { href: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { href: '/services', icon: Briefcase, label: 'Services' },
  { href: '/courses', icon: GraduationCap, label: 'Courses' },
  {
    href: '/training',
    icon: Presentation,
    label: 'Training',
    children: [
      { href: '/training', icon: BookOpen, label: 'Programs' },
      { href: '/training/assets', icon: Library, label: 'Asset Library' },
      { href: '/training/batches', icon: Users, label: 'Batches' },
      { href: '/training/students', icon: User, label: 'Students' },
    ],
  },
  { href: '/blog', icon: FileText, label: 'Blog Posts' },
  { href: '/pages', icon: LayoutTemplate, label: 'Pages' },
  { href: '/case-studies', icon: FolderKanban, label: 'Case Studies' },
  { href: '/media', icon: Image, label: 'Media Library' },
  { href: '/contacts', icon: Mail, label: 'Contacts' },
  {
    href: '/settings',
    icon: Settings,
    label: 'Settings',
    children: [
      { href: '/settings', icon: User, label: 'Profile' },
      { href: '/settings/users', icon: UserCog, label: 'Users' },
      { href: '/settings/general', icon: Sliders, label: 'App Settings' },
      { href: '/settings/secrets', icon: Key, label: 'Secrets' },
    ],
  },
];

const DEFAULT_ROLES: Role[] = ['admin'];

export function Sidebar() {
  const pathname = usePathname();
  const { sidebarCollapsed, toggleSidebar } = useUIStore();
  const { user } = useAuthStore();
  const [expandedItems, setExpandedItems] = useState<string[]>(['/settings', '/training']);

  const visibleItems = navItems.filter((item) =>
    hasRole(user, ...(item.roles ?? DEFAULT_ROLES))
  );

  const toggleExpanded = (href: string) => {
    setExpandedItems((prev) =>
      prev.includes(href) ? prev.filter((h) => h !== href) : [...prev, href]
    );
  };

  const isItemActive = (item: NavItem) => {
    if (item.children) {
      return item.children.some((child) => pathname === child.href);
    }
    return pathname.startsWith(item.href);
  };

  const visibleChildren = (item: NavItem) =>
    (item.children ?? []).filter((child) =>
      hasRole(user, ...(child.roles ?? item.roles ?? DEFAULT_ROLES))
    );

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 z-40 h-screen border-r border-gray-200 bg-white transition-all duration-300',
        sidebarCollapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Logo */}
      <div className="flex h-16 items-center justify-between border-b border-gray-200 px-4">
        {!sidebarCollapsed && (
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-white font-bold">
              T
            </div>
            <span className="text-lg font-semibold text-gray-900">TechPath</span>
          </Link>
        )}
        {sidebarCollapsed && (
          <Link href="/dashboard" className="mx-auto flex items-center justify-center">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-white font-bold">
              T
            </div>
          </Link>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1 p-3">
        {visibleItems.map((item) => {
          const isActive = isItemActive(item);
          const Icon = item.icon;
          const children = visibleChildren(item);
          const hasChildren = children.length > 0;
          const isExpanded = expandedItems.includes(item.href);

          if (hasChildren && !sidebarCollapsed) {
            return (
              <div key={item.href}>
                <button
                  onClick={() => toggleExpanded(item.href)}
                  className={cn(
                    'flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-teal-50 text-teal-700'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  )}
                >
                  <Icon className="h-5 w-5 shrink-0" />
                  <span className="flex-1 text-left">{item.label}</span>
                  <ChevronDown
                    className={cn(
                      'h-4 w-4 transition-transform',
                      isExpanded && 'rotate-180'
                    )}
                  />
                </button>
                {isExpanded && (
                  <div className="ml-4 mt-1 flex flex-col gap-1 border-l border-gray-200 pl-3">
                    {children.map((child) => {
                      const isChildActive = pathname === child.href;
                      const ChildIcon = child.icon;
                      return (
                        <Link
                          key={child.href}
                          href={child.href}
                          className={cn(
                            'flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors',
                            isChildActive
                              ? 'bg-teal-50 text-teal-700 font-medium'
                              : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                          )}
                        >
                          <ChildIcon className="h-4 w-4 shrink-0" />
                          <span>{child.label}</span>
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          }

          return (
            <Link
              key={item.href}
              href={hasChildren ? children[0].href : item.href}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-teal-50 text-teal-700'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
                sidebarCollapsed && 'justify-center px-2'
              )}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <Icon className="h-5 w-5 shrink-0" />
              {!sidebarCollapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Collapse Toggle */}
      <button
        onClick={toggleSidebar}
        className="absolute -right-3 top-20 flex h-6 w-6 items-center justify-center rounded-full border border-gray-200 bg-white shadow-sm hover:bg-gray-50"
      >
        {sidebarCollapsed ? (
          <ChevronRight className="h-3 w-3 text-gray-600" />
        ) : (
          <ChevronLeft className="h-3 w-3 text-gray-600" />
        )}
      </button>
    </aside>
  );
}

