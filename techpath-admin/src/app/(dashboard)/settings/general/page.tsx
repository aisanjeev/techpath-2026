'use client';

import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { Save, RefreshCw, Mail, Building2, Globe, BarChart3, Edit3 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Modal } from '@/components/ui/Modal';
import { Textarea } from '@/components/ui/Textarea';
import { settingsService, SettingsCategory, AppSetting } from '@/services/settings.service';

// Category icons
const categoryIcons: Record<string, React.ReactNode> = {
  email: <Mail className="w-5 h-5" />,
  general: <Building2 className="w-5 h-5" />,
  seo: <BarChart3 className="w-5 h-5" />,
  content: <Globe className="w-5 h-5" />,
};

export default function GeneralSettingsPage() {
  const [categories, setCategories] = useState<SettingsCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editedValues, setEditedValues] = useState<Record<string, string>>({});
  const [hasChanges, setHasChanges] = useState(false);

  // JSON editor modal (for value_type === 'json' or large text)
  const [jsonModalOpen, setJsonModalOpen] = useState(false);
  const [jsonModalSetting, setJsonModalSetting] = useState<AppSetting | null>(null);
  const [jsonModalValue, setJsonModalValue] = useState('');
  const [jsonModalSaving, setJsonModalSaving] = useState(false);
  const [jsonModalError, setJsonModalError] = useState<string | null>(null);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const data = await settingsService.listSettings();
      setCategories(data);
      
      // Initialize edited values
      const initialValues: Record<string, string> = {};
      data.forEach(cat => {
        cat.settings.forEach(setting => {
          initialValues[setting.key] = setting.value || '';
        });
      });
      setEditedValues(initialValues);
      setHasChanges(false);
    } catch (error: any) {
      toast.error(error.message || 'Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const handleValueChange = (key: string, value: string) => {
    setEditedValues(prev => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      
      // Find all changed values
      const updates: { key: string; value: string | null }[] = [];
      categories.forEach(cat => {
        cat.settings.forEach(setting => {
          const newValue = editedValues[setting.key];
          if (newValue !== (setting.value || '')) {
            updates.push({
              key: setting.key,
              value: newValue || null,
            });
          }
        });
      });

      if (updates.length === 0) {
        toast('No changes to save');
        return;
      }

      await settingsService.updateSettings(updates);
      toast.success(`Saved ${updates.length} setting(s)`);
      
      // Refresh to get updated data
      await fetchSettings();
    } catch (error: any) {
      toast.error(error.message || 'Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const handleReset = () => {
    // Reset to original values
    const originalValues: Record<string, string> = {};
    categories.forEach(cat => {
      cat.settings.forEach(setting => {
        originalValues[setting.key] = setting.value || '';
      });
    });
    setEditedValues(originalValues);
    setHasChanges(false);
    toast('Changes discarded');
  };

  const openJsonModal = (setting: AppSetting) => {
    const value = editedValues[setting.key] ?? setting.value ?? '';
    let displayValue = value;
    try {
      if (value.trim()) {
        const parsed = JSON.parse(value);
        displayValue = JSON.stringify(parsed, null, 2);
      }
    } catch {
      // Keep raw value if not valid JSON
    }
    setJsonModalSetting(setting);
    setJsonModalValue(displayValue);
    setJsonModalError(null);
    setJsonModalOpen(true);
  };

  const closeJsonModal = () => {
    setJsonModalOpen(false);
    setJsonModalSetting(null);
    setJsonModalValue('');
    setJsonModalError(null);
  };

  const saveJsonModal = async () => {
    if (!jsonModalSetting) return;
    setJsonModalError(null);
    try {
      const trimmed = jsonModalValue.trim();
      if (trimmed) {
        JSON.parse(trimmed);
      }
    } catch {
      setJsonModalError('Invalid JSON. Please fix syntax errors.');
      return;
    }
    try {
      setJsonModalSaving(true);
      await settingsService.updateSetting(
        jsonModalSetting.key,
        jsonModalValue.trim() || null
      );
      setEditedValues(prev => ({
        ...prev,
        [jsonModalSetting.key]: jsonModalValue.trim(),
      }));
      toast.success('Saved');
      closeJsonModal();
      await fetchSettings();
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : 'Failed to save';
      setJsonModalError(msg);
      toast.error(msg);
    } finally {
      setJsonModalSaving(false);
    }
  };

  const renderInput = (setting: AppSetting) => {
    const value = editedValues[setting.key] ?? '';

    if (setting.value_type === 'json') {
      const preview = value.length > 80 ? `${value.slice(0, 80)}…` : value;
      return (
        <div className="space-y-2">
          <div className="rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 text-sm font-mono text-gray-600 truncate">
            {preview || '—'}
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => openJsonModal(setting)}
          >
            <Edit3 className="w-4 h-4 mr-2" />
            Edit in popup
          </Button>
        </div>
      );
    }

    switch (setting.value_type) {
      case 'email':
        return (
          <Input
            type="email"
            value={value}
            onChange={(e) => handleValueChange(setting.key, e.target.value)}
            placeholder={`Enter ${setting.display_name.toLowerCase()}`}
          />
        );
      case 'number':
        return (
          <Input
            type="number"
            value={value}
            onChange={(e) => handleValueChange(setting.key, e.target.value)}
            placeholder={`Enter ${setting.display_name.toLowerCase()}`}
          />
        );
      case 'boolean':
        return (
          <select
            value={value}
            onChange={(e) => handleValueChange(setting.key, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Select...</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        );
      default:
        return (
          <Input
            type="text"
            value={value}
            onChange={(e) => handleValueChange(setting.key, e.target.value)}
            placeholder={`Enter ${setting.display_name.toLowerCase()}`}
          />
        );
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">App Settings</h1>
          <p className="text-gray-600 mt-1">
            Configure application settings like notifications, company info, and SEO
          </p>
        </div>
        <div className="flex items-center gap-3">
          {hasChanges && (
            <Button variant="outline" onClick={handleReset}>
              Discard Changes
            </Button>
          )}
          <Button onClick={handleSave} disabled={!hasChanges || saving}>
            {saving ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Settings by Category */}
      <div className="space-y-6">
        {categories.map(category => (
          <Card key={category.category} className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                {categoryIcons[category.category] || <Globe className="w-5 h-5" />}
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">
                  {category.display_name}
                </h2>
                <p className="text-sm text-gray-500">
                  {category.settings.length} setting(s)
                </p>
              </div>
            </div>

            <div className="space-y-6">
              {category.settings.map(setting => (
                <div key={setting.key} className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="md:col-span-1">
                    <label className="block text-sm font-medium text-gray-700">
                      {setting.display_name}
                    </label>
                    {setting.description && (
                      <p className="text-xs text-gray-500 mt-1">
                        {setting.description}
                      </p>
                    )}
                  </div>
                  <div className="md:col-span-2">
                    {renderInput(setting)}
                    {setting.updated_by_name && (
                      <p className="text-xs text-gray-400 mt-1">
                        Last updated by {setting.updated_by_name} on{' '}
                        {new Date(setting.updated_at).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {categories.length === 0 && (
        <Card className="p-12 text-center">
          <Globe className="w-12 h-12 mx-auto text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No settings found</h3>
          <p className="mt-2 text-gray-500">
            Settings will appear here once the database is migrated.
          </p>
        </Card>
      )}

      {/* JSON editor popup */}
      <Modal
        isOpen={jsonModalOpen}
        onClose={closeJsonModal}
        title={jsonModalSetting?.display_name}
        description={jsonModalSetting?.description ?? undefined}
        size="2xl"
      >
        <div className="space-y-4 -mt-2">
          <Textarea
            value={jsonModalValue}
            onChange={(e) => setJsonModalValue(e.target.value)}
            className="min-h-[320px] max-h-[70vh] overflow-y-auto font-mono text-sm resize-y"
            placeholder="{}"
            spellCheck={false}
          />
          {jsonModalError && (
            <p className="text-sm text-red-600">{jsonModalError}</p>
          )}
          <div className="flex justify-end gap-3 pt-2">
            <Button variant="outline" onClick={closeJsonModal} disabled={jsonModalSaving}>
              Cancel
            </Button>
            <Button onClick={saveJsonModal} disabled={jsonModalSaving}>
              {jsonModalSaving ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 mr-2" />
                  Save
                </>
              )}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

