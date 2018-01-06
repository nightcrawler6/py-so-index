"""DBProjectDelta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from delta.views import *
from delta.dbtester import *

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^musico_register', musico_register, name="musico-register"),
    url(r'^musico', musico, name="home-view"),
    url(r'^check-db', checkconnectivity, name="query"),
    url(r'^signup', register_user, name="register_new_user"),
    url(r'^signout', logout_user, name="logout_user"),
    url(r'^login', login_user, name="login_user"),
    url(r'^playlists_studio', playlists, name="manage_playlist"),
    url(r'^music_community', community, name="community"),
    url(r'^who_is_following', who_is_following, name="who_is_following"),
    url(r'^generator', generator, name="generator"),
    url(r'^get_my_playlists', get_personal_playlists, name="playlists"),
    url(r'^get_playlist_songs', get_songs_in_playlist, name="songs"),
    url(r'^create_playlist', add_playlist_user_space, name="create_playlist"),
    url(r'^search_songs', get_songs_by_search, name="search_songs"),
    url(r'^add_song_to_playlist', add_song_to_playlist, name="add_song"),
    url(r'^remove_song_from_playlist', delete_song_from_playlist, name="delete_song"),
    url(r'^get_popular_genre_user', get_most_listened_genre_by_user, name="most_popular_genre"),
    url(r'^get_popular_artist_user', get_most_listened_artist_by_user, name="most_popular_artist"),
    url(r'^populate_user_data', populate_users_preview_data, name="populate_user_data"),
    url(r'^follow_user', follow_user, name="follow_user"),
    url(r'^unfollow_user', unfollow_user ,name="unfollow_user"),
    url(r'^play_song', play_song, name="play_song"),
    url(r'^magic', magic, name="magin"),
]
