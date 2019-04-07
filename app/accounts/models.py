from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(
        verbose_name='Profile Image',
        null=True,
        blank=True,
    )


class Artist(models.Model):
    # genre, album, track
    user = models.ManyToManyField(User)
    href = models.CharField(max_length=255)
    image = models.ImageField(verbose_name='Artist Photo')
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Album(models.Model):
    # genre, track
    artist = models.ManyToManyField(Artist)
    album_type = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=128)
    album_art = models.ImageField(verbose_name='Album Cover')
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    release_date = models.CharField(max_length=128)
    total_tracks = models.PositiveIntegerField()


class Genre(models.Model):
    album = models.ManyToManyField(Album)
    artist = models.ManyToManyField(Artist)
    name = models.CharField(max_length=128)


class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)
    duration_ms = models.PositiveIntegerField()
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    track_number = models.PositiveIntegerField()






