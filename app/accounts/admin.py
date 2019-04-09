from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Artist, Album, Genre, Track

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Track)