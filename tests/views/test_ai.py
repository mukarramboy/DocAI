import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_upload_requires_auth(api_client, simple_uploaded_file):
    url = reverse("ai:upload-document")
    resp = api_client.post(url, {"file": simple_uploaded_file}, format="multipart")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_upload_starts_task(auth_api_client, simple_uploaded_file, monkeypatch):
    class FakeAsyncResult:
        id = "fake-task-id"

    class FakeTask:
        def delay(self, text, filename, user_id):
            # basic sanity checks on inputs
            assert isinstance(text, str)
            assert filename == simple_uploaded_file.name
            # user_id is stringified in the view
            assert isinstance(user_id, str) or isinstance(user_id, int)
            return FakeAsyncResult()

    # Patch the exact symbol that the view uses
    monkeypatch.setattr("ai.views.indexer_document", FakeTask(), raising=True)

    url = reverse("ai:upload-document")
    resp = auth_api_client.post(url, {"file": simple_uploaded_file}, format="multipart")

    assert resp.status_code == 201
    assert resp.data["task"] == "fake-task-id"
    assert resp.data["filename"] == simple_uploaded_file.name
    assert resp.data.get("success") is True


@pytest.mark.django_db
def test_chat_requires_auth(api_client):
    url = reverse("ai:chat")
    resp = api_client.post(url, {"query": "x"}, format="json")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_chat_returns_results(auth_api_client, mock_weaviate_service, monkeypatch):

    monkeypatch.setattr("ai.views.WeaviateRAGService", mock_weaviate_service, raising=True)

    url = reverse("ai:chat")
    resp = auth_api_client.post(url, {"query": "hello"}, format="json")

    assert resp.status_code == 200
    assert "results" in resp.data
    assert isinstance(resp.data["results"], list)
    assert len(resp.data["results"]) >= 1
