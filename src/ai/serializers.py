from rest_framework import serializers

class DocumentSerializer(serializers.Serializer):
    file = serializers.FileField()
