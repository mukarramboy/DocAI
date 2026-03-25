import uuid
import requests as http
from .chunking import chunk_text
import weaviate

NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


class WeaviateRAGService:
    COLLECTION = "Documentation"

    def __init__(self, weaviate_url: str = "http://localhost:8080"):
        self.base = weaviate_url.rstrip("/")
        self._setup_collection()

    def _make_uuid(self, file_name: str, chunk_id: int, user_id: str) -> str:
        return str(uuid.uuid5(NAMESPACE, f"{user_id}:{file_name}:{chunk_id}"))

    def _setup_collection(self):
        resp = http.get(f"{self.base}/v1/schema")
        existing = [c["class"] for c in resp.json().get("classes", [])]
        if self.COLLECTION not in existing:
            http.post(f"{self.base}/v1/schema", json={
                "class": self.COLLECTION,
                "vectorizer": "text2vec-transformers",
                "properties": [
                    {"name": "content",   "dataType": ["text"]},
                    {"name": "file_name", "dataType": ["text"], "moduleConfig": {"text2vec-transformers": {"skip": True}}},
                    {"name": "chunk_id",  "dataType": ["int"],  "moduleConfig": {"text2vec-transformers": {"skip": True}}},
                    {"name": "user_id",   "dataType": ["text"], "moduleConfig": {"text2vec-transformers": {"skip": True}}},
                ],
            })

    def index_document(self, text: str, file_name: str, user_id: str) -> list[str]:
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            generated_uuid = self._make_uuid(file_name, i, user_id)
            resp = http.post(f"{self.base}/v1/objects", json={
                "class": self.COLLECTION,
                "id": generated_uuid,
                "properties": {
                    "content":   chunk,
                    "file_name": file_name,
                    "chunk_id":  i,
                    "user_id":   str(user_id),
                },
            })
            if resp.status_code not in (200, 201):
                raise RuntimeError(f"Weaviate error: {resp.status_code} {resp.text}")

        return i

    def search(self, query: str, user_id: str, limit: int = 1) -> list[dict]:
        resp = http.post(f"{self.base}/v1/graphql", json={
            "query": f"""
            {{
                Get {{
                    {self.COLLECTION}(
                        nearText: {{ concepts: ["{query}"] }}
                        where: {{
                            path: ["user_id"]
                            operator: Equal
                            valueText: "{user_id}"
                        }}
                        limit: {limit}
                    ) {{
                        content
                        file_name
                        chunk_id
                        _additional {{ distance }}
                    }}
                }}
            }}
            """
        })
        objects = resp.json().get("data", {}).get("Get", {}).get(self.COLLECTION, [])
        return [
            {
                "content":   obj["content"],
                "file_name": obj["file_name"],
                "chunk_id":  obj["chunk_id"],
                "distance":  obj.get("_additional", {}).get("distance"),
            }
            for obj in objects
        ]

    def delete_document(self, file_name: str, user_id: str) -> None:
        http.delete(f"{self.base}/v1/objects", json={
            "match": {
                "class": self.COLLECTION,
                "where": {
                    "operator": "And",
                    "operands": [
                        {"path": ["file_name"], "operator": "Equal", "valueText": file_name},
                        {"path": ["user_id"],   "operator": "Equal", "valueText": user_id},
                    ],
                },
            }
        })
