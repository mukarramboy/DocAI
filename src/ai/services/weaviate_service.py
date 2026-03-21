import weaviate

client = weaviate.Client()


def split_text(text: str, chunk_size=150, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks


def add_document(document):
    chunks = split_text(document.content)
    ids = []

    for chunk in chunks:
        data = {
            "content": chunk,
            "user_id": document.user.id,
            "document_id": document.id
        }

        result = client.data_object.create(
            data_object=data,
            class_name="Document"
        )
        ids.append(result["id"])
    return ids


def search_user_documents(user, question, limit=5):
    result = client.query.get(
        "Document",
        ["content"]
    ).with_near_text({
        "concepts": [question]
    }).with_where({
        "path": ["user_id"],
        "operator": "Equal",
        "valueInt": user.id
    }).with_limit(limit).do()

    docs = result["data"]["Get"]["Document"]
    return [d["content"] for d in docs]
