from playwright.sync_api import expect
from shared import affiliations, authors, is_stacked


def test_authors_reference_their_affiliations(page):
    expect(authors(page)).to_have_text("Jane Doe1,2, John Smith, Alice Johnson1")


def test_affiliations_are_listed_inline(page):
    expect(affiliations(page)).to_have_text("1Quarkdown Labs, 2University of San Francisco")
    assert not is_stacked(page)
