import pytest
from playwright.sync_api import expect
from shared import box


def test_columns_are_side_by_side(page):
    expect(page.locator(".kanban strong")).to_have_text(["To do", "In progress", "Done"])
    columns = [box(page, title).bounding_box() for title in ("To do", "In progress", "Done")]
    assert columns[0]["x"] < columns[1]["x"] < columns[2]["x"]
    assert len({column["y"] for column in columns}) == 1


def test_cards_are_stacked_within_their_column(page):
    title, first, second = (
        box(page, text).bounding_box() for text in ("To do", "Authentication", "Update documentation")
    )
    assert title["y"] < first["y"] < second["y"]
    assert title["x"] == first["x"] == second["x"]


def test_column_width_defaults_to_12em(page):
    font_size = page.locator(".kanban").evaluate("element => parseFloat(getComputedStyle(element).fontSize)")
    assert box(page, "Authentication").bounding_box()["width"] == pytest.approx(12 * font_size)


def test_font_size_applies_to_the_board(page):
    sizes = page.locator(".kanban").evaluate(
        """element => [element, document.body].map((e) => parseFloat(getComputedStyle(e).fontSize))"""
    )
    assert sizes[0] < sizes[1]


def test_card_border_defaults_to_lightgray(page):
    expect(box(page, "Update documentation")).to_have_css("border-top-color", "rgb(211, 211, 211)")


def test_card_color_applies_to_its_border(page):
    expect(box(page, "Fix login bug")).to_have_css("border-top-color", "rgb(255, 0, 0)")


def test_column_color_applies_to_its_title(page):
    expect(box(page, "Done")).to_have_css("border-bottom-color", "rgb(0, 128, 0)")


def test_default_labels_have_translucent_colors(page):
    expect(box(page, "High")).to_have_css("background-color", "rgba(255, 0, 0, 0.25)")
    expect(box(page, "Medium")).to_have_css("background-color", "rgba(255, 255, 0, 0.25)")
    expect(box(page, "Low")).to_have_css("background-color", "rgba(0, 128, 0, 0.25)")


def test_labels_of_a_card_are_side_by_side(page):
    card = box(page, "Dashboard")
    low = card.get_by_text("Low", exact=True).bounding_box()
    medium = card.get_by_text("Medium", exact=True).bounding_box()
    assert low["y"] == medium["y"]
    assert low["x"] < medium["x"]
