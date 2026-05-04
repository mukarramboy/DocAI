from django.urls import path
from .views import RegisterApiView, ProfileApiview, LoginApiView

app_name = "users"

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("login/", LoginApiView.as_view(), name="login"),
    # path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("me/", ProfileApiview.as_view(), name="profile"),
]
