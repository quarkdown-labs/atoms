#!/usr/bin/env bash
# Runs every atom test case and compares the compiled output against its expectation.
#
# A test case is a directory matching `<atom>/<version>/__tests/<case>/` containing:
#   - main.qd      the document to compile
#   - expect.html  the expected HTML output
#
# Usage: scripts/test.sh [test-dir...]
# With no arguments, all test cases in the repository are run.

set -uo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly COMPILE=(quarkdown c main.qd -r html --pipe --nowrap --allow global-read)

discover_tests() {
    find "$ROOT" -mindepth 4 -maxdepth 4 -type d -path '*/__tests/*' | sort
}

# Canonical formatting options.
readonly TIDY=(tidy -q --indent auto --wrap 0 --tidy-mark no --show-warnings no
    --drop-empty-elements no --drop-empty-paras no --merge-divs no --merge-spans no
    --custom-tags blocklevel)

require_tidy() {
    local version
    version="$(tidy --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)"
    if [[ -z "$version" || ${version%%.*} -lt 5 ]]; then
        echo "::error::tidy-html5 >= 5 is required (found: ${version:-none})"
        exit 2
    fi
}

# Reformats stdin HTML canonically.
normalize() {
    "${TIDY[@]}" || [[ $? -eq 1 ]]
}

run_test() {
    local dir="$1"
    local name="${dir#"$ROOT"/}"
    local actual
    actual="$(cd "$dir" && "${COMPILE[@]}")" || { echo "::error::$name: compilation failed"; return 1; }

    if diff_output="$(diff -u <(normalize < "$dir/expect.html") <(normalize <<< "$actual"))"; then
        echo "PASS $name"
    else
        echo "FAIL $name"
        echo "$diff_output"
        return 1
    fi
}

main() {
    require_tidy

    local tests=() test
    if [[ $# -gt 0 ]]; then
        tests=("$@")
    else
        while IFS= read -r test; do tests+=("$test"); done < <(discover_tests)
    fi

    local failed=0
    for test in "${tests[@]}"; do
        run_test "$test" || failed=$((failed + 1))
    done

    echo "${#tests[@]} run, $failed failed"
    [[ $failed -eq 0 ]]
}

main "$@"
