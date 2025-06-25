"use client";

import React, { useState, useEffect } from 'react';
import { observer } from "mobx-react";
import { Search, Mail, Eye, Shield, Clock, Filter, Download } from 'lucide-react';

interface RedirectedEmail {
  id: string;
  to_email: string;
  from_email: string;
  subject: string;
  html_content: string;
  text_content: string;
  email_type: string;
  original_destination: string;
  status: string;
  contains_sensitive_data: boolean;
  external_links_removed: boolean;
  created_at: string;
  intended_send_time: string;
}

interface EmailStats {
  total_emails: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  external_services_blocked: Record<string, number>;
  sensitive_emails: number;
}

const RedirectedEmailsPage = observer(() => {
  const [emails, setEmails] = useState<RedirectedEmail[]>([]);
  const [stats, setStats] = useState<EmailStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [selectedEmail, setSelectedEmail] = useState<RedirectedEmail | null>(null);
  const [showEmailModal, setShowEmailModal] = useState(false);

  const fetchEmails = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Simulate API call - replace with actual API endpoint
      const mockEmails: RedirectedEmail[] = [
        {
          id: '1',
          to_email: 'user@example.com',
          from_email: 'noreply@localhost',
          subject: 'Welcome to Project Management System',
          html_content: '<h1>Welcome!</h1><p>Your account has been created.</p>',
          text_content: 'Welcome! Your account has been created.',
          email_type: 'auth',
          original_destination: 'smtp.gmail.com',
          status: 'stored',
          contains_sensitive_data: true,
          external_links_removed: false,
          created_at: new Date().toISOString(),
          intended_send_time: new Date().toISOString(),
        },
        {
          id: '2',
          to_email: 'admin@example.com',
          from_email: 'system@localhost',
          subject: 'Issue Updated: Security Review',
          html_content: '<p>Issue #123 has been updated with new comments.</p>',
          text_content: 'Issue #123 has been updated with new comments.',
          email_type: 'notification',
          original_destination: 'api.sendgrid.com',
          status: 'stored',
          contains_sensitive_data: false,
          external_links_removed: true,
          created_at: new Date(Date.now() - 3600000).toISOString(),
          intended_send_time: new Date(Date.now() - 3600000).toISOString(),
        }
      ];

      const mockStats: EmailStats = {
        total_emails: mockEmails.length,
        by_type: {
          auth: 1,
          notification: 1,
          invitation: 0,
          system: 0,
          webhook: 0,
          other: 0,
        },
        by_status: {
          stored: 2,
          viewed: 0,
          exported: 0,
        },
        external_services_blocked: {
          'smtp.gmail.com': 1,
          'api.sendgrid.com': 1,
        },
        sensitive_emails: 1,
      };

      setEmails(mockEmails);
      setStats(mockStats);
      
    } catch (err) {
      console.error('Failed to fetch emails:', err);
      setError('Failed to load redirected emails. The email redirection service may still be initializing.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchEmails, 30000);
    return () => clearInterval(interval);
  }, []);

  const filteredEmails = emails.filter(email => {
    const matchesSearch = 
      email.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
      email.to_email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      email.from_email.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filterType === 'all' || email.email_type === filterType;
    
    return matchesSearch && matchesFilter;
  });

  const handleViewEmail = (email: RedirectedEmail) => {
    setSelectedEmail(email);
    setShowEmailModal(true);
  };

  const getEmailTypeColor = (type: string) => {
    const colors = {
      auth: 'bg-blue-100 text-blue-800',
      notification: 'bg-green-100 text-green-800',
      invitation: 'bg-purple-100 text-purple-800',
      system: 'bg-red-100 text-red-800',
      webhook: 'bg-yellow-100 text-yellow-800',
      other: 'bg-gray-100 text-gray-800',
    };
    return colors[type as keyof typeof colors] || colors.other;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading redirected emails...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">📧 Redirected Emails</h1>
        <p className="text-gray-600">
          All emails that would have been sent to external services are stored here locally for your privacy and security.
        </p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
            <div className="flex items-center">
              <Mail className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600">Total Emails</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_emails}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-green-600 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600">Sensitive Secured</p>
                <p className="text-2xl font-bold text-gray-900">{stats.sensitive_emails}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
            <div className="flex items-center">
              <Clock className="h-8 w-8 text-orange-600 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600">Services Blocked</p>
                <p className="text-2xl font-bold text-gray-900">
                  {Object.keys(stats.external_services_blocked).length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
            <div className="flex items-center">
              <Eye className="h-8 w-8 text-purple-600 mr-3" />
              <div>
                <p className="text-sm font-medium text-gray-600">Privacy Status</p>
                <p className="text-sm font-bold text-green-600">100% Local</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search and Filter */}
      <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                placeholder="Search emails by subject, recipient, or sender..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="all">All Types</option>
              <option value="auth">Authentication</option>
              <option value="notification">Notifications</option>
              <option value="invitation">Invitations</option>
              <option value="system">System</option>
              <option value="webhook">Webhooks</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <button
            onClick={fetchEmails}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Emails Table */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email Details
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Original Destination
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Security
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredEmails.map((email) => (
                <tr key={email.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div>
                      <p className="text-sm font-medium text-gray-900 truncate max-w-xs">
                        {email.subject}
                      </p>
                      <p className="text-sm text-gray-500">
                        To: {email.to_email}
                      </p>
                      <p className="text-sm text-gray-500">
                        From: {email.from_email}
                      </p>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getEmailTypeColor(email.email_type)}`}>
                      {email.email_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {email.original_destination}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-col gap-1">
                      {email.contains_sensitive_data && (
                        <span className="inline-flex items-center px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                          <Shield className="w-3 h-3 mr-1" />
                          Sensitive
                        </span>
                      )}
                      {email.external_links_removed && (
                        <span className="inline-flex items-center px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                          🔗 Links Removed
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {formatDate(email.created_at)}
                  </td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => handleViewEmail(email)}
                      className="inline-flex items-center px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-800"
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredEmails.length === 0 && !loading && (
          <div className="text-center py-12">
            <Mail className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <p className="text-gray-500">
              {searchTerm || filterType !== 'all' 
                ? 'No emails match your search criteria.' 
                : 'No redirected emails found. Emails will appear here as they are intercepted.'}
            </p>
          </div>
        )}
      </div>

      {/* Email Detail Modal */}
      {showEmailModal && selectedEmail && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Email Details
                  </h3>
                  <div className="space-y-1 text-sm text-gray-600">
                    <p><strong>Subject:</strong> {selectedEmail.subject}</p>
                    <p><strong>To:</strong> {selectedEmail.to_email}</p>
                    <p><strong>From:</strong> {selectedEmail.from_email}</p>
                    <p><strong>Type:</strong> 
                      <span className={`ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getEmailTypeColor(selectedEmail.email_type)}`}>
                        {selectedEmail.email_type}
                      </span>
                    </p>
                    <p><strong>Original Destination:</strong> {selectedEmail.original_destination}</p>
                    <p><strong>Date:</strong> {formatDate(selectedEmail.created_at)}</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowEmailModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-96">
              <div className="space-y-4">
                {selectedEmail.html_content && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">HTML Content:</h4>
                    <div 
                      className="border border-gray-200 rounded p-4 bg-gray-50 max-h-64 overflow-y-auto"
                      dangerouslySetInnerHTML={{ __html: selectedEmail.html_content }}
                    />
                  </div>
                )}
                
                {selectedEmail.text_content && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Text Content:</h4>
                    <div className="border border-gray-200 rounded p-4 bg-gray-50 max-h-32 overflow-y-auto">
                      <pre className="whitespace-pre-wrap text-sm">{selectedEmail.text_content}</pre>
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 bg-gray-50">
              <div className="flex justify-between items-center">
                <div className="text-sm text-gray-600">
                  🔒 This email was intercepted and stored locally for your privacy
                </div>
                <button
                  onClick={() => setShowEmailModal(false)}
                  className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

export default RedirectedEmailsPage; 