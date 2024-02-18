from django.contrib import admin
from django.urls import path, include

from .views import main

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='homepage'),
    path('users/', include('users.urls')),  # Remove the name argument here
    path('rooms/', include('rooms.urls')),  # Remove the name argument here
]
