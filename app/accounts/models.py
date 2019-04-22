from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # genre, artist
    pass


class Artist(models.Model):
    # genre, album, track
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='artists')
    href = models.CharField(max_length=255)
    image_small = models.CharField(max_length=255, null=True, blank=True)
    image_medium = models.CharField(max_length=255, null=True, blank=True)
    image_large = models.CharField(max_length=255, null=True, blank=True)
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Album(models.Model):
    # genre, track
    artists = models.ManyToManyField(Artist, related_name='albums')
    album_type = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=128)
    art_small = models.CharField(max_length=255)
    art_medium = models.CharField(max_length=255)
    art_large = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    release_date = models.CharField(max_length=128)
    total_tracks = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='genres')
    albums = models.ManyToManyField(Album, related_name='genres')
    artists = models.ManyToManyField(Artist, related_name='genres')
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    artists = models.ManyToManyField(Artist, related_name='tracks')
    duration_ms = models.PositiveIntegerField()
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    track_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name