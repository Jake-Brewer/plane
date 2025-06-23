# Nginx Directory Guide
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains Nginx reverse proxy configurations for Plane. It provides load balancing, SSL termination, static file serving, and routing between different application services (web, admin, space, API, live).

## Scope

### In-Scope
- Nginx reverse proxy configuration
- SSL/TLS termination and certificate management
- Load balancing between application instances
- Static file serving and caching
- Request routing and path-based routing
- Security headers and rate limiting
- Development and production configurations

### Out-of-Scope
- Application source code (see `web/`, `admin/`, `space/`, `apiserver/`, `live/`)
- Deployment orchestration (see `deploy/`)
- Application-specific configurations
- Database configurations

## Directory Structure

```
nginx/
├── FOLDER_GUIDE.md (This file)
├── nginx.conf.template         # Production Nginx configuration template
├── nginx.conf.dev             # Development Nginx configuration
├── nginx-single-docker-image.conf # Single Docker image configuration
├── env.sh                     # Environment variable processing script
├── Dockerfile                 # Production Nginx Docker image
├── Dockerfile.dev            # Development Nginx Docker image
├── .prettierignore           # Prettier formatting ignore file
└── [additional configs]       # Additional configuration files
```

## Key Features

### Reverse Proxy Configuration
- **Service Routing**: Route requests to appropriate backend services
  - `/` → Web application (Next.js)
  - `/admin/` → Admin panel (Next.js)
  - `/spaces/` → Public space interface (Next.js)
  - `/api/` → Backend API (Django)
  - `/live/` → Real-time service (Node.js WebSocket)
- **Load Balancing**: Distribute requests across multiple application instances
- **Health Checks**: Backend service health monitoring
- **Failover**: Automatic failover to healthy instances

### SSL/TLS Management
- **SSL Termination**: Handle SSL/TLS encryption and decryption
- **Certificate Management**: SSL certificate configuration and renewal
- **Security Headers**: HSTS, CSP, and other security headers
- **Protocol Configuration**: Modern TLS configuration with security best practices

### Performance Optimization
- **Static File Serving**: Efficient serving of static assets
- **Caching**: Browser and proxy caching configuration
- **Compression**: Gzip and Brotli compression for responses
- **Connection Optimization**: Keep-alive and connection pooling

### Security Features
- **Rate Limiting**: Protect against DDoS and abuse
- **Access Control**: IP-based access restrictions
- **Security Headers**: Comprehensive security header configuration
- **Request Filtering**: Filter malicious requests and payloads

## Configuration Files

### Production Configuration (`nginx.conf.template`)
- **Template-based**: Uses environment variables for dynamic configuration
- **Multi-service**: Routes to all Plane application services
- **SSL-ready**: Production-ready SSL configuration
- **Performance-optimized**: Optimized for production workloads
- **Security-hardened**: Security best practices implemented

### Development Configuration (`nginx.conf.dev`)
- **Development-friendly**: Optimized for development workflow
- **Hot-reload support**: Supports development server hot reloading
- **Debug features**: Enhanced logging and debugging features
- **Simplified SSL**: Development SSL configuration

### Single Image Configuration (`nginx-single-docker-image.conf`)
- **All-in-one**: Configuration for single Docker image deployment
- **Simplified routing**: Streamlined routing for containerized deployment
- **Container-optimized**: Optimized for Docker container environments
- **Resource-efficient**: Minimal resource usage configuration

## Routing Architecture

### Frontend Applications
```
/                    → Web application (port 3000)
/admin/*             → Admin panel (port 3001)
/spaces/*            → Public space (port 3002)
```

### Backend Services
```
/api/*               → Django API server (port 8000)
/live/*              → Real-time service (port 3003)
/static/*            → Static file serving
/media/*             → Media file serving
```

### WebSocket Support
- **WebSocket Proxying**: Proper WebSocket connection handling
- **Upgrade Headers**: Correct HTTP upgrade header handling
- **Connection Persistence**: Maintain WebSocket connections
- **Load Balancing**: WebSocket-aware load balancing

## Environment Configuration

### Environment Variables
- **BACKEND_HOST**: Backend API server hostname/IP
- **FRONTEND_HOST**: Frontend application hostname/IP
- **SSL_CERTIFICATE**: SSL certificate file path
- **SSL_PRIVATE_KEY**: SSL private key file path
- **DOMAIN_NAME**: Primary domain name for the application

