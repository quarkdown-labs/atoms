"""Opens compiled Quarkdown documents in a browser."""
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import Browser, Page, Playwright


def launch_browser(playwright: Playwright) -> Browser:
    return playwright.chromium.launch(channel="chrome")


@contextmanager
def serve(directory: Path):
    """Serves a directory over HTTP, since paged.js fetches stylesheets with XHR, which file:// blocks."""
    handler = partial(QuietHandler, directory=str(directory))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        yield f"http://127.0.0.1:{server.server_port}"
        server.shutdown()


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def open_document(page: Page, url: str, html: Path):
    """Navigates to a served document and waits for it to finish rendering."""
    page.goto(f"{url}/{html.name}", wait_until="networkidle")
    page.wait_for_function("window.isReady()")
