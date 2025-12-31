'use client';

import { useEffect, useState, useCallback } from 'react';
import {
  Key,
  Mail,
  Brain,
  HardDrive,
  RefreshCw,
  Eye,
  EyeOff,
  Save,
  Trash2,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Loader2,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { Spinner } from '@/components/ui/Spinner';
import {
  secretsService,
  type SecretCategory,
  type SecretMetadata,
  type SecretsStatus,
} from '@/services/secrets.service';

// Category icons mapping
const CategoryIcon = ({ category }: { category: string }) => {
  switch (category) {
    case 'email':
      return <Mail className="h-5 w-5" />;
    case 'azure_openai':
      return <Brain className="h-5 w-5" />;
    case 'storage':
      return <HardDrive className="h-5 w-5" />;
    default:
      return <Key className="h-5 w-5" />;
  }
};

// Category colors mapping
const getCategoryColor = (category: string) => {
  switch (category) {
    case 'email':
      return 'bg-blue-100 text-blue-700';
    case 'azure_openai':
      return 'bg-purple-100 text-purple-700';
    case 'storage':
      return 'bg-green-100 text-green-700';
    default:
      return 'bg-gray-100 text-gray-700';
  }
};

export default function SecretsSettingsPage() {
  const [categories, setCategories] = useState<SecretCategory[]>([]);
  const [status, setStatus] = useState<SecretsStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  // Edit modal state
  const [editModal, setEditModal] = useState<{
    open: boolean;
    secret: SecretMetadata | null;
  }>({ open: false, secret: null });
  const [editValue, setEditValue] = useState('');
  const [showValue, setShowValue] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loadingValue, setLoadingValue] = useState(false);
  const [currentValue, setCurrentValue] = useState<string | null>(null);

  // Delete modal state
  const [deleteModal, setDeleteModal] = useState<{
    open: boolean;
    secret: SecretMetadata | null;
  }>({ open: false, secret: null });
  const [deleting, setDeleting] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [categoriesData, statusData] = await Promise.all([
        secretsService.listByCategory(),
        secretsService.getStatus(),
      ]);
      setCategories(categoriesData);
      setStatus(statusData);
    } catch (error) {
      console.error('Error fetching secrets:', error);
      toast.error('Failed to load secrets');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSync = async () => {
    setSyncing(true);
    try {
      await secretsService.syncStatus();
      toast.success('Secrets status synced from Key Vault');
      fetchData();
    } catch (error: any) {
      console.error('Error syncing secrets:', error);
      toast.error(error.message || 'Failed to sync secrets');
    } finally {
      setSyncing(false);
    }
  };

  const handleOpenEdit = async (secret: SecretMetadata) => {
    setEditModal({ open: true, secret });
    setEditValue('');
    setShowValue(false);
    setCurrentValue(null);

    // Load current value if set
    if (secret.is_set) {
      setLoadingValue(true);
      try {
        const valueData = await secretsService.getValue(secret.key_name, false);
        setCurrentValue(valueData.value);
      } catch (error) {
        console.error('Error loading secret value:', error);
      } finally {
        setLoadingValue(false);
      }
    }
  };

  const handleRevealValue = async () => {
    if (!editModal.secret) return;

    setLoadingValue(true);
    try {
      const valueData = await secretsService.getValue(editModal.secret.key_name, true);
      setCurrentValue(valueData.value);
      setShowValue(true);
    } catch (error) {
      console.error('Error revealing secret value:', error);
      toast.error('Failed to reveal secret value');
    } finally {
      setLoadingValue(false);
    }
  };

  const handleSaveSecret = async () => {
    if (!editModal.secret || !editValue.trim()) return;

    setSaving(true);
    try {
      await secretsService.updateValue(editModal.secret.key_name, editValue);
      toast.success('Secret saved to Key Vault');
      setEditModal({ open: false, secret: null });
      fetchData();
    } catch (error: any) {
      console.error('Error saving secret:', error);
      toast.error(error.message || 'Failed to save secret');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteSecret = async () => {
    if (!deleteModal.secret) return;

    setDeleting(true);
    try {
      await secretsService.deleteValue(deleteModal.secret.key_name);
      toast.success('Secret deleted from Key Vault');
      setDeleteModal({ open: false, secret: null });
      fetchData();
    } catch (error: any) {
      console.error('Error deleting secret:', error);
      toast.error(error.message || 'Failed to delete secret');
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        title="Secrets Management"
        description="Manage API keys and connection strings stored in Azure Key Vault"
        actions={
          <Button onClick={handleSync} disabled={syncing} variant="secondary">
            {syncing ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="mr-2 h-4 w-4" />
            )}
            Sync Status
          </Button>
        }
      />

      {/* Status Overview */}
      {status && (
        <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-100">
                  <Key className="h-5 w-5 text-gray-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Total Secrets</p>
                  <p className="text-2xl font-bold">{status.total_secrets}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Configured</p>
                  <p className="text-2xl font-bold text-green-600">{status.set_secrets}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-100">
                  <XCircle className="h-5 w-5 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Not Set</p>
                  <p className="text-2xl font-bold text-orange-600">{status.unset_secrets}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-lg ${
                    status.keyvault_configured ? 'bg-green-100' : 'bg-red-100'
                  }`}
                >
                  {status.keyvault_configured ? (
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  ) : (
                    <AlertTriangle className="h-5 w-5 text-red-600" />
                  )}
                </div>
                <div>
                  <p className="text-sm text-gray-500">Key Vault</p>
                  <p
                    className={`text-sm font-medium ${
                      status.keyvault_configured ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {status.keyvault_configured ? 'Connected' : 'Not Configured'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Warning if Key Vault not configured */}
      {status && !status.keyvault_configured && (
        <div className="mb-6 rounded-lg border border-orange-200 bg-orange-50 p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5" />
            <div>
              <h4 className="font-medium text-orange-800">Azure Key Vault Not Configured</h4>
              <p className="text-sm text-orange-700 mt-1">
                Set the following environment variables in your backend:
                <code className="block mt-2 p-2 bg-orange-100 rounded text-xs">
                  AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_KEYVAULT_URL
                </code>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Secrets by Category */}
      <div className="space-y-6">
        {categories.map((category) => (
          <Card key={category.category}>
            <CardHeader>
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-lg ${getCategoryColor(
                    category.category
                  )}`}
                >
                  <CategoryIcon category={category.category} />
                </div>
                <div>
                  <CardTitle>{category.display_name}</CardTitle>
                  <CardDescription>
                    {category.secrets.filter((s) => s.is_set).length} of {category.secrets.length}{' '}
                    configured
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="divide-y">
                {category.secrets.map((secret) => (
                  <div
                    key={secret.id}
                    className="flex items-center justify-between py-4 first:pt-0 last:pb-0"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium text-gray-900">{secret.display_name}</h4>
                        {secret.is_required && (
                          <span className="rounded bg-red-100 px-1.5 py-0.5 text-xs font-medium text-red-700">
                            Required
                          </span>
                        )}
                        {secret.is_set ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-gray-400" />
                        )}
                      </div>
                      <p className="mt-0.5 text-sm text-gray-500">{secret.description}</p>
                      <p className="mt-1 font-mono text-xs text-gray-400">{secret.key_name}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={() => handleOpenEdit(secret)}
                        disabled={!status?.keyvault_configured}
                      >
                        {secret.is_set ? 'Edit' : 'Set'}
                      </Button>
                      {secret.is_set && (
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setDeleteModal({ open: true, secret })}
                          disabled={!status?.keyvault_configured}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Edit Secret Modal */}
      <Modal
        isOpen={editModal.open}
        onClose={() => setEditModal({ open: false, secret: null })}
        title={`${editModal.secret?.is_set ? 'Edit' : 'Set'} ${editModal.secret?.display_name}`}
      >
        {editModal.secret && (
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">{editModal.secret.description}</p>
              <p className="mt-1 font-mono text-xs text-gray-400">{editModal.secret.key_name}</p>
            </div>

            {/* Current value (if set) */}
            {editModal.secret.is_set && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Current Value
                </label>
                <div className="flex items-center gap-2">
                  <Input
                    type={showValue ? 'text' : 'password'}
                    value={loadingValue ? 'Loading...' : currentValue || ''}
                    readOnly
                    className="font-mono text-sm"
                  />
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    onClick={handleRevealValue}
                    disabled={loadingValue || showValue}
                  >
                    {showValue ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </Button>
                </div>
              </div>
            )}

            {/* New value input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {editModal.secret.is_set ? 'New Value' : 'Value'}
              </label>
              <Input
                type="password"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                placeholder="Enter secret value"
                className="font-mono"
              />
              <p className="mt-1 text-xs text-gray-500">
                The value will be stored securely in Azure Key Vault
              </p>
            </div>

            <div className="flex justify-end gap-3 pt-4">
              <Button
                variant="secondary"
                onClick={() => setEditModal({ open: false, secret: null })}
              >
                Cancel
              </Button>
              <Button onClick={handleSaveSecret} disabled={saving || !editValue.trim()}>
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Save to Key Vault
                  </>
                )}
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, secret: null })}
        onConfirm={handleDeleteSecret}
        title="Delete Secret"
        description={`Are you sure you want to delete "${deleteModal.secret?.display_name}" from Azure Key Vault? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

