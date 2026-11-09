def authors(page):
    return page.locator("p", has_text="Jane Doe")


def affiliations(page):
    return page.locator(".authors-metadata")


def is_stacked(page) -> bool:
    """Whether each affiliation sits on its own line, regardless of the markup that achieves it."""
    markers = affiliations(page).locator("sup")
    tops = {round(marker.bounding_box()["y"]) for marker in markers.all()}
    return len(tops) == markers.count()
