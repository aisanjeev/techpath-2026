import type { Role, User } from '@/types/api';

/**
 * Role helpers for the admin app.
 *
 * These decide what a user is *shown*, not what they are *allowed*. Every route is
 * enforced server-side by `require_roles`; hiding a link here is a UX affordance and
 * nothing more. Never treat a check in this file as a security control.
 */

export const ROLES: Record<Role, string> = {
  admin: 'Admin',
  trainer: 'Trainer',
  user: 'User',
};

export function hasRole(user: User | null | undefined, ...roles: Role[]): boolean {
  return user != null && roles.includes(user.role);
}

export function isAdmin(user: User | null | undefined): boolean {
  return hasRole(user, 'admin');
}

/** Admins can use trainer views too, so they can support and demo the flow. */
export function isTrainer(user: User | null | undefined): boolean {
  return hasRole(user, 'trainer', 'admin');
}

/** Where a user belongs after signing in. */
export function landingPathForRole(user: User | null | undefined): string {
  if (!user) return '/login';
  if (user.role === 'trainer') return '/trainer';
  if (user.role === 'admin') return '/dashboard';
  // A plain "user" has nothing to see — the backend admits them but grants nothing.
  return '/no-access';
}
