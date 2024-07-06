#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the .env file
ENV_FILE="$SCRIPT_DIR/../project/config/.env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo ".env file not found at $ENV_FILE"
    exit 1
fi

# Load variables from the .env file
set -o allexport
source "$ENV_FILE"
set -o allexport

# Define the path to the certificates directory
CERTIFICATES_DIR="$SCRIPT_DIR/../project/certificates"

# Resolve CERTIFICATES_DIR to an absolute path
CERTIFICATES_DIR="$(cd "$CERTIFICATES_DIR" && pwd)"


# Define the configuration file path
EXTFILE="$CERTIFICATES_DIR/extfile.cnf"

# Create the configuration file with the provided IP address
echo "subjectAltName = IP:$ip_address" > "$EXTFILE"

# Generate a private key with a passphrase
openssl genpkey -algorithm RSA -aes256 -out "$CERTIFICATES_DIR/private.key"

# Create a Certificate Signing Request (CSR)
openssl req -new -key "$CERTIFICATES_DIR/private.key" -out "$CERTIFICATES_DIR/server.csr"

# Generate the self-signed certificate
openssl x509 -req -days 365 -in "$CERTIFICATES_DIR/server.csr" -signkey "$CERTIFICATES_DIR/private.key" -out "$CERTIFICATES_DIR/server.crt" -extfile "$EXTFILE"

# Clean up the configuration file
rm "$EXTFILE"

echo "Certificate generation complete. Certificates are saved in $CERTIFICATES_DIR"
