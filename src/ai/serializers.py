from rest_framework import serializers
import os

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.docx']

class DocumentSerializer(serializers.Serializer):
    file = serializers.FileField(required = True)

    def validate_file(self, value):
        if value.size > MAX_UPLOAD_SIZE:
            raise serializers.ValidationError("File too large (max 5MB)")
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(f"Unsupported format: {ext}")
        return value
