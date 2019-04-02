from django.urls import path
from .views import spotify_connect, spotify_callback

app_name = 'spotify'

urlpatterns = [
    path('connect/', spotify_connect, name='connect'),
    path('callback/', spotify_callback, name='callback'),
]