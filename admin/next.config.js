/** @type {import('next').NextConfig} */

const nextConfig = {
  trailingSlash: true,
  reactStrictMode: false,
  swcMinify: true,
  output: "standalone",
  images: {
    unoptimized: true,
  },
  basePath: process.env.NEXT_PUBLIC_ADMIN_BASE_PATH || "",
  
  // Enhanced configuration for better chunk loading and performance
  experimental: {
    optimizeCss: true,
    optimizeServerReact: true,
    // Reduce memory usage and improve build performance
    webpackBuildWorker: true,
  },
  
  // Webpack optimizations for chunk loading
  webpack: (config, { dev, isServer }) => {
    // Optimize chunk splitting for better loading
    if (!dev && !isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          default: {
            minChunks: 1,
            priority: -20,
            reuseExistingChunk: true,
            maxAsyncRequests: 10,
            maxInitialRequests: 5,
          },
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            priority: -10,
            chunks: 'all',
            maxAsyncRequests: 10,
          },
          // Separate chunk for admin-specific components
          admin: {
            name: 'admin',
            test: /[\\/]admin[\\/]/,
            priority: 10,
            chunks: 'all',
          },
        },
      };
      
      // Increase chunk loading timeout to prevent premature timeouts
      config.output.chunkLoadTimeout = 120000; // 2 minutes instead of default 30s
    }
    
    // Optimize module resolution
    config.resolve.alias = {
      ...config.resolve.alias,
      // Add aliases to reduce bundle size
      '@': require('path').resolve(__dirname, './'),
    };
    
    return config;
  },
  
  // Enhanced headers for better caching
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
        ],
      },
    ];
  },
  
  // Optimize build performance
  onDemandEntries: {
    // Keep pages in memory longer to reduce rebuild time
    maxInactiveAge: 60 * 1000, // 1 minute
    pagesBufferLength: 5,
  },
  
  // Compress pages for better performance
  compress: true,
  
  // Enable source maps in development for better debugging
  productionBrowserSourceMaps: false, // Disable in production for smaller bundles
};

module.exports = nextConfig;
