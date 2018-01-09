from django.db import connection
import datetime
import queries
import requests
from django.http import HttpResponse
from django.shortcuts import redirect
import json


# add a new playlist to the user's playlists studio
def add_playlist_user_space(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    # get current creation date
    fulldate = datetime.datetime.now();

    username = request.user
    title = request.POST['title']
    album_uri = request.POST['photo-album']
    date = '{}-{}-{}'.format(fulldate.year, fulldate.month, fulldate.day)

    # commit addition to db
    with connection.cursor() as cursor:
        query = queries.add_playlist_to_user_query.format(username, title, date, album_uri)
        cursor.execute(query)
    return redirect('/playlists_studio')


# fetch all playlists registered under current user in session
def get_personal_playlists(request):
    isAuth = request.user.is_authenticated()
    if not isAuth:
        return HttpResponse(json.dumps({'status': 'unauthorized'}), content_type="application/json", status=404)

    playlist_owner = request.user
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        playlist_owner = body['username']

    # retrieve raw data and parse into json
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
            if entry['id'] in song_count_dict:
                entry['total'] = song_count_dict[entry['id']]
            else:
                entry['total'] = 0

            date = tup[3]
            entry['created_on'] = "{}-{}-{}".format(date.year, date.month, date.day)
            entry['cover_uri'] = tup[4]
            response.append(entry)
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


# fetch all songs from selected playlist
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


# perform a db query for a set of songs determined by user free text search
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


# add new song to existing playlist
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


# delete a song from an existing playlist
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


# fetch the most listened genre by current user in the session
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


# fetch the most listened to artist based on current user in session
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


# get number of playlists in users studio
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


# returns basic raw data regarding each user in the registered program
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

# generated a brand new playlist based on different "MAGIC" factors!
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
        magic_query = queries.recommended_songs_query.format(buildStringy(personal_artist), buildStringy(personal_genre), average_playlist_length)
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

# simple user follow operation
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


# simple user unfollow operation
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


# play a song from youtube by generating a relevant embed URL and redirecting it back to the user
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


# helper function to render sets or arrays into a string representation
def buildStringy(some_set):
    out = "("
    for element in some_set:
        out += "'" + element + "', "
    out = out[:-2] + ")"
    return out