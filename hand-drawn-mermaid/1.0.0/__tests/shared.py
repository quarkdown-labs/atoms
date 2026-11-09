import re

import pytest
from playwright.sync_api import expect


def diagram(page):
    return page.locator(".mermaid svg")


def assert_labels(page, *labels):
    """Asserts that the labels are drawn, in the main color of the document."""
    main_color = page.evaluate("getComputedStyle(document.body).color")
    for label in labels:
        # The innermost element is the one that is painted.
        expect(diagram(page).locator("text, tspan", has_text=label).last).to_have_css("fill", main_color)


def assert_sketched_by_mermaid(page):
    expect(diagram(page).locator('[data-look="handDrawn"]').first).to_be_attached()
    expect(diagram(page)).not_to_have_attribute("stroke-linecap", "round")


def assert_sketched_by_svg2roughjs(page):
    """Asserts that the diagram was redrawn, with a viewBox fitted to its bounds with a 6 px margin."""
    svg = diagram(page)
    expect(svg).to_have_attribute("stroke-linecap", "round")
    expect(svg.locator('[data-look="handDrawn"]')).to_have_count(0)
    expect(svg).not_to_have_attribute("height", re.compile(".*"))
    view_box, bounds = svg.evaluate(
        """svg => {
            const { x, y, width, height } = svg.getBBox();
            return [svg.getAttribute("viewBox").split(" ").map(Number), [x - 6, y - 6, width + 12, height + 12]];
        }"""
    )
    assert view_box == pytest.approx(bounds, abs=0.01), f"viewBox {view_box} does not fit the bounds {bounds}"
