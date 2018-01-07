from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from DBProjectDelta.settings import BASE_DIR, CACHE_SIZE
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.db import connection
import datetime
import queries
import requests

import json


@ensure_csrf_cookie
@never_cache
def musico(request):
    isAuth = request.user.is_authenticated()
    context = {"authenticated": isAuth, "user": request.user}
    return render(request, "index.html", context)


@ensure_csrf_cookie
@never_cache
def generator(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "generator.html", context)
    return redirect("/musico_register")


@ensure_csrf_cookie
@never_cache
def community(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "community.html", context)
    return redirect("/musico_register")


@ensure_csrf_cookie
@never_cache
def who_is_following(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "who_is_following.html", context)
    return redirect("/musico_register")


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
        query = queries.add_playlist_to_user_query.format(username, title, date, album_uri)
        cursor.execute(query)
    return redirect('/playlists_studio')


def get_personal_playlists(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    playlist_owner = request.user
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        playlist_owner = body['username']

    with connection.cursor() as cursor:
        query = queries.get_personal_playlists_query.format(playlist_owner)
        cursor.execute(query)
        row = cursor.fetchall();

        query_count_songs = queries.songs_count_in_playlist_user_query.format(playlist_owner)
        cursor.execute(query_count_songs)
        song_count = cursor.fetchall();

        song_count_dict = {m[0]:m[1] for m in song_count}

        response = []

        for tup in row:
            entry = {}
            entry['id'] = tup[0]
            entry['user'] = tup[1]
            entry['title'] = tup[2]
            if entry['title'] in song_count_dict:
                entry['total'] = song_count_dict[entry['title']]
            else:
                entry['total'] = 0

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

        query = queries.get_songs_in_playlist_query.format(playlistId)

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
            entry['category'] = tup[5]
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

        query = queries.get_songs_by_search_query.format(search)

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
            entry['category'] = tup[7]

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

        query = queries.add_song_to_playlist_query.format(playlistId, songId)

        cursor.execute(query)
        row = cursor.fetchall()
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

        query = queries.delete_song_from_playlist_query.format(playlistId, songId)

        cursor.execute(query)
        row = cursor.fetchall()
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json", status=200)


def get_most_listened_genre_by_user(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        query = queries.most_listened_genre_by_user_query.format(request.user)

        cursor.execute(query)
        row = cursor.fetchall()

        response = []

        for tup in row:
            entry = {}
            entry['category_name'] = tup[0]
            entry['category_count'] = tup[1]

            response.append(entry)
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def get_most_listened_artist_by_user(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        query = queries.most_listened_artist_by_user_query.format(request.user)

        cursor.execute(query)
        row = cursor.fetchall()

        response = []

        for tup in row:
            entry = {}
            entry['artist_name'] = tup[0]
            entry['artist_count'] = tup[1]

            response.append(entry)
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def get_number_of_playlists(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    with connection.cursor() as cursor:
        query = queries.number_of_playlists_user_query.format(request.user)

        cursor.execute(query)
        row = cursor.fetchone()

        response = {}
        response['count'] = row[0]
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def populate_users_preview_data(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    current_user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    who_is_following_view = body['view']

    with connection.cursor() as cursor:
        popular_artists_query = queries.get_most_popular_artist_all_users_query.format(current_user.username)
        popular_genre_query = queries.get_most_popular_genre_all_users_query.format(current_user.username)
        enum_playlists_query = queries.number_of_playlists_user_query.format(current_user.username)
        who_is_following_ids_query = queries.user_follower_query.format(current_user.username)
        followers_ids_query = queries.user_follows_query.format(current_user.username)

        cursor.execute(popular_artists_query)
        popular_artists_dict = cursor.fetchall()

        cursor.execute(popular_genre_query)
        popular_genres_dict = cursor.fetchall()

        cursor.execute(enum_playlists_query)
        playlists_num_and_data = cursor.fetchall()

        cursor.execute(who_is_following_ids_query)
        following_id_dict = set([m[0] for m in cursor.fetchall()])

        cursor.execute(followers_ids_query)
        follower_id_dict = set([m[0] for m in cursor.fetchall()])

        response = {}
        for tup in playlists_num_and_data:
            entry = {}
            username = tup[0]
            if who_is_following_view and username not in following_id_dict:
                continue
            fname = tup[1]
            lname = tup[2]
            playlists_num = tup[3]
            entry['fname'] = fname
            entry['lname'] = lname
            entry['playlists_num'] = playlists_num
            entry['follow'] = username in follower_id_dict
            response[username] = entry

        for tup in popular_genres_dict:
            username = tup[0]
            if who_is_following_view and username not in following_id_dict:
                continue
            genre = tup[1]
            data = response[username]
            if not data.has_key('genre'):
                data['genre'] = []
            data['genre'].append(genre)

        for tup in popular_artists_dict:
            username = tup[0]
            if who_is_following_view and username not in following_id_dict:
                continue
            artist = tup[1]
            data = response[username]
            if not data.has_key('artist'):
                data['artist'] = []
            data['artist'].append(artist)

        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def magic(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    current_user = request.user

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id_set = body['id-set']

        fulldate = datetime.datetime.now()
        date = '{}-{}-{}'.format(fulldate.year, fulldate.month, fulldate.day)

        create_playlist_query = queries.add_playlist_to_user_query.format(current_user, "Magic Playlist", date, "static/media/magic.jpg")
        with connection.cursor() as cursor:
            cursor.execute(create_playlist_query)
            cursor.fetchall()
            playlistId = cursor.lastrowid

        with connection.cursor() as cursor:
            statement = ""
            for songId in id_set:
                value = "({},{})".format(playlistId, songId)
                statement += value + ","
            statement = statement[:-1]

            insert_bulk = queries.add_song_to_playlist_bulk_query.format(statement)
            cursor.execute(insert_bulk)

        return HttpResponse(json.dumps({}), content_type="application/json", status=200)

    with connection.cursor() as cursor:
        popular_artists_query = queries.get_most_popular_artist_all_users_query.format(current_user.username)
        popular_genre_query = queries.get_most_popular_genre_all_users_query.format(current_user.username)
        who_is_following_ids_query = queries.user_follower_query.format(current_user.username)
        followers_ids_query = queries.user_follows_query.format(current_user.username)
        average_songs_query = queries.average_song_per_playlist_user_query.format(current_user.username)
        personal_fav_artist = queries.most_listened_artist_by_user_query.format(current_user.username)
        personal_fav_genre = queries.most_listened_genre_by_user_query.format(current_user.username)

        cursor.execute(popular_artists_query)
        popular_artists_dict = cursor.fetchall()

        cursor.execute(popular_genre_query)
        popular_genres_dict = cursor.fetchall()

        cursor.execute(who_is_following_ids_query)
        following_id_dict = set([m[0] for m in cursor.fetchall()])

        cursor.execute(followers_ids_query)
        follower_id_dict = set([m[0] for m in cursor.fetchall()])

        cursor.execute(average_songs_query)
        average_playlist_length = int(float(cursor.fetchone()[0]))+1

        cursor.execute(personal_fav_artist)
        personal_artist = set([m[0] for m in cursor.fetchall()])

        cursor.execute(personal_fav_genre)
        personal_genre = set([m[0] for m in cursor.fetchall()])

        response = {}

        common_genres = set()
        common_artist = set()

        for tup in popular_genres_dict:
            username = tup[0]
            if username not in following_id_dict and username not in follower_id_dict:
                continue
            genre = tup[1]
            common_genres.add(genre)

        for tup in popular_artists_dict:
            username = tup[0]
            if username not in following_id_dict and username not in follower_id_dict:
                continue
            artist = tup[1]
            common_artist.add(artist)

        # strategy 1: aggregate all results together and bring it!
        personal_artist = personal_artist.union(common_artist)
        personal_genre = personal_genre.union(common_genres)
        magic_query = queries.recommended_songs_query.format(buildStringy(personal_artist), buildStringy(personal_genre), 10)
        cursor.execute(magic_query)
        magic_songs = cursor.fetchall()

        wrapper = {}
        response = []
        song_ids = []
        for tup in magic_songs:
            entry = {}
            entry['songId'] = tup[0]
            song_ids.append(tup[0])
            entry['title'] = tup[1]
            entry['duration'] = tup[2]
            entry['artist'] = tup[3]
            entry['album'] = tup[4]
            entry['category'] = tup[5]

            response.append(entry)
        wrapper['data'] = response
        wrapper['save_data'] = song_ids

        return HttpResponse(json.dumps(wrapper), content_type="application/json", status=200)


def follow_user(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    current_user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    to_follow_user = body['toFollow']

    with connection.cursor() as cursor:
        follow_query = queries.follow_user_query.format(current_user, to_follow_user)
        cursor.execute(follow_query)

        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json", status=200)


def unfollow_user(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    current_user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    to_unfollow_user = body['toUnfollow']

    with connection.cursor() as cursor:
        follow_query = queries.unfollow_user_query.format(current_user, to_unfollow_user)
        cursor.execute(follow_query)

        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json", status=200)


def play_song(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    current_user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    title = body['title'].replace(' ', '+')
    artist = body['artist'].replace(' ', '+')
    google_query_url = "http://www.google.com/search?q=site:youtube.com+"+title+"+"+artist+"&btnI"
    get = requests.get(google_query_url)
    redirect_url = get.url

    if redirect_url is not None:
        redirect_url = redirect_url.replace('watch?v=','embed/')

    redirect_url += '?autoplay=1'

    return HttpResponse(json.dumps({'embed': redirect_url}), content_type="application/json", status=200)


def buildStringy(some_set):
    out = "("
    for element in some_set:
        out += "'" + element + "', "
    out = out[:-2] + ")"
    return out
