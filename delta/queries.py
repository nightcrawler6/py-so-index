####### PLAYLIST VIEW ###########

# delete a song from a playlist
delete_song_from_playlist_query = "DELETE FROM playlist_song \
                                     WHERE playlist_song.playlist_id={} AND playlist_song.song_id='{}';"

# add a song to a playlist
add_song_to_playlist_query = "INSERT INTO playlist_song (playlist_id, song_id) \
                                VALUES \
                                ({},'{}');"

add_song_to_playlist_bulk_query = "INSERT INTO playlist_song (playlist_id, song_id) \
                                VALUES \
                                {};"

# get songs by search query
get_songs_by_search_query = "SELECT song.song_id, song.title, song.duration, song.release_date, song.views, artist.artist_name, album.album_title, category.category_name \
                                FROM song, artist, album, category \
                                WHERE song.artist_id=artist.artist_id AND \
                                song.album_id=album.album_id AND \
                                song.category_id=category.category_id AND \
                                (song.title LIKE '%{0}%' OR artist.artist_name LIKE '%{0}%' OR album.album_title LIKE '%{0}%');"

# get all songs in a playlist
get_songs_in_playlist_query = "SELECT song.song_id, song.title, song.duration,  artist.artist_name, album.album_title, category.category_name \
                                FROM playlist, playlist_song, song, artist, album, category \
                                WHERE playlist.playlist_id=playlist_song.playlist_id AND \
                                playlist_song.song_id=song.song_id AND \
                                song.artist_id=artist.artist_id AND \
                                song.album_id=album.album_id AND \
                                song.category_id=category.category_id AND \
                                playlist.playlist_id='{0}';"

# get all playlists that belong to a user
get_personal_playlists_query = "SELECT DISTINCT playlist.playlist_id, playlist.username, playlist.playlist_title, playlist.creation_date, playlist.cover_uri \
                                    FROM auth_user, playlist \
                                    WHERE auth_user.username = playlist.username AND \
                                    auth_user.username = '{0}';"

# add playlist to a user space
add_playlist_to_user_query = "INSERT INTO playlist \
                                (username, playlist_title, creation_date, cover_uri) \
                                VALUES \
                                ('{}', '{}', '{}', '{}'); \
                                select last_insert_id();"


most_listened_genre_by_user_query = "select ghost.category_name, frequency from ( \
                                        select count(*) as frequency, category.category_name, category.category_id as inner_id \
                                        from auth_user, playlist, playlist_song, song, category where \
                                        auth_user.username=playlist.username AND \
                                        playlist.playlist_id=playlist_song.playlist_id AND \
                                        song.song_id=playlist_song.song_id AND \
                                        song.category_id=category.category_id AND \
                                        auth_user.username='{0}' \
                                        group by category.category_id \
                                        ) as ghost, category \
                                    where inner_id=category.category_id \
                                    having frequency = (select max(temp) from( \
                                                            select count(*) as temp \
                                                                from auth_user, playlist, playlist_song, song, category where \
                                                                auth_user.username=playlist.username AND \
                                                                playlist.playlist_id=playlist_song.playlist_id AND \
                                                                song.song_id=playlist_song.song_id AND \
                                                                song.category_id=category.category_id AND \
                                                                auth_user.username='{0}' \
                                                                group by category.category_id \
                                                                ) as ghost2 )"

most_listened_artist_by_user_query = "select ghost.artist_name, frequency from ( \
                                        select count(*) as frequency, artist.artist_name, artist.artist_id as inner_id \
                                        from auth_user, playlist, playlist_song, song, artist where \
                                        auth_user.username=playlist.username AND \
                                        playlist.playlist_id=playlist_song.playlist_id AND \
                                        song.song_id=playlist_song.song_id AND \
                                        song.artist_id=artist.artist_id AND \
                                        auth_user.username='{0}' \
                                        group by artist.artist_id \
                                        ) as ghost, artist \
                                    where inner_id=artist.artist_id \
                                    having frequency = (select max(temp) from( \
                                                            select count(*) as temp \
                                                                from auth_user, playlist, playlist_song, song, artist where \
                                                                auth_user.username=playlist.username AND \
                                                                playlist.playlist_id=playlist_song.playlist_id AND \
                                                                song.song_id=playlist_song.song_id AND \
                                                                song.artist_id=artist.artist_id AND \
                                                                auth_user.username='{0}' \
                                                                group by artist.artist_id \
                                                                ) as ghost2 )"

