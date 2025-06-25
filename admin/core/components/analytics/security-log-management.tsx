"use client";

import React, { useState, useEffect } from 'react';

interface SecurityLogConfig {
  zDriveEnabled: boolean;
  zDrivePath: string;
  maxLogSize: number; // in GB
  retentionDays: number;
  alertThreshold: number; // in MB
}

interface SecurityAlert {
  id: string;
  type: 'LOG_TRUNCATION' | 'SIZE_WARNING' | 'RETENTION_CLEANUP';
  message: string;
  timestamp: string;
  acknowledged: boolean;
  details: {
    originalSize: number;
    newSize: number;
    recordsRemoved: number;
    action: string;
    prevention: string;
  };
}

export const SecurityLogManagement: React.FC = () => {
  const [config, setConfig] = useState<SecurityLogConfig>({
    zDriveEnabled: true,
    zDrivePath: 'Z:\\SecurityLogs\\Plane',
    maxLogSize: 1.0, // 1GB default
    retentionDays: 365,
    alertThreshold: 900 // 900MB warning threshold
  });
  
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [logStats, setLogStats] = useState({
    currentSize: 0,
    recordCount: 0,
    oldestRecord: null as string | null,
    newestRecord: null as string | null
  });

  const [loading, setLoading] = useState(false);

  // Load configuration and alerts on mount
  useEffect(() => {
    fetchSecurityLogConfig();
    fetchSecurityAlerts();
    fetchLogStatistics();
  }, []);

  const fetchSecurityLogConfig = async () => {
    try {
      const response = await fetch('/api/security/log-config');
      if (response.ok) {
        const data = await response.json();
        setConfig(data);
      }
    } catch (error) {
      console.error('Failed to fetch security log config:', error);
    }
  };

  const fetchSecurityAlerts = async () => {
    try {
      const response = await fetch('/api/security/alerts');
      if (response.ok) {
        const data = await response.json();
        setAlerts(data.filter((alert: SecurityAlert) => !alert.acknowledged));
      }
    } catch (error) {
      console.error('Failed to fetch security alerts:', error);
    }
  };

  const fetchLogStatistics = async () => {
    try {
      const response = await fetch('/api/security/log-stats');
      if (response.ok) {
        const data = await response.json();
        setLogStats(data);
      }
    } catch (error) {
      console.error('Failed to fetch log statistics:', error);
    }
  };

  const updateConfig = async (newConfig: SecurityLogConfig) => {
    setLoading(true);
    try {
      const response = await fetch('/api/security/log-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
      });
      
      if (response.ok) {
        setConfig(newConfig);
        await fetchLogStatistics();
      }
    } catch (error) {
      console.error('Failed to update security log config:', error);
    } finally {
      setLoading(false);
    }
  };

  const acknowledgeAlert = async (alertId: string) => {
    try {
      const response = await fetch(`/api/security/alerts/${alertId}/acknowledge`, {
        method: 'POST'
      });
      
      if (response.ok) {
        setAlerts(alerts.filter(alert => alert.id !== alertId));
      }
    } catch (error) {
      console.error('Failed to acknowledge alert:', error);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getSizeWarningColor = () => {
    const currentSizeMB = logStats.currentSize / (1024 * 1024);
    const maxSizeMB = config.maxLogSize * 1024;
    const percentage = (currentSizeMB / maxSizeMB) * 100;
    
    if (percentage > 90) return 'text-red-600 bg-red-50';
    if (percentage > 75) return 'text-yellow-600 bg-yellow-50';
    return 'text-green-600 bg-green-50';
  };

  return (
    <div className="space-y-6">
      {/* Security Alerts */}
      {alerts.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h3 className="text-lg font-medium text-red-900 mb-3">
            🚨 Security Log Alerts ({alerts.length})
          </h3>
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div key={alert.id} className="bg-white border border-red-200 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-red-800">{alert.type.replace('_', ' ')}</h4>
                    <p className="text-sm text-red-700 mt-1">{alert.message}</p>
                    <div className="mt-2 text-xs text-red-600">
                      <p><strong>Action:</strong> {alert.details.action}</p>
                      <p><strong>Prevention:</strong> {alert.details.prevention}</p>
                      <p><strong>Time:</strong> {new Date(alert.timestamp).toLocaleString()}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => acknowledgeAlert(alert.id)}
                    className="ml-4 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                  >
                    Acknowledge
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Log Statistics */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Security Log Statistics</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className={`p-4 rounded-lg ${getSizeWarningColor()}`}>
            <h4 className="font-medium">Current Size</h4>
            <p className="text-2xl font-bold">{formatFileSize(logStats.currentSize)}</p>
            <p className="text-sm">
              {((logStats.currentSize / (config.maxLogSize * 1024 * 1024 * 1024)) * 100).toFixed(1)}% of limit
            </p>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-800">Record Count</h4>
            <p className="text-2xl font-bold text-blue-600">{logStats.recordCount.toLocaleString()}</p>
            <p className="text-sm text-blue-600">Total security events</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-800">Retention</h4>
            <p className="text-2xl font-bold text-gray-600">{config.retentionDays}</p>
            <p className="text-sm text-gray-600">Days configured</p>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg">
            <h4 className="font-medium text-purple-800">Z Drive Status</h4>
            <p className="text-lg font-bold text-purple-600">
              {config.zDriveEnabled ? 'ACTIVE' : 'DISABLED'}
            </p>
            <p className="text-sm text-purple-600">External logging</p>
          </div>
        </div>
      </div>

      {/* Configuration */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Security Log Configuration</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Z Drive Logging
            </label>
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={config.zDriveEnabled}
                onChange={(e) => setConfig({...config, zDriveEnabled: e.target.checked})}
                className="rounded border-gray-300"
              />
              <span className="text-sm text-gray-600">Enable Z drive logging</span>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Z Drive Path
            </label>
            <input
              type="text"
              value={config.zDrivePath}
              onChange={(e) => setConfig({...config, zDrivePath: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Z:\SecurityLogs\Plane"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Log Size (GB)
            </label>
            <input
              type="number"
              step="0.1"
              min="0.1"
              max="10"
              value={config.maxLogSize}
              onChange={(e) => setConfig({...config, maxLogSize: parseFloat(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Retention Period (Days)
            </label>
            <select
              value={config.retentionDays}
              onChange={(e) => setConfig({...config, retentionDays: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value={30}>30 Days</option>
              <option value={90}>90 Days</option>
              <option value={365}>1 Year</option>
            </select>
          </div>
        </div>
        
        <div className="mt-6 flex space-x-4">
          <button
            onClick={() => updateConfig(config)}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Updating...' : 'Update Configuration'}
          </button>
        </div>
      </div>

      {/* Log Retention Policy */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <h4 className="font-medium text-yellow-800 mb-2">📋 Log Retention Policy</h4>
        <div className="text-sm text-yellow-700 space-y-1">
          <p>• Logs exceeding {config.maxLogSize}GB will be automatically truncated</p>
          <p>• Truncation priority: 1 year → 90 days → 30 days → alert admin</p>
          <p>• All truncations create pending alerts requiring acknowledgment</p>
          <p>• Z drive logging provides external backup when available</p>
          <p>• Security logging never impacts core user functionality</p>
        </div>
      </div>
    </div>
  );
};
