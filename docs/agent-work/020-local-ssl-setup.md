# Local SSL Setup for HTTPS Development

## Overview

This document explains how to set up SSL certificates for local HTTPS development using self-signed certificates. This is useful for testing features that require HTTPS, such as secure cookies, service workers, or OAuth integrations.

## Quick Start

### Generate SSL Certificates

1. **Run the SSL generation script:**
   `ash
./scripts/generate-ssl.sh
`

   This script will:
   - Create the
     ginx/ssl/ directory if it doesn't exist
   - Generate a private key (key.pem)
   - Generate a self-signed certificate (cert.pem)
   - Set appropriate file permissions

2. **Update your nginx configuration** to use the certificates (see nginx configuration section below)

3. **Restart your development environment:**
   `ash
make dev
`

4. **Access your application via HTTPS:**
   - Frontend: https://localhost:3000
   - Backend API: https://localhost:8000

## Certificate Details

### Generated Files

- **
  ginx/ssl/key.pem** - Private key (2048-bit RSA)
- **
  ginx/ssl/cert.pem** - Self-signed certificate (valid for 365 days)

### Certificate Properties

- **Valid for:** 365 days
- **Common Name:** localhost
- **Subject Alternative Names:**
  - DNS: localhost, \*.localhost
  - IP: 127.0.0.1, ::1
- **Key Usage:** Key encipherment, data encipherment
- **Extended Key Usage:** Server authentication

## Nginx Configuration

### HTTPS Server Block

Add the following to your nginx configuration:

`
ginx
server {
listen 443 ssl http2;
server_name localhost;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;

    # Proxy configuration (same as HTTP)
    location / {
        proxy_pass http://frontend:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade ;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host System.Management.Automation.Internal.Host.InternalHost;
        proxy_set_header X-Real-IP ;
        proxy_set_header X-Forwarded-For ;
        proxy_set_header X-Forwarded-Proto ;
        proxy_cache_bypass ;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Host System.Management.Automation.Internal.Host.InternalHost;
        proxy_set_header X-Real-IP ;
        proxy_set_header X-Forwarded-For ;
        proxy_set_header X-Forwarded-Proto ;
    }

}

# Redirect HTTP to HTTPS

server {
listen 80;
server_name localhost;
return 301 https://;
}
`

### Docker Compose Volume Mapping

Ensure your docker-compose.yml includes the SSL volume mapping:

`yaml
services:
  nginx:
    # ... other configuration
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl:ro  # Add this line
`

## Browser Setup

### Accept Self-Signed Certificate

When first accessing https://localhost, your browser will show a security warning because the certificate is self-signed.

**Chrome/Edge:**

1. Click "Advanced"
2. Click "Proceed to localhost (unsafe)"

**Firefox:**

1. Click "Advanced"
2. Click "Accept the Risk and Continue"

### Add Certificate to Trusted Store (Optional)

For a better development experience, you can add the certificate to your system's trusted certificate store:

#### macOS

`ash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain nginx/ssl/cert.pem
`

#### Windows

1. Double-click
   ginx/ssl/cert.pem
2. Click "Install Certificate"
3. Choose "Local Machine" and click "Next"
4. Select "Place all certificates in the following store"
5. Click "Browse" and select "Trusted Root Certification Authorities"
6. Click "Next" then "Finish"

#### Linux (Ubuntu/Debian)

`ash
sudo cp nginx/ssl/cert.pem /usr/local/share/ca-certificates/localhost.crt
sudo update-ca-certificates
`

## Environment Variables

Update your environment variables to use HTTPS URLs:

### Frontend (.env.local)

`ash
NEXT_PUBLIC_API_URL=https://localhost:8000
`

### Backend (.env)

`ash
FRONTEND_URL=https://localhost:3000
`

## Development Workflow

### Standard Workflow

1. Generate certificates: ./scripts/generate-ssl.sh
2. Update nginx configuration for HTTPS
3. Start development: make dev
4. Access via HTTPS: https://localhost

### Certificate Renewal

Certificates are valid for 365 days. To renew:

1. Run ./scripts/generate-ssl.sh
2. Choose "y" to overwrite existing certificates
3. Restart your development environment

## Troubleshooting

### Common Issues

**Certificate not trusted:**

- Solution: Add certificate to browser/system trust store (see browser setup)

**Mixed content warnings:**

- Cause: HTTP resources loaded on HTTPS pages
- Solution: Ensure all API calls and assets use HTTPS URLs

**Port conflicts:**

- Cause: Another service using port 443
- Solution: Stop conflicting service or change nginx HTTPS port

**Permission denied errors:**

- Cause: Insufficient permissions to create SSL files
- Solution: Ensure user has write access to
  ginx/ssl/ directory

### Verification Commands

**Check certificate validity:**
`ash
openssl x509 -in nginx/ssl/cert.pem -text -noout
`

**Test SSL connection:**
`ash
openssl s_client -connect localhost:443 -servername localhost
`

**Verify nginx configuration:**
`ash
nginx -t
`

## Security Considerations

### Development Only

⚠️ **Important:** These are self-signed certificates for development only!

- **Do not use in production**
- **Do not commit certificates to version control**
- **Regenerate certificates periodically**
- **Use proper CA-signed certificates for staging/production**

### Best Practices

1. **Keep certificates local** - Add
   ginx/ssl/ to .gitignore
2. **Regenerate regularly** - Monthly or when working on security features
3. **Use HTTPS for all development** - Matches production environment
4. **Test security headers** - Verify HSTS, CSP, and other headers work correctly

## Integration with CI/CD

For automated testing environments, consider:

`ash

# In CI script

if [ ! -f "nginx/ssl/cert.pem" ]; then
./scripts/generate-ssl.sh
fi
`

## Additional Resources

- [Let's Encrypt](https://letsencrypt.org/) for production certificates
- [mkcert](https://github.com/FiloSottile/mkcert) alternative tool for local certificates
- [SSL Configuration Generator](https://ssl-config.mozilla.org/) for nginx SSL settings
