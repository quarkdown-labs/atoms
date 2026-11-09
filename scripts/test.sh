#!/usr/bin/env bash
# Runs atom test cases, asserting against their compiled output as rendered in a browser.
#
# A test case is a directory matching `<atom>/<version>/__tests/<case>/` containing:
#   - main.qd  the document to compile
#   - test.py  the assertions on the rendered document
#
# Usage: scripts/test.sh [--print-only] [dir...] [pytest-option...]
# Each directory can be a test case, a package version (kanban/1.0.0) or a whole package (kanban),
# whose test cases are all run. With none given, all test cases in the repository are run.
# With --print-only, the compiled output of each test case is printed instead of being tested.
# In this mode, only directories are accepted.

set -uo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SCRIPTS="$ROOT/scripts"
readonly COMPILE=(quarkdown c main.qd -r html --pipe --nowrap --allow global-read)

# Prints the test case directories within the given directories, or within the repository if none are given.
discover_tests() {
    find "${@:-$ROOT}" -name main.qd -path '*/__tests/*/main.qd' -exec dirname {} \; | sort
}

print_test() {
    local dir="$1"
    echo "=== ${dir#"$ROOT"/}"
    (cd "$dir" && "${COMPILE[@]}")
}

print_tests() {
    local failed=0 test
    while IFS= read -r test; do
        print_test "$test" || failed=$((failed + 1))
    done < <(discover_tests "$@")
    [[ $failed -eq 0 ]]
}

run_tests() {
    QUARKDOWN="$(command -v quarkdown)" "$SCRIPTS/python.sh" -m pytest -c "$SCRIPTS/pytest.ini" --rootdir "$ROOT" "${@:-$ROOT}"
}

main() {
    if [[ ${1:-} == --print-only ]]; then
        shift
        print_tests "$@"
    else
        run_tests "$@"
    fi
}

main "$@"
