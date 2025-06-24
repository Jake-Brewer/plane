#!/bin/bash
# E2E Test: List Workspaces (Read-Only)
# Safely verifies that the Plane API is up and can return workspaces.
# No side effects. Can be run repeatedly.

set -e

API_URL="http://localhost:8000/api/workspaces/"

# Optionally, allow override via env
if [[ -n "$PLANE_API_URL" ]]; then
  API_URL="$PLANE_API_URL/api/workspaces/"
fi

# Print test header
cat <<EOF
========================================
E2E Test: List Workspaces (Read-Only)
Endpoint: $API_URL
========================================
EOF

# Make the API call
response=$(curl -s -w "\n%{http_code}" "$API_URL")
body=$(echo "$response" | head -n -1)
status=$(echo "$response" | tail -n1)

# Check HTTP status
if [[ "$status" != "200" ]]; then
  echo "[FAIL] API did not return 200 OK. Status: $status"
  exit 1
fi

# Check for expected JSON structure (should contain 'results' or be a list)
if echo "$body" | grep -q '"results"' || echo "$body" | grep -q '\['; then
  echo "[PASS] Workspaces listed successfully."
else
  echo "[FAIL] Response does not contain expected workspace data."
  echo "Response: $body"
  exit 1
fi

exit 0 