"""Pytest plugin that gives each atom test case its main.qd, compiled and rendered in a browser.

A `test.py` receives the rendered document through the `page` fixture. All the tests of a case share
the same page, so they should not change it. The page's clock is fixed to `NOW`.

Helpers shared by the test cases of a package go in `__tests/shared.py`, which a `test.py` imports as `shared`.
"""
import importlib.util
import os
import subprocess
import sys
from datetime import datetime
from functools import cache
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from rendering import launch_browser, open_document, serve

# Output may depend on the current date.
NOW = datetime(2026, 1, 1)

# Without --strict, a failing function call is rendered into the document and the exit code is 0.
COMPILE = (os.environ.get("QUARKDOWN", "quarkdown"), "c", "main.qd", "--strict", "--allow", "global-read")


def pytest_collect_file(file_path: Path):
    """Rejects a test case with no assertions, which would otherwise be silently left out of the run."""
    is_case = file_path.name == "main.qd" and file_path.parent.parent.name == "__tests"
    if is_case and not (file_path.parent / "test.py").exists():
        raise pytest.UsageError(f"{file_path.parent}: test case has no test.py")


def pytest_collectstart(collector):
    """Points `shared` to the helpers of the package whose test case is about to be imported.

    Packages can't import their helpers by path, and a single module named `shared` would be cached
    for the whole run, so it is swapped before each test case is imported.
    """
    if isinstance(collector, pytest.Module):
        helpers = collector.path.parent.parent / "shared.py"
        if helpers.exists():
            sys.modules["shared"] = load_helpers(helpers)


@cache
def load_helpers(path: Path):
    spec = importlib.util.spec_from_file_location("shared", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        yield browser
        browser.close()


@pytest.fixture(scope="module")
def document(request, tmp_path_factory) -> Path:
    """Compiles the test case, returning the path of its HTML output."""
    out = tmp_path_factory.mktemp("out")
    result = subprocess.run(
        [*COMPILE, "-o", str(out)], cwd=request.path.parent, capture_output=True, text=True
    )
    if result.returncode != 0:
        pytest.fail(f"Compilation failed:\n{result.stdout}{result.stderr}", pytrace=False)
    return next(out.rglob("index.html"))


@pytest.fixture(scope="module")
def page(browser, document):
    """The rendered document. Uncaught script errors while it loads fail every test of the case."""
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(error))
    page.clock.set_fixed_time(NOW)
    with serve(document.parent) as url:
        open_document(page, url, document)
        if errors:
            pytest.fail(f"Page errors: {errors}", pytrace=False)
        yield page
    page.close()
