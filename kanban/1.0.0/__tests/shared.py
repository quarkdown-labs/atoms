def box(page, text):
    """Finds the box that directly encloses a column title, a card's text or a label."""
    return page.get_by_text(text, exact=True).first.locator("xpath=ancestor::div[1]")
