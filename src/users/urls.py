from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterApiView, ProfileApiview, LoginApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("register/", RegisterApiView.as_view()),
    path("login/", LoginApiView.as_view())
    # path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("me/", ProfileApiview.as_view(), name="profile"),

]
