#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_DIR="${DEVFOLIO_WORKSPACE_PATH:-$(cd "$PLUGIN_DIR/../.." && pwd)}"
MCP_DIR="${DEVFOLIO_MCP_SERVER_DIR:-$WORKSPACE_DIR/devfolio-mcp-server}"

if [[ ! -d "$MCP_DIR" ]]; then
  echo "Devfolio MCP server not found at: $MCP_DIR" >&2
  echo "Set DEVFOLIO_WORKSPACE_PATH or DEVFOLIO_MCP_SERVER_DIR and try again." >&2
  exit 1
fi

if [[ -z "${DEVFOLIO_API_BASE_URL:-}" ]]; then
  echo "DEVFOLIO_API_BASE_URL is required." >&2
  echo "Example: export DEVFOLIO_API_BASE_URL=https://api.devfolio.co/api" >&2
  exit 1
fi

cd "$MCP_DIR"

if [[ ! -d node_modules ]]; then
  echo "node_modules is missing in $MCP_DIR" >&2
  echo "Install dependencies first: npx pnpm@10.12.1 install --frozen-lockfile" >&2
  exit 1
fi

if [[ ! -f dist/index.js ]]; then
  if [[ ! -x ./node_modules/.bin/tsc ]]; then
    echo "TypeScript compiler not found at ./node_modules/.bin/tsc" >&2
    exit 1
  fi
  ./node_modules/.bin/tsc
fi

exec node dist/index.js
