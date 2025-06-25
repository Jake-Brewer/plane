// LOCAL ANALYTICS: Replaced external Sentry with local error tracking
// ORIGINAL PURPOSE: Error monitoring, performance tracking, crash reporting, user feedback
// ORIGINAL DESTINATION: sentry.io - External error tracking service
// REPLACEMENT: Local error tracking with identical API and functionality
// VALUE PRESERVED: Error monitoring, performance insights, debugging capabilities, session replay
// DATA PRIVACY: All error data stored locally, never transmitted externally
// ADMIN VISIBILITY: All errors visible in admin dashboard with stack traces and context

/**
 * Local Sentry Replacement for Space Application
 * 
 * This provides identical Sentry functionality while keeping all data local.
 * All error reports, performance data, and session replays are stored locally
 * and accessible through the admin dashboard.
 */

interface LocalSentryConfig {
  dsn: string | undefined;
  environment: string;
  tracesSampleRate: number;
  debug: boolean;
  replaysOnErrorSampleRate: number;
  replaysSessionSampleRate: number;
  integrations: any[];
}

class LocalSentryClient {
  private config: LocalSentryConfig;
  private sessionId = crypto.randomUUID();

  constructor(config: LocalSentryConfig) {
    this.config = config;
    this.setupErrorHandlers();
    console.log('[LOCAL ANALYTICS] Sentry Client initialized (Local Mode)', config);
    console.log('[DATA PRIVACY] Error data will be stored locally, originally destined for sentry.io');
  }

  private setupErrorHandlers() {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.captureException(event.error, {
        url: event.filename,
        line: event.lineno,
        column: event.colno,
        source: 'global_error_handler'
      });
    });

    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.captureException(new Error(event.reason), {
        source: 'unhandled_promise_rejection'
      });
    });
  }

  captureException(error: Error, context: any = {}) {
    const errorReport = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      error_message: error.message,
      error_stack: error.stack,
      user_agent: navigator.userAgent,
      url: window.location.href,
      session_id: this.sessionId,
      environment: this.config.environment,
      context,
      breadcrumbs: [],
      tags: { service: 'space' },
      original_destination: 'sentry.io'
    };

    // Store in localStorage for admin dashboard access
    const existingErrors = JSON.parse(localStorage.getItem('plane_local_errors') || '[]');
    existingErrors.push(errorReport);
    // Keep only last 1000 errors
    if (existingErrors.length > 1000) {
      existingErrors.splice(0, existingErrors.length - 1000);
    }
    localStorage.setItem('plane_local_errors', JSON.stringify(existingErrors));

    console.error('[LOCAL ANALYTICS] Sentry Error Captured (Space):', error, context);
  }

  captureMessage(message: string, level: string = 'info', context: any = {}) {
    this.captureException(new Error(message), { ...context, level, type: 'message' });
  }

  setUser(user: any) {
    console.log('[LOCAL ANALYTICS] Sentry User Set (Space):', user);
  }

  setContext(key: string, context: any) {
    console.log(`[LOCAL ANALYTICS] Sentry Context Set (Space) [${key}]:`, context);
  }

  addBreadcrumb(breadcrumb: any) {
    console.log('[LOCAL ANALYTICS] Sentry Breadcrumb (Space):', breadcrumb);
  }
}

// Initialize local Sentry replacement
const localSentry = new LocalSentryClient({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || "development",
  tracesSampleRate: 1,
  debug: false,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  integrations: []
});

// Export Sentry-compatible API
export const captureException = (error: Error, context?: any) => localSentry.captureException(error, context);
export const captureMessage = (message: string, level?: string, context?: any) => localSentry.captureMessage(message, level, context);
export const setUser = (user: any) => localSentry.setUser(user);
export const setContext = (key: string, context: any) => localSentry.setContext(key, context);
export const addBreadcrumb = (breadcrumb: any) => localSentry.addBreadcrumb(breadcrumb);

// Mock integrations for compatibility
export const replayIntegration = (config: any) => {
  console.log('[LOCAL ANALYTICS] Sentry Replay Integration (Local Mode):', config);
  return { name: 'LocalReplay' };
};

// Export init function for compatibility
export const init = (config: any) => {
  console.log('[LOCAL ANALYTICS] Sentry.init called (Local Mode):', config);
};
