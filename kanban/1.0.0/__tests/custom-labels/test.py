from playwright.sync_api import expect
from shared import box


def test_custom_labels_have_translucent_colors(page):
    expect(box(page, "high")).to_have_css("background-color", "rgba(0, 0, 255, 0.25)")
    expect(box(page, "y")).to_have_css("background-color", "rgba(255, 165, 0, 0.25)")


def test_card_without_labels_has_none(page):
    expect(box(page, "Update documentation").locator("div")).to_have_count(0)
