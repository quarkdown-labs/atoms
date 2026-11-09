from playwright.sync_api import expect
from shared import affiliations, authors


def font_size(locator):
    return float(locator.evaluate("element => parseFloat(getComputedStyle(element).fontSize)"))


def test_font_applies_to_authors(page):
    expect(authors(page)).to_have_css("font-weight", "700")


def test_font_size_applies_to_authors_only(page):
    assert font_size(authors(page)) > font_size(affiliations(page))


def test_references_keep_a_normal_weight(page):
    expect(authors(page).locator("sup").first).to_have_css("font-weight", "400")
