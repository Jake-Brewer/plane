"use client";

import React from 'react';
import { LocalAnalyticsDashboard } from '@/core/components/analytics/local-analytics-dashboard';

export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <LocalAnalyticsDashboard />
    </div>
  );
} 