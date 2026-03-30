import uuid
import weaviate
from .chunking import chunk_text

NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


class WeaviateRAGService:
    COLLECTION = "Documentation"

    def __init__(self, weaviate_url: str = "http://localhost:8080"):
        # создаём клиент Weaviate
        self.client = weaviate.Client(weaviate_url)
        self._setup_collection()

    # Генерация UUID для каждого чанка документа
    def _make_uuid(self, file_name: str, chunk_id: int, user_id: str) -> str:
        return str(uuid.uuid5(NAMESPACE, f"{user_id}:{file_name}:{chunk_id}"))

    # Создание класса в Weaviate, если его нет
    def _setup_collection(self):
        schema = self.client.schema.get()
        classes = [c["class"] for c in schema.get("classes", [])]

        if self.COLLECTION not in classes:
            self.client.schema.create_class({
                "class": self.COLLECTION,
                "vectorizer": "text2vec-transformers",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {
                        "name": "file_name",
                        "dataType": ["text"],
                        "moduleConfig": {"text2vec-transformers": {"skip": True}},
                    },
                    {
                        "name": "chunk_id",
                        "dataType": ["int"],
                        "moduleConfig": {"text2vec-transformers": {"skip": True}},
                    },
                    {
                        "name": "user_id",
                        "dataType": ["text"],
                        "moduleConfig": {"text2vec-transformers": {"skip": True}},
                    },
                ],
            })

    # Индексация документа с разделением на чанки и использованием batch
    def index_document(self, text: str, file_name: str, user_id: str):
        chunks = chunk_text(text)

        with self.client.batch as batch:
            batch.batch_size = 50  # можно менять под нагрузку
            batch.timeout_retries = 3

            for i, chunk in enumerate(chunks):
                obj_uuid = self._make_uuid(file_name, i, user_id)

                batch.add_data_object(
                    data_object={
                        "content": chunk,
                        "file_name": file_name,
                        "chunk_id": i,
                        "user_id": str(user_id),
                    },
                    class_name=self.COLLECTION,
                    uuid=obj_uuid,
                )

        return i

    # Поиск по семантическому сходству с фильтром по пользователю и порогу distance
    def search(self, query: str, user_id: str, limit: int = 3, max_distance: float = 0.4):
        result = (
            self.client.query
            .get(self.COLLECTION, ["content", "file_name", "chunk_id"])
            .with_near_text({"concepts": [query]})
            .with_where({
                "path": ["user_id"],
                "operator": "Equal",
                "valueText": str(user_id),
            })
            .with_additional(["distance"])
            .with_limit(limit * 5)  # берём больше, чтобы потом фильтровать по distance
            .do()
        )

        objects = result["data"]["Get"].get(self.COLLECTION, [])

        # фильтруем по max_distance и лимиту
        filtered = [
            {
                "content": obj["content"],
                "file_name": obj["file_name"],
                "chunk_id": obj["chunk_id"],
                "distance": obj["_additional"]["distance"],
            }
            for obj in objects
            if obj["_additional"]["distance"] <= max_distance
        ]

        return filtered[:limit]

    # Удаление документа по file_name и user_id
    def delete_document(self, file_name: str, user_id: str):
        self.client.batch.delete_objects(
            class_name=self.COLLECTION,
            where={
                "operator": "And",
                "operands": [
                    {"path": ["file_name"], "operator": "Equal", "valueText": file_name},
                    {"path": ["user_id"], "operator": "Equal", "valueText": str(user_id)},
                ],
            },
        )
