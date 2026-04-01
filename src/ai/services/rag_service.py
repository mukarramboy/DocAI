import weaviate
from weaviate.classes.config import Property, DataType
from weaviate.classes.config import Configure
from weaviate.classes.query import Filter

class WeaviateRAGService:
    def __init__(self, collection_name: str = "Documents"):
        self.client = weaviate.connect_to_local()
        self.collection_name = collection_name

        self._setup_collection()

    def _setup_collection(self):
        try:
            if  self.client.collections.exists(self.collection_name):
                return
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=Configure.Vectorizer.text2vec_transformers(),
                properties=[
                    Property(
                        name="content",
                        data_type=DataType.TEXT,
                        description="The text content of the documentation chunk",
                    ),
                    Property(
                        name="filename",
                        data_type=DataType.TEXT,
                        description="Source filename of the documentation chunk",
                        skip_vectorization=True,
                    ),
                    Property(
                        name="chank_id",
                        data_type=DataType.INT,
                        description="Chunk number within the file",
                        skip_vectorization=True,
                    ),
                    Property(
                        name="user_id",
                        data_type=DataType.TEXT,
                        description="User ID who uploaded the document",
                        skip_vectorization=True,
                    ),
                ],
                vector_index_config=Configure.VectorIndex.hnsw()
            )

            print(f"Collection {self.collection_name} created successfully")
        except Exception as e:
            print(f"Error setting up collection: {e}")
            raise

    def chunk_text(self,text: str, chunk_size: int = 300, overlap: int = 50):

        words = text.split()
        chunks = []

        step = chunk_size - overlap

        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])

            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def index_document(self, text: str, file_name: str, user_id: str):
        collection = self.client.collections.get(self.collection_name)
        total_count = 0

        try:
            chunks = self.chunk_text(text)
            with collection.batch.dynamic() as batch:
                for i, chunk in enumerate(chunks):
                    batch.add_object(
                        properties={
                            "content": chunk,
                            "filename": file_name,
                            "chunk_id": i,
                            "user_id": user_id
                        }
                    )
                    total_count += 1
        except Exception as e:
            print(f"Error indexing document: {e}")
            raise

        return total_count

    def search_user_documents(self, query: str, user_id: str, limit: int = 1):
        collection = self.client.collections.get(self.collection_name)

        response = collection.query.near_text(
            query=query,
            filters=Filter.by_property("user_id").equal(str(user_id)),
            limit=limit
        )
        return [obj.properties["content"] for obj in response.objects]

    def close(self):
        self.client.close()
