from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.conf import settings

from accounts.models import User, Artist, Album, Genre, Track

import requests
import base64

def spotify_connect(request):
    '''
    Sends user to the login and authorization pages for spotify
    '''

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
  
def get_user_data(request):
    '''
    Gets all music data about the user, and adds relevant data to the
    user's account and to the other tables
    '''

    token = _spotify_callback(request)
    url = 'https://api.spotify.com/v1/me/albums'
    header = {'Authorization': 'Bearer {}'.format(token)}
    album_names = []
    payload = {'limit': '50'}
    response = requests.get(url, params=payload, headers=header)
    total_albums = response.json()['total']

    for i in range(int(total_albums/50)+1):
        for item in response.json()['items']:
            artists = _save_artist(item['album'], request.user)
            album = _save_album(item['album'], artists)
            _save_genres(item['album'], request.user, artists, album)
            _save_tracks(item['album']['tracks'], album)
            album_names.append(item['album']['name'])
        offset = 50*(i+1)
        payload = {'limit': '50', 'offset': offset}
        response = requests.get(url, params=payload, headers=header)

    artists = Artist.objects.all()
        
    return render(request, 'spotify/artists.html', {
        'artists': artists
    })

def _spotify_callback(request):
    '''
    Redirect uri view for Spotify that transfers the code for an auth
    token and returns that auth token for use
    '''
    token = _get_token(request)
    return token
    # Add the token to the given user and save it for user

def _get_token(request):
    '''
    Transfers the code that was sent from Spotify for an auth
    token and returns that auth token for use
    '''
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

def _save_artist(album, user):
    '''
    Saves the artist to the user's list of artists, and
    adds info about artist to artist table if the artist
    hasn't been added before by a different user
    '''
    objs = []
    for artist in album['artists']:
        obj, created = Artist.objects.get_or_create(
            href = artist['external_urls']['spotify'],
            spotify_id = artist['id'],
            name = artist['name'],
        )
        obj.users.add(user)
        objs.append(obj)

    return objs

def _save_album(album, artists):
    '''
    Saves info about the album to album table if the album
    hasn't been added before by a different user
    '''
    obj, created = Album.objects.get_or_create(
        album_type = album['album_type'],
        href = album['external_urls']['spotify'],
        spotify_id = album['id'],
        name = album['name'],
        release_date = album['release_date'],
        total_tracks = album['tracks']['total'],
    )
    for artist in artists:
        obj.artists.add(artist)

    return obj

def _save_genres(album, user, artists, album_obj):
    '''
    Saves the genre to the user's list of genres, and
    adds genre to the genre table if it hasn't been added before
    by a different user
    '''
    for genre in album['genres']:
        obj, created = Genre.objects.get_or_create(name=genre)
        obj.users.add(user)
        obj.albums.add(album_obj)
        for artist in artists:
            obj.artists.add(artist)

def _save_tracks(tracks, album):
    '''
    Saves track to the track table if it hasn't been added before
    by a different user
    '''
    for track in tracks['items']:
        artists = []
        for artist in track['artists']:
            obj, created = Artist.objects.get_or_create(
                href = artist['external_urls']['spotify'],
                spotify_id = artist['id'],
                name = artist['name'],
            )
            artists.append(obj)

        obj, created = Track.objects.get_or_create(
            album = album,
            duration_ms = track['duration_ms'],
            spotify_id = track['id'],
            name = track['name'],
            track_number = track['track_number'],
        )
        for artist in artists:
            obj.artists.add(artist)
        