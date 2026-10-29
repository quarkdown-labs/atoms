---
name: generating-package-images
description: Use when an atom in this repository needs a README screenshot or a THUMBNAIL.webp, when one is missing, or when a package's or template's output changed and its images are stale.
---

# Generating package images

A demo document is compiled with the local `quarkdown` and screenshotted in headless Chrome. The layout is inferred from `atom.toml`:

| Atom | Layout | Output |
|---|---|---|
| No `[template]` section | 2:1 | `__images/preview.png` at 2x, cropped to the content<br>`THUMBNAIL.webp`, 800x400, content centered and downscaled only if it doesn't fit |
| `doctype = "paged"` | Vertical | `THUMBNAIL.webp` of the first page, sized as the page format (794x1123 for A4) |
| `doctype = "plain"` | Vertical | `THUMBNAIL.webp` of the top of the document, 794x1123 |
| `doctype = "slides"` | Horizontal | `THUMBNAIL.webp` of the first slide without navigation controls, 1123x705 |
| `doctype = "docs"` | Horizontal | `THUMBNAIL.webp` of the first screen, 1123x705 |

## Steps

1. Get a demo document:

   - **Template:** use `__test.qd` in the package folder. It is gitignored, so if it's missing, write one in the scratchpad with this shape:

     ```
     .docname {Vintage Slides}
     .doctype {slides}
     ...other metadata used by the template, such as .docauthors...

     .include {main.qd}
     .include {template.qd}
     ```

   - **Package:** write a demo in the scratchpad whose content is the README's main example, unchanged, so the images match what readers see:

     ```
     .docname {kanban}
     .doctype {plain}
     .include {main.qd}

     ...README example...
     ```

   `.include {main.qd}` resolves against the package. Keep anything the example needs before the include in that position. For example, `.docauthors` comes before the include in authors-frontmatter.

2. Run:

   ```bash
   bash scripts/images/generate.sh kanban/1.0.0 <demo.qd> [viewport-width]
   ```

   The viewport width only applies to packages and defaults to `1000`. Increase it when the content wraps, like kanban, which uses `1200`. The first run creates a Python venv with Pillow and Playwright in `~/.cache/quarkdown-atoms`.

3. Read the generated images and check them before reporting back.

4. For a package whose README doesn't show the preview yet, add it right under the description, with the same absolute link format as the other packages:

   ```markdown
   ![Alt text](https://github.com/quarkdown-labs/atoms/blob/main/kanban/1.0.0/__images/preview.png?raw=true)
   ```

   The link only resolves once the image is pushed to `main`.

## Notes

- The images overwrite existing ones. Regenerate a committed thumbnail only when asked, or when the atom's output changed.
- For packages, measure resolution in CSS pixels, not image pixels. A small demo produces a small image even at 2x. Don't add `zoom` or `transform` to make it bigger.
- The package background color is sampled from the top-left pixel. If a demo has a colored page background, keep the margins around the content so that pixel is still background.
- Requires `quarkdown` on `PATH` and Google Chrome installed.
