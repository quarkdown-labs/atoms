from shared import assert_labels, assert_sketched_by_svg2roughjs


def test_labels_are_drawn(page):
    assert_labels(page, "Plan", "Design")


def test_is_sketched(page):
    assert_sketched_by_svg2roughjs(page)
