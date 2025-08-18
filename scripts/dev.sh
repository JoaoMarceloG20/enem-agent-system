#!/bin/bash

############################################################################
# Run the application in development mode
# Usage: ./scripts/dev.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname $CURR_DIR)"
source ${CURR_DIR}/_utils.sh

print_heading "Starting Agent API in development mode..."

# Load environment variables
if [ -f "${REPO_ROOT}/.env" ]; then
    export $(cat ${REPO_ROOT}/.env | grep -v '#' | xargs)
fi

print_heading "Running: fastapi dev app/main.py --host 0.0.0.0 --port 8000"
cd ${REPO_ROOT}
fastapi dev app/main.py --host 0.0.0.0 --port 8000