get_most_popular_genre_all_users_query = "select f.username, f.category_name, f.frequency \
                                            from(\
                                                select username, max(frequency) as maximal_value\
                                                from( \
                                                    select auth_user.username, category.category_name, count(*) frequency\
                                                    from auth_user join playlist on auth_user.username=playlist.username \
                                                    join playlist_song on playlist_song.playlist_id=playlist.playlist_id \
                                                    join song on song.song_id=playlist_song.song_id \
                                                    join category on category.category_id=song.category_id \
                                                    group by username, category_name) as ghost \
                                                where username != '{}' \
                                                group by username \
                                            ) as ghost2 inner join (select auth_user.username, category.category_name, count(*) frequency \
                                                    from auth_user join playlist on auth_user.username=playlist.username \
                                                    join playlist_song on playlist_song.playlist_id=playlist.playlist_id\
                                                    join song on song.song_id=playlist_song.song_id \
                                                    join category on category.category_id=song.category_id \
                                                    group by username, category_name) as f on f.username = ghost2.username and f.frequency = ghost2.maximal_value "


get_most_popular_artist_all_users_query = "select f.username, f.artist_name, f.frequency \
                                            from( \
                                                select username, max(frequency) as maximal_value \
                                                from( \
                                                    select auth_user.username, artist.artist_name, count(*) frequency \
                                                    from auth_user join playlist on auth_user.username=playlist.username \
                                                    join playlist_song on playlist_song.playlist_id=playlist.playlist_id\
                                                    join song on song.song_id=playlist_song.song_id\
                                                    join artist on artist.artist_id=song.artist_id\
                                                    group by username, artist_name) as ghost\
                                                where username != '{}'\
                                                group by username\
                                            ) as ghost2 inner join (select auth_user.username, artist.artist_name, count(*) frequency \
                                                    from auth_user join playlist on auth_user.username=playlist.username \
                                                    join playlist_song on playlist_song.playlist_id=playlist.playlist_id\
                                                    join song on song.song_id=playlist_song.song_id\
                                                    join artist on artist.artist_id=song.artist_id\
                                                    group by username, artist_name) as f on f.username = ghost2.username and f.frequency = ghost2.maximal_value "

number_of_playlists_user_query = "select auth_user.username, auth_user.first_name, auth_user.last_name, count(*) \
                                    from playlist, auth_user where \
                                    playlist.username = auth_user.username and \
                                    auth_user.username != '{}' \
                                    group by auth_user.username"

user_follows_query = "select follows.following_username from follows where follower_username = '{}'"


user_follower_query = "select follows.follower_username from follows where following_username = '{}'"

songs_count_in_playlist_user_query = "select playlist.playlist_id, count(*) as freq \
                                        from playlist, auth_user, playlist_song, song \
                                        where auth_user.username='{}' and \
                                        playlist.username=auth_user.username and \
                                        playlist.playlist_id=playlist_song.playlist_id and \
                                        song.song_id=playlist_song.song_id \
                                        group by auth_user.username, playlist.playlist_id"

follow_user_query = "insert into follows (follower_username, following_username) values ('{}', '{}');"

unfollow_user_query = "delete from follows where follower_username='{}' and following_username='{}'"

recommended_songs_query = "select song.song_id, song.title, song.duration, artist.artist_name, album.album_title, category.category_name \
                              from song, artist, category, album \
                              where \
                              artist.artist_id=song.artist_id and \
                              (artist.artist_name IN {} or \
                              category.category_name IN {}) and  \
                              category.category_id=song.category_id and \
                              song.album_id=album.album_id\
                              order by rand() LIMIT {};"

average_song_per_playlist_user_query = "select avg(freq) from (" + songs_count_in_playlist_user_query + ") as ghost_alias"