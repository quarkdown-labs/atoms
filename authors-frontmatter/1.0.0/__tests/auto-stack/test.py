from playwright.sync_api import expect
from shared import affiliations, authors, is_stacked


def test_authors_reference_their_affiliations(page):
    expect(authors(page)).to_have_text("Jane Doe1,2,3, John Smith4,5, Alice Johnson6")


def test_affiliations_past_the_threshold_are_stacked(page):
    expect(affiliations(page).locator("sup")).to_have_count(6)
    assert is_stacked(page)
