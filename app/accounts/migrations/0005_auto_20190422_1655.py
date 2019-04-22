# Generated by Django 2.2 on 2019-04-22 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190409_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='users',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='users',
        ),
        migrations.AddField(
            model_name='user',
            name='artists',
            field=models.ManyToManyField(related_name='artists', to='accounts.Artist'),
        ),
        migrations.AddField(
            model_name='user',
            name='genres',
            field=models.ManyToManyField(related_name='genres', to='accounts.Genre'),
        ),
        migrations.AlterField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(related_name='albums', to='accounts.Artist'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='albums',
            field=models.ManyToManyField(related_name='genres', to='accounts.Album'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='artists',
            field=models.ManyToManyField(related_name='genres', to='accounts.Artist'),
        ),
        migrations.AlterField(
            model_name='track',
            name='artists',
            field=models.ManyToManyField(related_name='tracks', to='accounts.Artist'),
        ),
    ]
