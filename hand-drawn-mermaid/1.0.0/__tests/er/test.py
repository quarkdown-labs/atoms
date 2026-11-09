from shared import assert_labels, assert_sketched_by_mermaid


def test_labels_are_drawn(page):
    assert_labels(page, "CUSTOMER", "ORDER", "places")


def test_is_sketched(page):
    assert_sketched_by_mermaid(page)
