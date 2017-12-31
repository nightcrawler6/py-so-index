from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from DBProjectDelta.settings import BASE_DIR, CACHE_SIZE
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.db import connection
import datetime

import json
from cache import Cache

# init cache singletone
cache = Cache(CACHE_SIZE)

@ensure_csrf_cookie
@never_cache
def musico(request):
    isAuth = request.user.is_authenticated()
    context = {"authenticated": isAuth, "user": request.user}
    return render(request, "index.html", context)

def playlists(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "playlists-creator.html", context)
    return redirect("/musico_register")

@ensure_csrf_cookie
@never_cache
def musico_register(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        return redirect("/musico")
    return render(request, 'signup.html')

@ensure_csrf_cookie
@never_cache
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = None

    if User.objects.filter(username=username).exists():
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect("/musico")
        else:
            return redirect("/musico_register")


@ensure_csrf_cookie
@never_cache
def register_user(request):
    # user is already logged in
    if request.session.has_key('username'):
        user = authenticate(request.session['username'])
        print request.session['username']
        return redirect("/musico",{'user':user})

    # user is not logged in - trying to create new account
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = None

        if User.objects.filter(username=username).exists():
            user = None
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect("/musico")
        else:
            return redirect("/musico_register")

def logout_user(request):
    if request.session.has_key('username'):
        logout(request)
        # del request.session['username']
    return redirect("/musico")


############################# Private methods - DB #############3

def add_playlist_user_space(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    fulldate = datetime.datetime.now();

    username = request.user
    title = request.POST['title']
    album_uri = request.POST['photo-album']
    date = '{}-{}-{}'.format(fulldate.year, fulldate.month, fulldate.day)

    with connection.cursor() as cursor:
        query = "INSERT INTO playlist \
                    (Username, Title, CreationDate, cover_uri) \
                    VALUES \
                    ('{}', '{}', '{}', '{}')".format(username, title, date, album_uri)
        cursor.execute(query)
    return redirect('/playlists_studio')


def get_personal_playlists(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        query = "SELECT DISTINCT playlist.PlaylistId, playlist.Username, playlist.Title, playlist.CreationDate, playlist.cover_uri \
                    FROM auth_user, playlist \
                    WHERE auth_user.username = playlist.Username AND \
                    auth_user.username = '{0}';".format(request.user)
        cursor.execute(query)
        row = cursor.fetchall();

        response = []

        for tup in row:
            entry = {}
            entry['id'] = tup[0]
            entry['user'] = tup[1]
            entry['title'] = tup[2]

            date = tup[3]
            entry['created_on'] = "{}-{}-{}".format(date.year, date.month, date.day)
            entry['cover_uri'] = tup[4]
            response.append(entry)
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def get_songs_in_playlist(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status':'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        playlistId = body['playlistId']
        query = "SELECT song.SongId, song.Title, song.Duration,  artist.Name, album.Title \
                    FROM playlist, playlist_song, song, artist, album \
                    WHERE playlist.PlaylistId=playlist_song.PlaylistId AND \
                    playlist_song.SongId=song.SongId AND \
                    song.ArtistId=artist.ArtistId AND \
                    song.AlbumId=album.AlbumId AND \
                    playlist.PlaylistId='{0}';".format(playlistId)

        cursor.execute(query)
        row = cursor.fetchall();

        response = []

        for tup in row:
            entry = {}
            entry['id'] = tup[0]
            entry['title'] = tup[1]
            entry['duration'] = tup[2]
            entry['artist'] = tup[3]
            entry['album'] = tup[4]
            response.append(entry)

        return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def get_songs_by_search(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status':'unauthorized'}), content_type="application/json", status=404)
    with connection.cursor() as cursor:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        search = body['search_string']

        query = "SELECT song.SongId, song.Title, song.Duration, song.PublicDate, song.Views, artist.Name, album.Title \
                    FROM song, artist, album \
                    WHERE song.ArtistId=artist.ArtistId AND \
                    song.AlbumId=album.AlbumId AND \
                    (song.Title LIKE '%{0}%' OR artist.Name LIKE '%{0}%' OR album.Title LIKE '%{0}%');".format(search)

        cursor.execute(query)
        row = cursor.fetchall();

        response = []

        for tup in row:
            entry = {}
            entry['id'] = tup[0]
            entry['title'] = tup[1]
            entry['duration'] = tup[2]

            date = tup[3]
            entry['publication-date'] = "{}-{}-{}".format(date.year, date.month, date.day)

            entry['views'] = tup[4]
            entry['artist'] = tup[5]
            entry['album'] = tup[6]

            response.append(entry)

        return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def add_song_to_playlist(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        playlistId = body['playlistId']
        songId = body['songId']

        query = "INSERT INTO playlist_song (PlaylistId, SongId) \
                  VALUES \
                  ({},{});".format(playlistId, songId)

        cursor.execute(query)
        row = cursor.fetchall();
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json", status=200)


def delete_song_from_playlist(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        playlistId = body['playlistId']
        songId = body['songId']

        query = "DELETE FROM playlist_song \
                    WHERE playlist_song.PlaylistId={} AND playlist_song.SongId={};".format(playlistId, songId)

        cursor.execute(query)
        row = cursor.fetchall();
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json", status=200)

