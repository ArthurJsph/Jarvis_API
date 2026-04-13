#!/bin/bash
set -e

# Compatibility wrapper: delegates to scripts/start.sh
exec "$(dirname "$0")/scripts/start.sh" "$@"
