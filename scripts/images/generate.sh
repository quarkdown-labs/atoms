#!/usr/bin/env bash
# Generates the images of an atom from a demo document.
#
# Usage: generate.sh <package-dir> <demo.qd> [viewport-width]
#   package-dir     e.g. kanban/1.0.0
#   demo.qd         a document that includes the package via `.include {main.qd}`, like __test.qd
#   viewport-width  CSS width of the page, in pixels, for packages. Defaults to 1000.
#
# The layout is inferred from the template doctype in atom.toml:
#   no template  <package-dir>/__images/preview.png and an 800x400 <package-dir>/THUMBNAIL.webp
#   paged        <package-dir>/THUMBNAIL.webp of the first page
#   slides       <package-dir>/THUMBNAIL.webp of the first slide

set -euo pipefail

readonly HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly VENV="${XDG_CACHE_HOME:-$HOME/.cache}/quarkdown-atoms/venv"

package="$(cd "$1" && pwd)" demo="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")" width="${3:-1000}"

ensure_venv() {
    [[ -x "$VENV/bin/python" ]] && return
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install -q --disable-pip-version-check pillow playwright
}

# Prints the template doctype declared in atom.toml, or `package` if the atom is not a template.
layout() {
    local doctype
    doctype="$(sed -n '/^\[template\]/,/^\[/s/^doctype *= *"\(.*\)"/\1/p' "$package/atom.toml")"
    echo "${doctype:-package}"
}

# Compiles the demo next to a copy of the package, so that relative includes and assets resolve.
compile() {
    local work="$1"
    cp -R "$package/." "$work"
    cp "$demo" "$work/__preview.qd"
    (cd "$work" && quarkdown c __preview.qd -o out --allow global-read > /dev/null)
    find "$work/out" -name index.html | head -1
}

ensure_venv
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

"$VENV/bin/python" -I "$HERE/capture.py" "$(layout)" "$(compile "$work")" "$package" "$width"
