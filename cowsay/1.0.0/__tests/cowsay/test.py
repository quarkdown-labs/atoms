from playwright.sync_api import expect


def test_message_is_in_a_rounded_bubble(page):
    bubble = page.get_by_text("Hello!!", exact=True).locator("xpath=ancestor::div[1]")
    expect(bubble).to_have_css("border-top-color", "rgb(211, 211, 211)")
    expect(bubble).not_to_have_css("border-top-left-radius", "0px")


def test_cow_is_below_the_message(page):
    message = page.get_by_text("Hello!!", exact=True).bounding_box()
    cow = page.get_by_text("🐄", exact=True).bounding_box()
    assert cow["y"] >= message["y"] + message["height"]
