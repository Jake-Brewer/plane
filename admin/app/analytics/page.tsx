"use client";

import { FC } from "react";
import { LocalAnalyticsDashboard } from "@/core/components/analytics/local-analytics-dashboard";

const AnalyticsPage: FC = () => {
  return (
    <div className="h-full w-full">
      <LocalAnalyticsDashboard />
    </div>
  );
};

export default AnalyticsPage; 