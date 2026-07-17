'use client';

import { useCallback, useEffect, useState } from 'react';
import { Plus, Trash2, Eye, EyeOff } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { DataTable, type Column } from '@/components/tables/DataTable';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Modal } from '@/components/ui/Modal';
import { FormField } from '@/components/ui/FormField';
import { usersService } from '@/services/users.service';
import { useAuthStore } from '@/store/auth.store';
import type { AdminUser, Role } from '@/types/api';

const ROLE_VARIANT: Record<Role, 'purple' | 'info' | 'default'> = {
  admin: 'purple',
  trainer: 'info',
  user: 'default',
};

export default function UsersPage() {
  const { user: currentUser } = useAuthStore();
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);

  // Add user modal
  const [addOpen, setAddOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState<Role>('trainer');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  // Delete confirmation
  const [deleteTarget, setDeleteTarget] = useState<AdminUser | null>(null);
  const [deleting, setDeleting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await usersService.list({ limit: 100 });
      setUsers(result.items);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not load users');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const resetForm = () => {
    setEmail('');
    setName('');
    setRole('trainer');
    setPassword('');
    setShowPassword(false);
  };

  const addUser = async () => {
    if (!email.trim() || !name.trim()) return;
    if (password && password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }
    setSaving(true);
    try {
      await usersService.provision({
        email: email.trim(),
        name: name.trim(),
        role,
        password: password || undefined,
      });
      toast.success(
        password
          ? 'User created with Firebase account. They can sign in immediately.'
          : 'User added. Now create their account in the Firebase console.'
      );
      setAddOpen(false);
      resetForm();
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not add the user');
    } finally {
      setSaving(false);
    }
  };

  const changeRole = async (u: AdminUser, next: Role) => {
    try {
      await usersService.update(u.id, { role: next });
      toast.success(`${u.name} is now ${next}`);
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not change the role');
    }
  };

  const toggleActive = async (u: AdminUser) => {
    try {
      await usersService.update(u.id, { is_active: !u.is_active });
      toast.success(u.is_active ? 'Account deactivated' : 'Account activated');
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not update the account');
    }
  };

  const confirmDelete = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      await usersService.remove(deleteTarget.id);
      toast.success(`${deleteTarget.name} has been deleted`);
      setDeleteTarget(null);
      void load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Could not delete the user');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<AdminUser>[] = [
    {
      key: 'name',
      header: 'User',
      render: (u) => (
        <div>
          <p className="font-medium text-gray-900">
            {u.name}
            {u.id === currentUser?.id && (
              <span className="ml-2 text-xs font-normal text-gray-400">(you)</span>
            )}
          </p>
          <p className="text-xs text-gray-500">{u.email}</p>
        </div>
      ),
    },
    {
      key: 'role',
      header: 'Role',
      render: (u) => (
        <Select
          value={u.role}
          onChange={(e) => changeRole(u, e.target.value as Role)}
          disabled={u.id === currentUser?.id}
          className="max-w-[140px]"
        >
          <option value="admin">Admin</option>
          <option value="trainer">Trainer</option>
          <option value="user">User</option>
        </Select>
      ),
    },
    {
      key: 'has_signed_in',
      header: 'Firebase',
      render: (u) =>
        u.has_signed_in ? (
          <Badge variant="success">Linked</Badge>
        ) : (
          <Badge variant="warning">Awaiting first sign-in</Badge>
        ),
    },
    {
      key: 'is_active',
      header: 'Status',
      render: (u) => (
        <button
          onClick={() => toggleActive(u)}
          disabled={u.id === currentUser?.id}
          className="disabled:cursor-not-allowed disabled:opacity-60"
          title={u.id === currentUser?.id ? 'You cannot deactivate yourself' : undefined}
        >
          <Badge variant={u.is_active ? 'success' : 'error'}>
            {u.is_active ? 'Active' : 'Inactive'}
          </Badge>
        </button>
      ),
    },
    {
      key: 'actions',
      header: '',
      render: (u) =>
        u.id !== currentUser?.id ? (
          <button
            onClick={() => setDeleteTarget(u)}
            className="rounded p-1.5 text-gray-400 transition-colors hover:bg-red-50 hover:text-red-600"
            title={`Delete ${u.name}`}
          >
            <Trash2 className="h-4 w-4" />
          </button>
        ) : null,
    },
  ];

  return (
    <div>
      <PageHeader
        title="Users"
        description="Who can sign in, and what they can see"
        actions={
          <Button onClick={() => setAddOpen(true)}>
            <Plus className="mr-1 h-4 w-4" />
            Add user
          </Button>
        }
      />

      <DataTable
        columns={columns}
        data={users}
        loading={loading}
        keyExtractor={(u) => u.id}
        emptyMessage="No users yet."
      />

      {/* Add user modal */}
      <Modal
        isOpen={addOpen}
        onClose={() => {
          setAddOpen(false);
          resetForm();
        }}
        title="Add a user"
      >
        <div className="space-y-4">
          <FormField label="Email" required>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="trainer@techpath.biz"
              autoFocus
            />
          </FormField>
          <FormField label="Name" required>
            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Rachit" />
          </FormField>
          <FormField label="Role">
            <Select value={role} onChange={(e) => setRole(e.target.value as Role)}>
              <option value="trainer">Trainer</option>
              <option value="admin">Admin</option>
              <option value="user">User (no access)</option>
            </Select>
          </FormField>
          <FormField
            label="Password"
            description="Set a password to create their Firebase account automatically. Leave empty to create the Firebase account manually later."
          >
            <div className="relative">
              <Input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Min 6 characters"
                className="pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </FormField>
          <div className="flex justify-end gap-3 pt-2">
            <Button
              variant="outline"
              onClick={() => {
                setAddOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button onClick={addUser} disabled={saving || !email.trim() || !name.trim()}>
              {saving ? 'Creating…' : 'Create user'}
            </Button>
          </div>
        </div>
      </Modal>

      {/* Delete confirmation modal */}
      <Modal
        isOpen={deleteTarget !== null}
        onClose={() => setDeleteTarget(null)}
        title="Delete user"
      >
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            Are you sure you want to delete{' '}
            <strong>{deleteTarget?.name}</strong> ({deleteTarget?.email})?
          </p>
          {deleteTarget?.has_signed_in && (
            <Card className="border-amber-200 bg-amber-50 p-3">
              <p className="text-xs text-amber-800">
                This user has a linked Firebase account. It will also be deleted and they
                will no longer be able to sign in.
              </p>
            </Card>
          )}
          <p className="text-xs text-gray-500">This action cannot be undone.</p>
          <div className="flex justify-end gap-3">
            <Button variant="outline" onClick={() => setDeleteTarget(null)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={confirmDelete} disabled={deleting}>
              {deleting ? 'Deleting…' : 'Delete user'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
