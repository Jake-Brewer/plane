// LOCAL ANALYTICS: Replaced external Sentry with local error tracking (Server-side)
// ORIGINAL PURPOSE: Server-side error monitoring, performance tracking, crash reporting
// ORIGINAL DESTINATION: sentry.io - External error tracking service
// REPLACEMENT: Local error tracking with file-based storage for server errors
// VALUE PRESERVED: Server error monitoring, performance insights, debugging capabilities
// DATA PRIVACY: All error data stored locally, never transmitted externally
// ADMIN VISIBILITY: All errors accessible through admin dashboard

/**
 * Local Sentry Replacement for Space Application (Server-side)
 * 
 * This provides server-side error tracking while keeping all data local.
 * Errors are logged to local files and made accessible through the admin dashboard.
 */

import { writeFileSync, existsSync, readFileSync, mkdirSync } from 'fs';
import { join } from 'path';

interface ServerErrorReport {
  id: string;
  timestamp: string;
  error_message: string;
  error_stack?: string;
  environment: string;
  context: any;
  tags: Record<string, string>;
  original_destination: string;
}

class LocalSentryServer {
  private logDir: string;
  private logFile: string;

  constructor() {
    this.logDir = join(process.cwd(), 'logs', 'local-analytics');
    this.logFile = join(this.logDir, 'space-errors.json');
    this.ensureLogDirectory();
    console.log('[LOCAL ANALYTICS] Sentry Server initialized (Local Mode)');
    console.log('[DATA PRIVACY] Server error data will be stored locally');
  }

  private ensureLogDirectory() {
    if (!existsSync(this.logDir)) {
      mkdirSync(this.logDir, { recursive: true });
    }
  }

  captureException(error: Error, context: any = {}) {
    const errorReport: ServerErrorReport = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      error_message: error.message,
      error_stack: error.stack,
      environment: process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || 'development',
      context,
      tags: { service: 'space-server' },
      original_destination: 'sentry.io'
    };

    this.writeErrorToFile(errorReport);
    console.error('[LOCAL ANALYTICS] Sentry Server Error Captured:', error, context);
  }

  captureMessage(message: string, level: string = 'info', context: any = {}) {
    this.captureException(new Error(message), { ...context, level, type: 'message' });
  }

  private writeErrorToFile(errorReport: ServerErrorReport) {
    try {
      let existingErrors: ServerErrorReport[] = [];
      if (existsSync(this.logFile)) {
        const fileContent = readFileSync(this.logFile, 'utf-8');
        existingErrors = JSON.parse(fileContent);
      }

      existingErrors.push(errorReport);
      
      // Keep only last 1000 errors
      if (existingErrors.length > 1000) {
        existingErrors.splice(0, existingErrors.length - 1000);
      }

      writeFileSync(this.logFile, JSON.stringify(existingErrors, null, 2));
    } catch (writeError) {
      console.error('[LOCAL ANALYTICS] Failed to write error to file:', writeError);
    }
  }
}

// Initialize local Sentry server
const localSentryServer = new LocalSentryServer();

// Export Sentry-compatible API
export const captureException = (error: Error, context?: any) => localSentryServer.captureException(error, context);
export const captureMessage = (message: string, level?: string, context?: any) => localSentryServer.captureMessage(message, level, context);

// Mock functions for compatibility
export const setUser = (user: any) => console.log('[LOCAL ANALYTICS] Sentry Server User Set:', user);
export const setContext = (key: string, context: any) => console.log(`[LOCAL ANALYTICS] Sentry Server Context Set [${key}]:`, context);
export const addBreadcrumb = (breadcrumb: any) => console.log('[LOCAL ANALYTICS] Sentry Server Breadcrumb:', breadcrumb);

// Export init function for compatibility
export const init = (config: any) => {
  console.log('[LOCAL ANALYTICS] Sentry Server.init called (Local Mode):', config);
};
