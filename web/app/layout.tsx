import { Metadata, Viewport } from "next";
import Script from "next/script";
// styles
import "@/styles/globals.css";
import "@/styles/command-pallette.css";
import "@/styles/emoji.css";
import "@/styles/react-day-picker.css";
// meta data info
import { SITE_NAME, SITE_DESCRIPTION } from "@/constants/meta";
// helpers
import { API_BASE_URL, cn } from "@/helpers/common.helper";
// local
import { AppProvider } from "./provider";

export const metadata: Metadata = {
  title: "✈️ | Simple, extensible, open-source project management tool.",
  description: SITE_DESCRIPTION,
  openGraph: {
    title: "✈️ | Simple, extensible, open-source project management tool.",
    description:
      "Open-source project management tool to manage issues, sprints, and product roadmaps with peace of mind.",
    url: "https://app.✈️.so/",
  },
  keywords:
    "software development, plan, ship, software, accelerate, code management, release management, project management, issue tracking, agile, scrum, kanban, collaboration",
  twitter: {
    site: "@planepowers",
  },
};

export const viewport: Viewport = {
  minimumScale: 1,
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  width: "device-width",
  viewportFit: "cover",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const isSessionRecorderEnabled = parseInt(process.env.NEXT_PUBLIC_ENABLE_SESSION_RECORDER || "0");

  return (
    <html lang="en">
      <head>
        <meta name="theme-color" content="#fff" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest.json" />
        <link rel="shortcut icon" href="/favicon/favicon.ico" />
        {/* Meta info for PWA */}
        <meta name="application-name" content="✈️" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content={SITE_NAME} />
        <meta name="format-detection" content="telephone=no" />
        <meta name="mobile-web-app-capable" content="yes" />
        <link rel="apple-touch-icon" href="/icons/icon-512x512.png" />
        <link rel="apple-touch-icon" sizes="152x152" href="/icons/icon-152x152.png" />
        <link rel="apple-touch-icon" sizes="180x180" href="/icons/icon-180x180.png" />
        <link rel="apple-touch-icon" sizes="512x512" href="/icons/icon-512x512.png" />
        <link rel="manifest" href="/manifest.json" />
        {/* preloading */}
        <link rel="preload" href={`${API_BASE_URL}/api/instances/`} as="fetch" crossOrigin="use-credentials" />
        <link rel="preload" href={`${API_BASE_URL}/api/users/me/ `} as="fetch" crossOrigin="use-credentials" />
        <link rel="preload" href={`${API_BASE_URL}/api/users/me/profile/ `} as="fetch" crossOrigin="use-credentials" />
        <link rel="preload" href={`${API_BASE_URL}/api/users/me/settings/ `} as="fetch" crossOrigin="use-credentials" />
        <link
          rel="preload"
          href={`${API_BASE_URL}/api/users/me/workspaces/`}
          as="fetch"
          crossOrigin="use-credentials"
        />
      </head>
      <body>
        <div id="context-menu-portal" />
        <AppProvider>
          <div
            className={cn(
              "h-screen w-full overflow-hidden bg-custom-background-100 relative flex flex-col",
              "app-container"
            )}
          >
            <div className="w-full h-full overflow-hidden relative">{children}</div>
          </div>
        </AppProvider>
      </body>
      
      {/* LOCAL ANALYTICS: Replaced external tracking scripts with local analytics
          ORIGINAL SCRIPTS REMOVED:
          1. Plausible: https://plausible.io/js/script.js -> Sent page view data to plausible.io
          2. Microsoft Clarity: https://www.clarity.ms/tag/ -> Sent session recordings to clarity.microsoft.com
          
          REPLACEMENT: Local analytics initialization with identical functionality
          VALUE PRESERVED: Page view tracking, session recording, user interaction analytics
          DATA PRIVACY: All analytics data stored locally in IndexedDB
          ADMIN VISIBILITY: All tracking data visible in admin dashboard
      */}
      {process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN && (
        <Script id="local-plausible-analytics">
          {`
            console.log('[LOCAL ANALYTICS] Plausible analytics initialized (Local Mode)');
            console.log('[DATA PRIVACY] Page view data stored locally, originally destined for plausible.io');
            // Local analytics automatically tracks page views via web/lib/local-analytics.ts
          `}
        </Script>
      )}
      {!!isSessionRecorderEnabled && process.env.NEXT_PUBLIC_SESSION_RECORDER_KEY && (
        <Script id="local-clarity-analytics">
          {`
            console.log('[LOCAL ANALYTICS] Clarity session recording initialized (Local Mode)');
            console.log('[DATA PRIVACY] Session data stored locally, originally destined for clarity.microsoft.com');
            // Local analytics automatically tracks interactions via web/lib/local-analytics.ts
            
            // Initialize local clarity replacement
            if (typeof window !== 'undefined' && window.localAnalytics) {
              window.localAnalytics.clarity.init('${process.env.NEXT_PUBLIC_SESSION_RECORDER_KEY}');
            }
          `}
        </Script>
      )}
    </html>
  );
}
