"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { AlertTriangle, Shield, Eye, Download, Search, Filter } from 'lucide-react';

// Types for exfiltration monitoring
interface ExfiltrationAttempt {
  id: string;
  timestamp: string;
  type: string;
  destination: string;
  data_summary: string;
  data_size: number;
  source_function: string;
  stack_trace: string;
  user_id?: string;
  workspace_id?: string;
  project_id?: string;
  blocked: boolean;
  local_alternative_used: boolean;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  metadata: Record<string, any>;
}

interface ExfiltrationStats {
  total_attempts: number;
  blocked_attempts: number;
  by_type: Record<string, number>;
  by_risk_level: Record<string, number>;
  by_destination: Record<string, number>;
  recent_24h: number;
}

// Mock data for demonstration (in production, this would come from the prevention module)
const mockStats: ExfiltrationStats = {
  total_attempts: 247,
  blocked_attempts: 231,
  by_type: {
    'ANALYTICS': 89,
    'CDN_ASSET': 67,
    'ERROR_REPORTING': 34,
    'EMAIL': 23,
    'SOCIAL_MEDIA': 18,
    'WEBHOOK': 16
  },
  by_risk_level: {
    'CRITICAL': 12,
    'HIGH': 45,
    'MEDIUM': 134,
    'LOW': 56
  },
  by_destination: {
    'google-analytics.com': 45,
    'sentry.io': 34,
    'plausible.io': 28,
    'clarity.ms': 21,
    'jsdelivr.net': 19
  },
  recent_24h: 89
};

const mockAttempts: ExfiltrationAttempt[] = [
  {
    id: '1',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    type: 'ANALYTICS',
    destination: 'google-analytics.com',
    data_summary: 'Object(5 keys): event, user_id, timestamp, properties, session_id',
    data_size: 1247,
    source_function: 'trackPageView at analytics.js:45',
    stack_trace: 'Error: Blocked\n    at fetch...',
    blocked: true,
    local_alternative_used: true,
    risk_level: 'HIGH',
    metadata: {
      user_agent: 'Mozilla/5.0...',
      url: 'https://app.plane.so/dashboard'
    }
  },
  {
    id: '2',
    timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    type: 'ERROR_REPORTING',
    destination: 'sentry.io',
    data_summary: 'Object(8 keys): error, user, environment, release, tags...',
    data_size: 2341,
    source_function: 'captureException at sentry.js:123',
    stack_trace: 'TypeError: Cannot read property...',
    blocked: true,
    local_alternative_used: true,
    risk_level: 'CRITICAL',
    metadata: {
      user_agent: 'Mozilla/5.0...',
      url: 'https://app.plane.so/projects'
    }
  },
  {
    id: '3',
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    type: 'CDN_ASSET',
    destination: 'jsdelivr.net',
    data_summary: 'String(0 chars): ',
    data_size: 0,
    source_function: 'loadScript at component.tsx:67',
    stack_trace: 'Error: External script blocked...',
    blocked: true,
    local_alternative_used: false,
    risk_level: 'MEDIUM',
    metadata: {
      user_agent: 'Mozilla/5.0...',
      url: 'https://app.plane.so/issues'
    }
  }
];

