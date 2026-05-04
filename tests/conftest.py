import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.fixture
def user(db):
    """Создаёт тестового пользователя в БД с использованием менеджера create_user (email required)."""
    # Use create_user to ensure password is hashed and required email field for CustomUser is provided.
    email = "test@example.com"
    password = "password"
    user = User.objects.create_user(email=email, password=password)
    return user

@pytest.fixture
def api_client():
    """DRF APIClient (неаутентифицированный)."""
    return APIClient()

@pytest.fixture
def auth_api_client(api_client, user):
    """Аутентифицированный клиент."""
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def simple_uploaded_file():
    """Простой загружаемый файл для multipart upload."""
    content = b"hello world"
    return SimpleUploadedFile("sample.txt", content, content_type="text/plain")

@pytest.fixture
def celery_eager(settings):
    """Включает synchronous режим Celery задач в тестах."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    return settings

@pytest.fixture
def mock_weaviate_service(monkeypatch):
    """Простейшая замена реального WeaviateRAGService для unit-тестов."""
    class DummyWeaviate:
        def __init__(self, *args, **kwargs): pass
        def index_document(self, text, file_name, user_id): return 3
        def search_user_documents(self, query, user_id, limit=1): return ["chunk1"][:limit]
        def close(self): pass
        def __enter__(self): return self
        def __exit__(self, exc_type, exc, tb): return False

    monkeypatch.setattr("ai.services.rag_service.WeaviateRAGService", DummyWeaviate)
    return DummyWeaviate


@pytest.fixture
def user_with_credentials(db):
    """Создаёт пользователя и возвращает (user, credentials_dict).

    Удобно для тестов аутентификации: фикстура сразу отдаёт и email/password в явном виде.
    """
    email = "testuser@example.com"
    password = "password"
    user = User.objects.create_user(email=email, password=password)
    return user, {"email": email, "password": password}
