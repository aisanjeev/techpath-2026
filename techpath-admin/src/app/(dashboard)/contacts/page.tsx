'use client';

import { useEffect, useState, useCallback } from 'react';
import { Search, Mail, Phone, Building, MessageSquare } from 'lucide-react';
import toast from 'react-hot-toast';
import { PageHeader } from '@/components/layout/PageHeader';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { DataTable, Column } from '@/components/tables/DataTable';
import { StatusBadge } from '@/components/tables/StatusBadge';
import { Modal, ConfirmModal } from '@/components/ui/Modal';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Textarea } from '@/components/ui/Textarea';
import { FormField } from '@/components/ui/FormField';
import { contactsService } from '@/services/contacts.service';
import { formatDate, formatRelativeTime } from '@/lib/utils/format';
import type { ContactInquiry } from '@/types/api';

export default function ContactsPage() {
  const [contacts, setContacts] = useState<ContactInquiry[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [selectedContact, setSelectedContact] = useState<ContactInquiry | null>(null);
  const [detailModalOpen, setDetailModalOpen] = useState(false);
  const [deleteModal, setDeleteModal] = useState<{ open: boolean; contact: ContactInquiry | null }>({
    open: false,
    contact: null,
  });
  const [deleting, setDeleting] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [notes, setNotes] = useState('');
  const [newStatus, setNewStatus] = useState<string>('');
  const limit = 20;

  const fetchContacts = useCallback(async () => {
    setLoading(true);
    try {
      const response = await contactsService.list({
        skip: (page - 1) * limit,
        limit,
        status: statusFilter as 'new' | 'in_progress' | 'resolved' | 'closed' || undefined,
      });
      // Filter by search client-side since backend doesn't support search param
      let filtered = response.items;
      if (search) {
        const searchLower = search.toLowerCase();
        filtered = filtered.filter(
          (c) =>
            c.name.toLowerCase().includes(searchLower) ||
            c.email.toLowerCase().includes(searchLower) ||
            (c.subject && c.subject.toLowerCase().includes(searchLower))
        );
      }
      setContacts(filtered);
      setTotal(filtered.length);
    } catch (error) {
      console.error('Error fetching contacts:', error);
      toast.error('Failed to load contact inquiries');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => {
    fetchContacts();
  }, [fetchContacts]);

  const handleViewDetails = (contact: ContactInquiry) => {
    setSelectedContact(contact);
    setNotes(contact.notes || '');
    setNewStatus(contact.status);
    setDetailModalOpen(true);
  };

  const handleUpdateContact = async () => {
    if (!selectedContact) return;
    setUpdating(true);
    try {
      await contactsService.update(selectedContact.id, {
        status: newStatus as 'new' | 'in_progress' | 'resolved' | 'closed',
        notes,
      });
      toast.success('Contact updated successfully');
      setDetailModalOpen(false);
      fetchContacts();
    } catch (error) {
      console.error('Error updating contact:', error);
      toast.error('Failed to update contact');
    } finally {
      setUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteModal.contact) return;
    setDeleting(true);
    try {
      await contactsService.delete(deleteModal.contact.id);
      toast.success('Contact deleted successfully');
      setDeleteModal({ open: false, contact: null });
      fetchContacts();
    } catch (error) {
      console.error('Error deleting contact:', error);
      toast.error('Failed to delete contact');
    } finally {
      setDeleting(false);
    }
  };

  const columns: Column<ContactInquiry>[] = [
    {
      key: 'name',
      header: 'Contact',
      sortable: true,
      render: (item) => (
        <div>
          <div className="font-medium text-gray-900">{item.name}</div>
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Mail className="h-3 w-3" />
            {item.email}
          </div>
        </div>
      ),
    },
    {
      key: 'subject',
      header: 'Subject',
      render: (item) => (
        <div className="max-w-xs truncate" title={item.subject || item.message}>
          {item.subject || item.message.slice(0, 50) + '...'}
        </div>
      ),
    },
    {
      key: 'service_interest',
      header: 'Service',
      render: (item) => item.service_interest || '-',
    },
    {
      key: 'status',
      header: 'Status',
      render: (item) => <StatusBadge status={item.status} />,
    },
    {
      key: 'created_at',
      header: 'Received',
      sortable: true,
      render: (item) => (
        <div>
          <div className="text-sm">{formatDate(item.created_at)}</div>
          <div className="text-xs text-gray-500">{formatRelativeTime(item.created_at)}</div>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Contact Inquiries"
        description="Manage customer inquiries and requests"
      />

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search contacts..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="pl-10"
          />
        </div>
        <Select
          value={statusFilter}
          onChange={(e) => {
            setStatusFilter(e.target.value);
            setPage(1);
          }}
          className="w-40"
        >
          <option value="">All Status</option>
          <option value="new">New</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={contacts}
        loading={loading}
        keyExtractor={(item) => item.id}
        onView={handleViewDetails}
        onDelete={(item) => setDeleteModal({ open: true, contact: item })}
        pagination={{
          page,
          limit,
          total,
          onPageChange: setPage,
        }}
        emptyMessage="No contact inquiries found."
      />

      {/* Detail Modal */}
      <Modal
        isOpen={detailModalOpen}
        onClose={() => setDetailModalOpen(false)}
        title="Contact Details"
        size="lg"
      >
        {selectedContact && (
          <div className="space-y-6">
            {/* Contact Info */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Contact Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-teal-100 text-teal-700">
                    {selectedContact.name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div className="font-medium">{selectedContact.name}</div>
                    {selectedContact.company && (
                      <div className="flex items-center gap-1 text-sm text-gray-500">
                        <Building className="h-3 w-3" />
                        {selectedContact.company}
                      </div>
                    )}
                  </div>
                </div>
                <div className="flex flex-wrap gap-4 text-sm">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Mail className="h-4 w-4" />
                    <a href={`mailto:${selectedContact.email}`} className="hover:text-teal-600">
                      {selectedContact.email}
                    </a>
                  </div>
                  {selectedContact.phone && (
                    <div className="flex items-center gap-2 text-gray-600">
                      <Phone className="h-4 w-4" />
                      <a href={`tel:${selectedContact.phone}`} className="hover:text-teal-600">
                        {selectedContact.phone}
                      </a>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Message */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <MessageSquare className="h-4 w-4" />
                  Message
                </CardTitle>
              </CardHeader>
              <CardContent>
                {selectedContact.subject && (
                  <div className="mb-2 font-medium">{selectedContact.subject}</div>
                )}
                <p className="whitespace-pre-wrap text-gray-600">{selectedContact.message}</p>
                {selectedContact.service_interest && (
                  <div className="mt-3 rounded-lg bg-gray-50 p-2 text-sm">
                    <span className="font-medium">Interested in:</span>{' '}
                    {selectedContact.service_interest}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Status & Notes */}
            <div className="space-y-4">
              <FormField label="Status" htmlFor="status">
                <Select
                  id="status"
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                >
                  <option value="new">New</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </Select>
              </FormField>

              <FormField label="Notes" htmlFor="notes">
                <Textarea
                  id="notes"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add internal notes about this inquiry..."
                  rows={3}
                />
              </FormField>
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-3 border-t border-gray-200 pt-4">
              <Button variant="outline" onClick={() => setDetailModalOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleUpdateContact} loading={updating}>
                Update Contact
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, contact: null })}
        onConfirm={handleDelete}
        title="Delete Contact"
        description={`Are you sure you want to delete the inquiry from "${deleteModal.contact?.name}"? This action cannot be undone.`}
        confirmText="Delete"
        variant="danger"
        loading={deleting}
      />
    </div>
  );
}

