from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # genre, artist
    pass


class Artist(models.Model):
    # genre, album, track
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    href = models.CharField(max_length=255)
    image = models.ImageField(verbose_name='Artist Photo')
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Album(models.Model):
    # genre, track
    artists = models.ManyToManyField(Artist)
    album_type = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=128)
    album_art = models.ImageField(
        verbose_name='Album Cover',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    release_date = models.CharField(max_length=128)
    total_tracks = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    albums = models.ManyToManyField(Album)
    artists = models.ManyToManyField(Artist)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist)
    duration_ms = models.PositiveIntegerField()
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    track_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name