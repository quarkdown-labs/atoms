"""Screenshots a compiled Quarkdown document and saves the images of an atom, according to its layout.

Usage: capture.py <layout> <html-file> <package-dir> [viewport-width]

Layouts:
  package         2x preview cropped to the content, and an 800x400 thumbnail with the content centered
  plain, paged    vertical thumbnail of the top of the document, or of its first page
  slides, docs    horizontal thumbnail of the first screen, or of the first slide
"""
import io
import sys
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from PIL import Image, ImageChops
from playwright.sync_api import Page, sync_playwright


class Layout:
    """Strategy that defines how a document is viewed and which images are derived from it."""

    viewport = {"width": 1000, "height": 800}
    scale = 1

    def prepare(self, page: Page):
        """Adjusts the rendered page before it is captured."""

    def capture(self, page: Page) -> Image.Image:
        raise NotImplementedError

    def save(self, image: Image.Image, package: Path):
        raise NotImplementedError


class PackageLayout(Layout):
    """A package's output, which is small and free-floating on a plain page."""

    scale = 2
    preview_margin = 32 * scale
    thumbnail_size = (800, 400)
    thumbnail_margin = 48

    def __init__(self, width: int):
        self.viewport = {"width": width, "height": 800}

    def capture(self, page):
        return screenshot(page.screenshot(full_page=True))

    def save(self, image, package):
        background = image.getpixel((0, 0))
        content = crop_to_content(image)
        (package / "__images").mkdir(exist_ok=True)
        self.preview(content, background).save(package / "__images" / "preview.png", optimize=True)
        self.thumbnail(content, background).save(package / "THUMBNAIL.webp", quality=90, method=6)

    def preview(self, content, background):
        size = (content.width + 2 * self.preview_margin, content.height + 2 * self.preview_margin)
        return center(content, size, background)

    def thumbnail(self, content, background):
        """Downscales the content to fit within the margins, never upscaling it past its 2x source."""
        width, height = self.thumbnail_size
        margin = 2 * self.thumbnail_margin
        scale = min(1, (width - margin) / content.width, (height - margin) / content.height)
        resized = content.resize((round(content.width * scale), round(content.height * scale)), Image.LANCZOS)
        return center(resized, self.thumbnail_size, background)


class TemplateLayout(Layout):
    """A template's first screen, saved as the thumbnail as is."""

    def capture(self, page):
        return screenshot(page.screenshot())

    def save(self, image, package):
        image.save(package / "THUMBNAIL.webp", quality=90, method=6)


class VerticalLayout(TemplateLayout):
    """A portrait thumbnail, sized as an A4 page."""

    viewport = {"width": 794, "height": 1123}


class PagedLayout(VerticalLayout):
    """A portrait thumbnail of the first page, sized as the document's page format."""

    def capture(self, page):
        return screenshot(page.locator(".pagedjs_page").first.screenshot())


class HorizontalLayout(TemplateLayout):
    """A landscape thumbnail, framed as in the browser."""

    viewport = {"width": 1123, "height": 705}


class SlidesLayout(HorizontalLayout):
    """A landscape thumbnail of the first slide, without the navigation controls."""

    def prepare(self, page):
        page.add_style_tag(content=".reveal .controls, .reveal .progress { display: none !important; }")


def screenshot(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data)).convert("RGB")


def crop_to_content(image: Image.Image) -> Image.Image:
    """Crops away the uniform background, which is sampled from the top-left pixel."""
    background = Image.new("RGB", image.size, image.getpixel((0, 0)))
    mask = ImageChops.difference(image, background).point(lambda p: 255 if p > 8 else 0)
    return image.crop(mask.getbbox())


def center(content: Image.Image, size: tuple[int, int], background) -> Image.Image:
    canvas = Image.new("RGB", size, background)
    canvas.paste(content, ((size[0] - content.width) // 2, (size[1] - content.height) // 2))
    return canvas


def layout_of(name: str, width: int) -> Layout:
    layouts = {
        "package": lambda: PackageLayout(width),
        "plain": VerticalLayout,
        "paged": PagedLayout,
        "docs": HorizontalLayout,
        "slides": SlidesLayout,
    }
    return layouts[name]()


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


def main():
    name, html, package = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    layout = layout_of(name, int(sys.argv[4]) if len(sys.argv) > 4 else 1000)

    with serve(html.parent) as url, sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport=layout.viewport, device_scale_factor=layout.scale)
        page.goto(f"{url}/{html.name}", wait_until="networkidle")
        page.wait_for_function("window.isReady()")
        layout.prepare(page)
        image = layout.capture(page)
        browser.close()

    layout.save(image, package)


if __name__ == "__main__":
    main()
