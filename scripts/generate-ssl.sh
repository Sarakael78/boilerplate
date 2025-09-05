#!/bin/bash
# generate-ssl.sh - Generate self-signed SSL certificates for local HTTPS development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SSL_DIR="nginx/ssl"
CERT_FILE="cert.pem"
KEY_FILE="key.pem"
DAYS_VALID=365
COUNTRY="US"
STATE="California"
CITY="San Francisco"
ORGANIZATION="Development"
ORGANIZATIONAL_UNIT="IT Department"
COMMON_NAME="localhost"

echo -e "🔒 Generating SSL certificates for local development"

# Create SSL directory if it doesn't exist
if [ ! -d "" ]; then
    echo -e "📁 Creating SSL directory: "
    mkdir -p ""
fi

# Check if certificates already exist
if [ -f "/" ] && [ -f "/" ]; then
    read -p "SSL certificates already exist. Overwrite? (y/n): " -n 1 -r
    echo
    if [[ !  =~ ^[Yy]$ ]]; then
        echo -e "⏭️  Skipping certificate generation"
        exit 0
    fi
fi

# Generate private key
echo -e "🔑 Generating private key..."
openssl genrsa -out "/" 2048

# Generate certificate signing request
echo -e "📝 Generating certificate signing request..."
openssl req -new -key "/" -out "/cert.csr" -subj "/C=/ST=/L=/O=/OU=/CN="

# Generate self-signed certificate
echo -e "📜 Generating self-signed certificate..."
openssl x509 -req -in "/cert.csr" -signkey "/" -out "/" -days  -extensions v3_req -extfile <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C=
ST=
L=
O=
OU=
CN=

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
DNS.3 = 127.0.0.1
IP.1 = 127.0.0.1
IP.2 = ::1
EOF
)

# Clean up CSR file
rm "/cert.csr"

# Set appropriate permissions
chmod 600 "/"
chmod 644 "/"

echo -e "✅ SSL certificates generated successfully!"
echo
echo -e "📁 Certificate files created:"
echo -e "   🔑 Private Key: /"
echo -e "   📜 Certificate: /"
echo
echo -e "🚀 Next steps:"
echo -e "   1. Update your nginx configuration to use these certificates"
echo -e "   2. Add the certificate to your browser's trusted certificates (optional)"
echo -e "   3. Access your application via https://localhost"
echo
echo -e "⚠️  Warning: These are self-signed certificates for development only!"
echo -e "   Do not use in production environments."

# Display certificate information
echo
echo -e "📋 Certificate Information:"
openssl x509 -in "/" -text -noout | grep -A 5 "Subject:\|Validity\|DNS:"
