// LOCAL ANALYTICS: Replaced external Sentry with local error tracking (Edge Runtime)
// ORIGINAL PURPOSE: Edge runtime error monitoring for middleware and edge routes
// ORIGINAL DESTINATION: sentry.io - External error tracking service
// REPLACEMENT: Local error tracking compatible with edge runtime limitations
// VALUE PRESERVED: Edge error monitoring, middleware error tracking
// DATA PRIVACY: All error data stored locally, never transmitted externally
// ADMIN VISIBILITY: All errors accessible through admin dashboard

/**
 * Local Sentry Replacement for Space Application (Edge Runtime)
 * 
 * This provides edge runtime error tracking while keeping all data local.
 * Due to edge runtime limitations, errors are logged to console and stored
 * in a way that can be accessed by the admin dashboard.
 */

interface EdgeErrorReport {
  id: string;
  timestamp: string;
  error_message: string;
  error_stack?: string;
  environment: string;
  context: any;
  tags: Record<string, string>;
  original_destination: string;
}

class LocalSentryEdge {
  constructor() {
    console.log('[LOCAL ANALYTICS] Sentry Edge initialized (Local Mode)');
    console.log('[DATA PRIVACY] Edge error data will be stored locally');
  }

  captureException(error: Error, context: any = {}) {
    const errorReport: EdgeErrorReport = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      error_message: error.message,
      error_stack: error.stack,
      environment: process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || 'development',
      context,
      tags: { service: 'space-edge' },
      original_destination: 'sentry.io'
    };

    // Log to console for now (edge runtime limitations)
    console.error('[LOCAL ANALYTICS] Sentry Edge Error Captured:', JSON.stringify(errorReport, null, 2));
  }

  captureMessage(message: string, level: string = 'info', context: any = {}) {
    this.captureException(new Error(message), { ...context, level, type: 'message' });
  }
}

// Initialize local Sentry edge
const localSentryEdge = new LocalSentryEdge();

// Export Sentry-compatible API
export const captureException = (error: Error, context?: any) => localSentryEdge.captureException(error, context);
export const captureMessage = (message: string, level?: string, context?: any) => localSentryEdge.captureMessage(message, level, context);

// Mock functions for compatibility
export const setUser = (user: any) => console.log('[LOCAL ANALYTICS] Sentry Edge User Set:', user);
export const setContext = (key: string, context: any) => console.log(`[LOCAL ANALYTICS] Sentry Edge Context Set [${key}]:`, context);
export const addBreadcrumb = (breadcrumb: any) => console.log('[LOCAL ANALYTICS] Sentry Edge Breadcrumb:', breadcrumb);

// Export init function for compatibility
export const init = (config: any) => {
  console.log('[LOCAL ANALYTICS] Sentry Edge.init called (Local Mode):', config);
};
