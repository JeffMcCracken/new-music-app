from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.conf import settings

import requests
import base64

# Create your views here.
def spotify_connect(request):

    client_id = settings.SPOTIFY_ID
    redirect_uri = settings.SPOTIFY_REDIRECT_URI
    response_type= 'code'
    scope = 'user-read-private user-follow-modify user-follow-read user-library-read'
    
    url = 'https://accounts.spotify.com/authorize'
    mod_url = '{}?client_id={}&response_type={}&redirect_uri={}&scope={}'.format(
        url,
        client_id,
        response_type,
        redirect_uri,
        scope
    )

    return HttpResponseRedirect(mod_url)

    
def spotify_callback(request):
    token = _get_token(request)

    # Getting all albums
    url = 'https://api.spotify.com/v1/me/albums'
    header = {'Authorization': 'Bearer {}'.format(token)}
    album_names = []
    payload = {'limit': '50'}
    response = requests.get(url, params=payload, headers=header)
    total_albums = response.json()['total']

    for i in range(int(total_albums/50)+1):
        for item in response.json()['items']:
            album_names.append(item['album']['name'])
        offset = 50*(i+1)
        payload = {'limit': '50', 'offset': offset}
        response = requests.get(url, params=payload, headers=header)
    
    for item in response.json()['items']:
        album_names.append(item['album']['name'])
        
    return render(request, 'spotify/artists.html', {
        'album_names': album_names
    })

def _get_token(request):
    payload = {
        'grant_type': 'authorization_code',
        'code': request.GET.get('code'),
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
    }
    client_id = settings.SPOTIFY_ID
    client_secret = settings.SPOTIFY_SECRET
    auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
    header = {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}
    url = 'https://accounts.spotify.com/api/token'

    tokens = requests.post(url, data=payload, headers=header)
    return tokens.json()['access_token']

