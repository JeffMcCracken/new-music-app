from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from accounts.models import Artist, User

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def artists(request):

    artists = request.user.artists.all().order_by(Lower('name'))

    return render(request, 'artists.html', {
        'artists': artists,
    })

@login_required
def artist_details(request, *args, **kwargs):
    artist_id = kwargs.pop('artist_id')
    artist = Artist.objects.get(id=artist_id)

    albums = artist.albums.all()

    return render(request, 'artist_details.html', {
        'artist': artist,
        'albums': albums,
    })