### Dynamic Configuration
- **Template Processing**: Environment variable substitution in templates
- **Runtime Configuration**: Dynamic configuration based on environment
- **Multi-environment**: Support for development, staging, and production
- **Feature Toggles**: Environment-based feature enabling/disabling

## Security Configuration

### SSL/TLS Security
- **Modern TLS**: TLS 1.2+ with secure cipher suites
- **HSTS**: HTTP Strict Transport Security headers
- **Certificate Validation**: Proper certificate chain validation
- **OCSP Stapling**: OCSP stapling for certificate validation

### Application Security
- **CSP Headers**: Content Security Policy headers
- **XSS Protection**: Cross-site scripting protection headers
- **Clickjacking Protection**: X-Frame-Options headers
- **MIME Type Security**: X-Content-Type-Options headers

### Access Control
- **Rate Limiting**: Request rate limiting per IP
- **Geographic Blocking**: Country-based access control (if needed)
- **IP Whitelisting**: Allow/deny lists for IP addresses
- **User Agent Filtering**: Block malicious user agents

## Performance Tuning

### Caching Strategy
- **Static Assets**: Long-term caching for CSS, JS, images
- **API Responses**: Appropriate caching for API responses
- **Browser Caching**: Optimal browser cache configuration
- **Proxy Caching**: Nginx proxy cache for improved performance

### Compression Configuration
- **Gzip Compression**: Text-based content compression
- **Brotli Compression**: Modern compression algorithm support
- **Compression Levels**: Balanced compression vs CPU usage
- **MIME Type Configuration**: Appropriate compression by content type

### Connection Optimization
- **Keep-alive**: HTTP keep-alive connection optimization
- **Connection Pooling**: Backend connection pooling
- **Buffer Sizes**: Optimized buffer sizes for different content types
- **Timeout Configuration**: Appropriate timeout settings

## Development Workflow

### Local Development
1. **Configuration**: Use `nginx.conf.dev` for development
2. **SSL Setup**: Self-signed certificates for HTTPS testing
3. **Service Discovery**: Point to local development servers
4. **Hot Reload**: Support for frontend hot reloading

### Testing Configuration
- **Configuration Validation**: Test Nginx configuration syntax
- **SSL Testing**: Validate SSL certificate configuration
- **Load Testing**: Test reverse proxy performance
- **Security Testing**: Validate security header configuration

### Deployment Preparation
- **Template Validation**: Validate configuration templates
- **Environment Testing**: Test with production-like environment variables
- **Performance Benchmarking**: Benchmark configuration performance
- **Security Auditing**: Security audit of configuration

## Monitoring and Logging

### Access Logging
- **Request Logging**: Comprehensive request logging
- **Error Logging**: Error and warning log configuration
- **Performance Metrics**: Response time and throughput logging
- **Security Events**: Security-related event logging

### Health Monitoring
- **Service Health**: Backend service health monitoring
- **SSL Certificate**: Certificate expiration monitoring
- **Performance Metrics**: Nginx performance metrics
- **Error Rate Monitoring**: Error rate and anomaly detection

### Log Analysis
- **Log Aggregation**: Integration with log aggregation systems
- **Metrics Extraction**: Extract metrics from access logs
- **Alert Configuration**: Configure alerts for critical issues
- **Dashboard Integration**: Integration with monitoring dashboards

## Maintenance and Operations

### Regular Tasks
- **SSL Certificate Renewal**: Automated certificate renewal
- **Configuration Updates**: Regular configuration optimization
- **Security Updates**: Nginx version and security updates
- **Performance Tuning**: Ongoing performance optimization

### Troubleshooting
- **Configuration Debugging**: Debug configuration issues
- **SSL Troubleshooting**: SSL certificate and connection issues
- **Performance Issues**: Diagnose and resolve performance problems
- **Security Incidents**: Handle security-related incidents

### Backup and Recovery
- **Configuration Backup**: Regular backup of Nginx configurations
- **SSL Certificate Backup**: Secure backup of SSL certificates
- **Recovery Procedures**: Disaster recovery procedures
- **Rollback Procedures**: Configuration rollback procedures

---

**Note**: This directory contains Nginx reverse proxy configurations for Plane. For application source code, see the respective application directories (`web/`, `admin/`, `space/`, `apiserver/`, `live/`). For deployment configurations, see the `deploy/` directory. 