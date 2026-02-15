#!/usr/bin/env bash
set -euo pipefail

# Download a Dynamics 365 / Dataverse solution as a zip using PAC CLI.
# Required env vars:
#   DATAVERSE_ENV_URL   e.g. https://org.crm.dynamics.com
#   SOLUTION_NAME       unique solution name in Dataverse
# Optional:
#   SOLUTION_MANAGED    true|false (default: false)
#   OUTPUT_DIR          folder path (default: .)
#   OUTPUT_FILE         explicit filename (default: solution_1_0_0_0.zip)

: "${DATAVERSE_ENV_URL:?Set DATAVERSE_ENV_URL, e.g. https://org.crm.dynamics.com}"
: "${SOLUTION_NAME:?Set SOLUTION_NAME (solution unique name in Dataverse)}"

SOLUTION_MANAGED="${SOLUTION_MANAGED:-false}"
OUTPUT_DIR="${OUTPUT_DIR:-.}"
mkdir -p "$OUTPUT_DIR"

if [[ "$SOLUTION_MANAGED" != "true" && "$SOLUTION_MANAGED" != "false" ]]; then
  echo "SOLUTION_MANAGED must be true or false"
  exit 1
fi

if ! command -v pac >/dev/null 2>&1; then
  echo "PAC CLI not found. Install with: dotnet tool install --global Microsoft.PowerApps.CLI.Tool"
  exit 1
fi

if [[ -z "${OUTPUT_FILE:-}" ]]; then
  OUTPUT_FILE="solution_1_0_0_0.zip"
fi

OUT_PATH="${OUTPUT_DIR%/}/$OUTPUT_FILE"

echo "Authenticating to $DATAVERSE_ENV_URL ..."
pac auth create --url "$DATAVERSE_ENV_URL" >/dev/null

echo "Exporting solution '$SOLUTION_NAME' (managed=$SOLUTION_MANAGED) ..."
pac solution export \
  --name "$SOLUTION_NAME" \
  --path "$OUT_PATH" \
  --managed "$SOLUTION_MANAGED" \
  --overwrite true

echo "Downloaded solution package: $OUT_PATH"
