'use client';

import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { Save, RefreshCw, Mail, Building2, Globe, BarChart3 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { settingsService, SettingsCategory, AppSetting } from '@/services/settings.service';

// Category icons
const categoryIcons: Record<string, React.ReactNode> = {
  email: <Mail className="w-5 h-5" />,
  general: <Building2 className="w-5 h-5" />,
  seo: <BarChart3 className="w-5 h-5" />,
};

export default function GeneralSettingsPage() {
  const [categories, setCategories] = useState<SettingsCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editedValues, setEditedValues] = useState<Record<string, string>>({});
  const [hasChanges, setHasChanges] = useState(false);

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

  const renderInput = (setting: AppSetting) => {
    const value = editedValues[setting.key] ?? '';
    
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
    </div>
  );
}