export default function ExfiltrationMonitorPage() {
  const [stats, setStats] = useState<ExfiltrationStats>(mockStats);
  const [attempts, setAttempts] = useState<ExfiltrationAttempt[]>(mockAttempts);
  const [filteredAttempts, setFilteredAttempts] = useState<ExfiltrationAttempt[]>(mockAttempts);
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [blockedFilter, setBlockedFilter] = useState('ALL');
  const [selectedAttempt, setSelectedAttempt] = useState<ExfiltrationAttempt | null>(null);

  // Filter attempts based on search and filters
  useEffect(() => {
    let filtered = attempts;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(attempt =>
        attempt.destination.toLowerCase().includes(searchTerm.toLowerCase()) ||
        attempt.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        attempt.data_summary.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Type filter
    if (typeFilter !== 'ALL') {
      filtered = filtered.filter(attempt => attempt.type === typeFilter);
    }

    // Risk filter
    if (riskFilter !== 'ALL') {
      filtered = filtered.filter(attempt => attempt.risk_level === riskFilter);
    }

    // Blocked filter
    if (blockedFilter !== 'ALL') {
      filtered = filtered.filter(attempt => 
        blockedFilter === 'BLOCKED' ? attempt.blocked : !attempt.blocked
      );
    }

    setFilteredAttempts(filtered);
  }, [attempts, searchTerm, typeFilter, riskFilter, blockedFilter]);

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
      case 'HIGH': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'ANALYTICS': return 'bg-blue-100 text-blue-800';
      case 'ERROR_REPORTING': return 'bg-red-100 text-red-800';
      case 'CDN_ASSET': return 'bg-purple-100 text-purple-800';
      case 'EMAIL': return 'bg-green-100 text-green-800';
      case 'SOCIAL_MEDIA': return 'bg-pink-100 text-pink-800';
      case 'WEBHOOK': return 'bg-indigo-100 text-indigo-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const generateReport = async () => {
    // In production, this would call the prevention module's generateReport method
    const report = `# Data Exfiltration Prevention Report

**Generated**: ${new Date().toISOString()}

## Summary Statistics
- **Total Attempts**: ${stats.total_attempts}
- **Blocked Attempts**: ${stats.blocked_attempts}
- **Success Rate**: ${((stats.blocked_attempts / stats.total_attempts) * 100).toFixed(1)}%
- **Recent 24h**: ${stats.recent_24h}

## By Risk Level
${Object.entries(stats.by_risk_level).map(([level, count]) => `- **${level}**: ${count}`).join('\n')}

## By Type
${Object.entries(stats.by_type).map(([type, count]) => `- **${type}**: ${count}`).join('\n')}

## Top Destinations
${Object.entries(stats.by_destination).map(([dest, count]) => `- **${dest}**: ${count}`).join('\n')}
`;

    const blob = new Blob([report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exfiltration-report-${new Date().toISOString().split('T')[0]}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Data Exfiltration Monitor</h1>
          <p className="text-gray-600 mt-2">
            Real-time monitoring of data exfiltration attempts and security measures
          </p>
        </div>
        <Button onClick={generateReport} className="flex items-center gap-2">
          <Download className="w-4 h-4" />
          Generate Report
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Attempts</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_attempts}</div>
            <p className="text-xs text-muted-foreground">
              {stats.recent_24h} in last 24h
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Blocked</CardTitle>
            <Shield className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats.blocked_attempts}</div>
            <p className="text-xs text-muted-foreground">
              {((stats.blocked_attempts / stats.total_attempts) * 100).toFixed(1)}% success rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Risks</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.by_risk_level.CRITICAL || 0}</div>
            <p className="text-xs text-muted-foreground">
              Require immediate attention
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Local Alternatives</CardTitle>
            <Shield className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {attempts.filter(a => a.local_alternative_used).length}
            </div>
            <p className="text-xs text-muted-foreground">
              Functionality preserved
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Risk Level Distribution */}
      <Card>
        <CardHeader>
          <CardTitle>Risk Level Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(stats.by_risk_level).map(([level, count]) => (
              <div key={level} className="text-center">
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRiskLevelColor(level)}`}>
                  {level}
                </div>
                <div className="text-2xl font-bold mt-2">{count}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="w-4 h-4" />
            Filters & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search attempts..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Types</SelectItem>
                {Object.keys(stats.by_type).map(type => (
                  <SelectItem key={type} value={type}>{type}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={riskFilter} onValueChange={setRiskFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by risk" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Risk Levels</SelectItem>
                <SelectItem value="CRITICAL">Critical</SelectItem>
                <SelectItem value="HIGH">High</SelectItem>
                <SelectItem value="MEDIUM">Medium</SelectItem>
                <SelectItem value="LOW">Low</SelectItem>
              </SelectContent>
            </Select>

            <Select value={blockedFilter} onValueChange={setBlockedFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Attempts</SelectItem>
                <SelectItem value="BLOCKED">Blocked Only</SelectItem>
                <SelectItem value="ALLOWED">Allowed Only</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Attempts List */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Exfiltration Attempts ({filteredAttempts.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredAttempts.map((attempt) => (
              <div
                key={attempt.id}
                className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
                onClick={() => setSelectedAttempt(attempt)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge className={getTypeColor(attempt.type)}>
                        {attempt.type}
                      </Badge>
                      <Badge className={getRiskLevelColor(attempt.risk_level)}>
                        {attempt.risk_level}
                      </Badge>
                      {attempt.blocked && (
                        <Badge variant="destructive">BLOCKED</Badge>
                      )}
                      {attempt.local_alternative_used && (
                        <Badge variant="secondary">LOCAL ALT</Badge>
                      )}
                    </div>
                    <div className="text-sm text-gray-600 mb-1">
                      <strong>Destination:</strong> {attempt.destination}
                    </div>
                    <div className="text-sm text-gray-600 mb-1">
                      <strong>Data:</strong> {attempt.data_summary}
                    </div>
                    <div className="text-sm text-gray-600">
                      <strong>Size:</strong> {attempt.data_size} bytes
                    </div>
                  </div>
                  <div className="text-right text-sm text-gray-500">
                    {new Date(attempt.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
            
            {filteredAttempts.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No exfiltration attempts found matching your filters.
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Detailed View Modal */}
      {selectedAttempt && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Exfiltration Attempt Details</h2>
                <Button
                  variant="ghost"
                  onClick={() => setSelectedAttempt(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ×
                </Button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold mb-2">Basic Information</h3>
                  <div className="space-y-2 text-sm">
                    <div><strong>ID:</strong> {selectedAttempt.id}</div>
                    <div><strong>Timestamp:</strong> {new Date(selectedAttempt.timestamp).toLocaleString()}</div>
                    <div><strong>Type:</strong> 
                      <Badge className={`ml-2 ${getTypeColor(selectedAttempt.type)}`}>
                        {selectedAttempt.type}
                      </Badge>
                    </div>
                    <div><strong>Risk Level:</strong> 
                      <Badge className={`ml-2 ${getRiskLevelColor(selectedAttempt.risk_level)}`}>
                        {selectedAttempt.risk_level}
                      </Badge>
                    </div>
                    <div><strong>Destination:</strong> {selectedAttempt.destination}</div>
                    <div><strong>Data Size:</strong> {selectedAttempt.data_size} bytes</div>
                    <div><strong>Blocked:</strong> {selectedAttempt.blocked ? 'Yes' : 'No'}</div>
                    <div><strong>Local Alternative:</strong> {selectedAttempt.local_alternative_used ? 'Yes' : 'No'}</div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold mb-2">Source Information</h3>
                  <div className="space-y-2 text-sm">
                    <div><strong>Source Function:</strong> 
                      <code className="bg-gray-100 px-2 py-1 rounded text-xs ml-2">
                        {selectedAttempt.source_function}
                      </code>
                    </div>
                    <div><strong>User Agent:</strong> 
                      <code className="bg-gray-100 px-2 py-1 rounded text-xs ml-2 block mt-1">
                        {selectedAttempt.metadata.user_agent}
                      </code>
                    </div>
                    <div><strong>URL:</strong> 
                      <code className="bg-gray-100 px-2 py-1 rounded text-xs ml-2 block mt-1">
                        {selectedAttempt.metadata.url}
                      </code>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6">
                <h3 className="font-semibold mb-2">Data Summary</h3>
                <code className="bg-gray-100 p-3 rounded text-sm block">
                  {selectedAttempt.data_summary}
                </code>
              </div>
              
              <div className="mt-6">
                <h3 className="font-semibold mb-2">Stack Trace</h3>
                <pre className="bg-gray-100 p-3 rounded text-xs overflow-x-auto">
                  {selectedAttempt.stack_trace}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 