from django.urls import path

from .views import UploadDocumentView, ChatView


urlpatterns = [
    path("upload/", UploadDocumentView.as_view(), name="upload-document"),
    path("chat/", ChatView.as_view(), name="chat"),
]
