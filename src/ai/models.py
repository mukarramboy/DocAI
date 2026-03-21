from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    content = models.TextField()

    weaviate_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
