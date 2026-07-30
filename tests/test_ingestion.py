from backend.app.ingestion.adzuna import normalize


def test_normalize_maps_fields_correctly():
    sample_job = {
        "id": 12345,
        "title": "Software Developer",
        "company": {"display_name": "Acme Corp"},
        "location": {"display_name": "Toronto, ON"},
        "description": "Great job",
        "redirect_url": "https://example.com/job/12345",
        "created": "2026-07-01T12:00:00Z",
    }
    result = normalize(sample_job)

    assert result["external_id"] == "12345"
    assert result["title"] == "Software Developer"
    assert result["company"] == "Acme Corp"
    assert result["location"] == "Toronto, ON"
    assert result["url"] == "https://example.com/job/12345"
    assert result["posted_date"] is not None


def test_normalize_handles_missing_optional_fields():
    """Adzuna doesn't always include company/location/created - normalize
    should degrade gracefully instead of raising."""
    sample_job = {"id": 999, "title": "Some Job"}
    result = normalize(sample_job)

    assert result["external_id"] == "999"
    assert result["company"] is None
    assert result["location"] is None
    assert result["posted_date"] is None
