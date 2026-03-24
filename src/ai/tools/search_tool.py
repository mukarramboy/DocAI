from ..services.rag_service import WeaviateRAGService


def search_documentation_tool(query: str, user_id: int):

    rag = WeaviateRAGService()

    results = rag.search(query=query, user_id=user_id)

    if not results:
        return "Релевантная информация не найдена."

    output = ""

    for i, res in enumerate(results, 1):

        output += f"--- Фрагмент {i} (Файл: {res['file_name']}) ---\n"
        output += f"{res['content']}\n\n"

    return output
