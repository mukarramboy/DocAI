import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .services.rag_service import WeaviateRAGService
from .serializers import DocumentSerializer
from .tasks import indexer_document

ALLOWED_EXTENSIONS = ('.pdf', '.txt', '.docx', '.md')
MAX_UPLOAD_SIZE = 5 * 1024 * 1024

class UploadDocument1View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get("file")
            user_id = request.user.id
            try:
                text = file.read().decode("utf-8")

                task = indexer_document.delay(text, file.name, str(user_id))

                return Response({
                    "success": True,
                    "task": task.id,
                    "filename": file.name
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Upload failed: {str(e)}"}, status=400)
        return Response(serializer.errors, status=400)

class ChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        query = request.data.get("query")
        if not query and str(query).strip():
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with WeaviateRAGService() as weaviate_service:
                results = weaviate_service.search_user_documents(query=query, user_id=request.user.id, limit=3)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"query": query, "results": results}, status=status.HTTP_200_OK)
