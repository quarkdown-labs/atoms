#!/usr/bin/env bash
# Runs Python with the dependencies of the scripts of this repository, which uv installs and caches.
#
# Usage: scripts/python.sh [python-argument...]

readonly SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHONPATH="$SCRIPTS" exec uv run --quiet --no-project --with-requirements "$SCRIPTS/requirements.txt" python "$@"
