from playwright.sync_api import expect
from shared import affiliations, authors, is_stacked


def test_authors_reference_their_affiliations(page):
    expect(authors(page)).to_have_text("Jane Doe1,2,3, John Smith4,5, Alice Johnson5")


def test_affiliations_at_the_threshold_are_inline(page):
    expect(affiliations(page).locator("sup")).to_have_count(5)
    assert not is_stacked(page)
