from django.contrib import admin
from django.urls import path, include
from users.views import register_user

urlpatterns = [
path('admin/', admin.site.urls),
path('auth/register/', register_user),
]
