from playwright.sync_api import expect
from shared import affiliations, authors, is_stacked


def test_authors_reference_their_affiliations(page):
    expect(authors(page)).to_have_text("Jane Doe1,2, John Smith, Alice Johnson1")


def test_affiliations_are_stacked(page):
    expect(affiliations(page).locator("sup")).to_have_text(["1", "2"])
    expect(affiliations(page)).to_contain_text("Quarkdown Labs")
    expect(affiliations(page)).to_contain_text("University of San Francisco")
    assert is_stacked(page)
