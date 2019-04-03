from django.urls import path
from .views import spotify_connect, get_user_artists

app_name = 'spotify'

urlpatterns = [
    path('connect/', spotify_connect, name='connect'),
    path('callback/', get_user_artists, name='callback'),
]