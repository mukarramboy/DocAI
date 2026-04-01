import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .services.rag_service import WeaviateRAGService
from .serializers import DocumentSerializer

# class UploadDocumentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         file = request.FILES.get("file")
#         if not file:
#             return Response({"error": "File required"}, status=status.HTTP_400_BAD_REQUEST)

#         # 1. Проверка расширения
#         if not file.name.endswith((".txt", ".md", ".csv")):
#             return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

#         # 2. Ограничение размера (5 MB)
#         if file.size > 5 * 1024 * 1024:
#             return Response({"error": "File too large (max 5MB)"}, status=status.HTTP_400_BAD_REQUEST)

#         # 3. Безопасное чтение с обработкой ошибок декодирования
#         try:
#             text = file.read().decode("utf-8")
#         except UnicodeDecodeError:
#             return Response({"error": "File must be UTF-8 encoded"}, status=status.HTTP_400_BAD_REQUEST)

#         if not text.strip():
#             return Response({"error": "File is empty"}, status=status.HTTP_400_BAD_REQUEST)

#         # 4. Индексация с обработкой ошибок Weaviate
#         try:
#             rag = WeaviateRAGService()
#             count_chunks = rag.index_document(
#                 text=text,
#                 file_name=file.name,
#                 user_id=str(request.user.id),
#             )
#         except Exception as e:
#             import traceback
#             traceback.print_exc()  # выведет полный traceback в консоль Django
#             return Response({"error": f"Indexing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         data = {
#             "message": "Document indexed",
#             "file_name": file.name,
#             "chunks": count_chunks  ,
#         }

#         return Response(data, status=201)

class UploadDocument1View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get("file")
            user_id = request.user.id
            weaviate_service = WeaviateRAGService()
            try:
                text = file.read().decode("utf-8")

                chunks_count = weaviate_service.index_document(text, file.name, str(user_id))

                return Response({
                    "message": "Документ успешно проиндексирован",
                    "chunks_created": chunks_count,
                    "filename": file.name
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Upload failed: {str(e)}"}, status=400)
            finally:
                weaviate_service.close()
        return Response(serializer.errors, status=400)

class ChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        query = request.data.get("query")

        weaviate_service = WeaviateRAGService()
        results = weaviate_service.search_user_documents(
            query=query,
            user_id=request.user.id
        )
        weaviate_service.close()

        return Response({"query": query, "results": results})
