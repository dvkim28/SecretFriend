"""
URL configuration for secret_friend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import RoomCreateView, MyRooms, RoomDetailView, AllRooms, passcheck

app_name = 'rooms'
urlpatterns = [
    path('create/', RoomCreateView.as_view(), name='RoomCreateView'),
    path('my_rooms/', MyRooms.as_view(), name='MyRoomsView'),
    path('all_rooms/', AllRooms.as_view(), name='AllRooms'),
    path('room/<int:pk>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('pass_check', passcheck, name='passcheck'),

]
