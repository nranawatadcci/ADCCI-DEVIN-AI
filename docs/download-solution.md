# Download Dynamics CRM Solution (Unmanaged or Managed)

Use the helper script to export/download a Dataverse solution package from your environment.

## Prerequisites
- Power Platform CLI (`pac`) installed.
- Access to the target Dataverse environment.
- Solution unique name (not display name).

## Command

```bash
DATAVERSE_ENV_URL="https://<org>.crm.dynamics.com" \
SOLUTION_NAME="ADCCIDEVINAIV1" \
SOLUTION_MANAGED="false" \
OUTPUT_DIR="." \
./scripts/download-solution.sh
```

## Parameters
- `DATAVERSE_ENV_URL` (required): Dataverse org URL.
- `SOLUTION_NAME` (required): Solution unique name.
- `SOLUTION_MANAGED` (optional): `true` or `false` (default `false`).
- `OUTPUT_DIR` (optional): Destination folder (default current directory).
- `OUTPUT_FILE` (optional): Output filename override.

## Output
The script exports the solution zip to the requested output location and prints the path.
