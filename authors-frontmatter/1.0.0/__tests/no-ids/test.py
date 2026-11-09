from playwright.sync_api import expect
from shared import affiliations, authors


def test_authors_have_no_references(page):
    expect(authors(page)).to_have_text("Jane Doe, John Smith, Alice Johnson")


def test_affiliations_are_omitted(page):
    expect(affiliations(page)).to_have_count(0)
