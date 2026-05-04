from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include users.urls with explicit namespace to allow reverse('users:...') in tests
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('ai/', include('ai.urls')),
]

urlpatterns += []
