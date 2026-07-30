def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_postings_empty(client):
    response = client.get("/postings/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_postings_returns_seeded_posting(client, sample_posting):
    response = client.get("/postings/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Backend Developer"


def test_get_nonexistent_posting_returns_404(client):
    response = client.get("/postings/99999")
    assert response.status_code == 404


def test_create_application(client, sample_posting):
    response = client.post("/applications/", json={"posting_id": sample_posting.id})
    assert response.status_code == 201
    assert response.json()["status"] == "saved"


def test_cannot_track_same_posting_twice(client, sample_posting):
    client.post("/applications/", json={"posting_id": sample_posting.id})
    response = client.post("/applications/", json={"posting_id": sample_posting.id})
    assert response.status_code == 400


def test_update_application_status(client, sample_posting):
    create_response = client.post("/applications/", json={"posting_id": sample_posting.id})
    application_id = create_response.json()["id"]

    update_response = client.patch(f"/applications/{application_id}", json={"status": "applied"})
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "applied"
