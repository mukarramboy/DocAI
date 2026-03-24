import weaviate


class WeaviateClient:

    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = weaviate.connect_to_local()
        return cls._client

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
