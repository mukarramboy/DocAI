from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services.rag_service import WeaviateRAGService

class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "File required"}, status=400)

        # 1. Проверка расширения
        if not file.name.endswith((".txt", ".md", ".csv")):
            return Response({"error": "Unsupported file type"}, status=400)

        # 2. Ограничение размера (5 MB)
        if file.size > 5 * 1024 * 1024:
            return Response({"error": "File too large (max 5MB)"}, status=400)

        # 3. Безопасное чтение с обработкой ошибок декодирования
        try:
            text = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response({"error": "File must be UTF-8 encoded"}, status=400)

        if not text.strip():
            return Response({"error": "File is empty"}, status=400)

        # 4. Индексация с обработкой ошибок Weaviate
        try:
            rag = WeaviateRAGService()
            uuids = rag.index_document(
                text=text,
                file_name=file.name,
                user_id=str(request.user.id),
            )
        except Exception as e:
            import traceback
            traceback.print_exc()  # выведет полный traceback в консоль Django
            return Response({"error": f"Indexing failed: {str(e)}"}, status=500)

        return Response({
            "message": "Document indexed",
            "file_name": file.name,
            "chunks": len(uuids),
        }, status=201)

class ChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        query = request.data.get("query")

        rag = WeaviateRAGService()

        context = rag.search(
            query=query,
            user_id=request.user.id
        )

        return Response({
            "context": context
        })
