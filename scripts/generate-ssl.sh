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
if [ ! -d "${SSL_DIR}" ]; then
    echo -e "📁 Creating SSL directory: ${SSL_DIR}"
    mkdir -p "${SSL_DIR}"
fi

# Check if certificates already exist
if [ -f "${SSL_DIR}/${CERT_FILE}" ] && [ -f "${SSL_DIR}/${KEY_FILE}" ]; then
    read -p "SSL certificates already exist. Overwrite? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "⏭️  Skipping certificate generation"
        exit 0
    fi
fi

# Generate private key
echo -e "🔑 Generating private key..."
openssl genrsa -out "${SSL_DIR}/${KEY_FILE}" 2048

# Generate certificate signing request
echo -e "📝 Generating certificate signing request..."
openssl req -new -key "${SSL_DIR}/${KEY_FILE}" -out "${SSL_DIR}/cert.csr" -subj "/C=${COUNTRY}/ST=${STATE}/L=${CITY}/O=${ORGANIZATION}/OU=${ORGANIZATIONAL_UNIT}/CN=${COMMON_NAME}"

# Generate self-signed certificate
echo -e "📜 Generating self-signed certificate..."
openssl x509 -req -in "${SSL_DIR}/cert.csr" -signkey "${SSL_DIR}/${KEY_FILE}" -out "${SSL_DIR}/${CERT_FILE}" -days ${DAYS_VALID} -extensions v3_req -extfile <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C=${COUNTRY}
ST=${STATE}
L=${CITY}
O=${ORGANIZATION}
OU=${ORGANIZATIONAL_UNIT}
CN=${COMMON_NAME}

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
