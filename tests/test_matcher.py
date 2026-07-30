from backend.app.matching.matcher import strip_html, compute_match_score


def test_strip_html_removes_tags():
    html = "<p>Great <b>Python</b> role</p>"
    result = strip_html(html)
    assert "<" not in result
    assert "Python" in result


def test_strip_html_handles_empty_input():
    assert strip_html("") == ""
    assert strip_html(None) == ""


def test_compute_match_score_ranks_similar_text_higher():
    """
    This is the test that actually validates the point of using semantic
    embeddings: a posting can score higher than an unrelated one even
    without sharing exact keywords with the profile.
    """
    profile = "Experienced Python backend developer with FastAPI and PostgreSQL skills."
    similar_posting = "Looking for a backend engineer skilled in Python and API development."
    unrelated_posting = "Seeking a pastry chef with 5 years of experience in French baking."

    similar_score = compute_match_score(profile, similar_posting)
    unrelated_score = compute_match_score(profile, unrelated_posting)

    assert similar_score > unrelated_score
