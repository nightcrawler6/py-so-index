####### PLAYLIST VIEW ###########

# delete a song from a playlist
delete_song_from_playlist_query = "DELETE FROM playlist_song \
                                     WHERE playlist_song.PlaylistId={} AND playlist_song.SongId={};"

# add a song to a playlist
add_song_to_playlist_query = "INSERT INTO playlist_song (PlaylistId, SongId) \
                                VALUES \
                                ({},{});"

# get songs by search query
get_songs_by_search_query = "SELECT song.SongId, song.Title, song.Duration, song.PublicDate, song.Views, artist.Name, album.Title, category.name \
                                FROM song, artist, album, category \
                                WHERE song.ArtistId=artist.ArtistId AND \
                                song.AlbumId=album.AlbumId AND \
                                song.CategoryId=category.categoryId AND \
                                (song.Title LIKE '%{0}%' OR artist.Name LIKE '%{0}%' OR album.Title LIKE '%{0}%');"

# get all songs in a playlist
get_songs_in_playlist_query = "SELECT song.SongId, song.Title, song.Duration,  artist.Name, album.Title, category.name \
                                FROM playlist, playlist_song, song, artist, album, category \
                                WHERE playlist.PlaylistId=playlist_song.PlaylistId AND \
                                playlist_song.SongId=song.SongId AND \
                                song.ArtistId=artist.ArtistId AND \
                                song.AlbumId=album.AlbumId AND \
                                song.CategoryId=category.categoryId AND \
                                playlist.PlaylistId='{0}';"

# get all playlists that belong to a user
get_personal_playlists_query = "SELECT DISTINCT playlist.PlaylistId, playlist.Username, playlist.Title, playlist.CreationDate, playlist.cover_uri \
                                    FROM auth_user, playlist \
                                    WHERE auth_user.username = playlist.Username AND \
                                    auth_user.username = '{0}';"

# add playlist to a user space
add_playlist_to_user_query = "INSERT INTO playlist \
                                (Username, Title, CreationDate, cover_uri) \
                                VALUES \
                                ('{}', '{}', '{}', '{}')"

most_listened_genre_by_user_query = "select ghost.name, frequency from ( \
                                        select count(*) as frequency, category.name, category.categoryId as inner_id \
                                        from auth_user, playlist, playlist_song, song, category where \
                                        auth_user.username=playlist.Username AND \
                                        playlist.PlaylistId=playlist_song.PlaylistId AND \
                                        song.SongId=playlist_song.SongId AND \
                                        song.CategoryId=category.categoryId AND \
                                        auth_user.username='{0}' \
                                        group by category.categoryId \
                                        ) as ghost, category \
                                    where inner_id=category.categoryId \
                                    having frequency = (select max(temp) from( \
                                                            select count(*) as temp \
                                                                from auth_user, playlist, playlist_song, song, category where \
                                                                auth_user.username=playlist.Username AND \
                                                                playlist.PlaylistId=playlist_song.PlaylistId AND \
                                                                song.SongId=playlist_song.SongId AND \
                                                                song.CategoryId=category.categoryId AND \
                                                                auth_user.username='{0}' \
                                                                group by category.categoryId \
                                                                ) as ghost2 )"

most_listened_artist_by_user_query = "select ghost.name, frequency from ( \
                                        select count(*) as frequency, artist.name, artist.ArtistId as inner_id \
                                        from auth_user, playlist, playlist_song, song, artist where \
                                        auth_user.username=playlist.Username AND \
                                        playlist.PlaylistId=playlist_song.PlaylistId AND \
                                        song.SongId=playlist_song.SongId AND \
                                        song.ArtistId=artist.ArtistId AND \
                                        auth_user.username='{0}' \
                                        group by artist.ArtistId \
                                        ) as ghost, artist \
                                    where inner_id=artist.ArtistId \
                                    having frequency = (select max(temp) from( \
                                                            select count(*) as temp \
                                                                from auth_user, playlist, playlist_song, song, artist where \
                                                                auth_user.username=playlist.Username AND \
                                                                playlist.PlaylistId=playlist_song.PlaylistId AND \
                                                                song.SongId=playlist_song.SongId AND \
                                                                song.ArtistId=artist.ArtistId AND \
                                                                auth_user.username='{0}' \
                                                                group by artist.ArtistId \
                                                                ) as ghost2 )"

get_most_popular_genre_all_users_query = "select f.username, f.name, f.frequency \
                                            from(\
                                                select username, max(frequency) as maximal_value\
                                                from( \
                                                    select auth_user.username, category.name, count(*) frequency\
                                                    from auth_user join playlist on auth_user.username=playlist.Username \
                                                    join playlist_song on playlist_song.PlaylistId=playlist.PlaylistId \
                                                    join song on song.SongId=playlist_song.SongId \
                                                    join category on category.categoryId=song.CategoryId \
                                                    group by username, name) as ghost \
                                                where username != '{}' \
                                                group by username \
                                            ) as ghost2 inner join (select auth_user.username, category.name, count(*) frequency \
                                                    from auth_user join playlist on auth_user.username=playlist.Username \
                                                    join playlist_song on playlist_song.PlaylistId=playlist.PlaylistId\
                                                    join song on song.SongId=playlist_song.SongId \
                                                    join category on category.categoryId=song.CategoryId \
                                                    group by username, name) as f on f.username = ghost2.username and f.frequency = ghost2.maximal_value "


get_most_popular_artist_all_users_query = "select f.username, f.name, f.frequency \
                                            from( \
                                                select username, max(frequency) as maximal_value \
                                                from( \
                                                    select auth_user.username, artist.Name, count(*) frequency \
                                                    from auth_user join playlist on auth_user.username=playlist.Username \
                                                    join playlist_song on playlist_song.PlaylistId=playlist.PlaylistId\
                                                    join song on song.SongId=playlist_song.SongId\
                                                    join artist on artist.ArtistId=song.ArtistId\
                                                    group by username, name) as ghost\
                                                where username != '{}'\
                                                group by username\
                                            ) as ghost2 inner join (select auth_user.username, artist.Name, count(*) frequency \
                                                    from auth_user join playlist on auth_user.username=playlist.Username \
                                                    join playlist_song on playlist_song.PlaylistId=playlist.PlaylistId\
                                                    join song on song.SongId=playlist_song.SongId\
                                                    join artist on artist.ArtistId=song.ArtistId\
                                                    group by username, name) as f on f.username = ghost2.username and f.frequency = ghost2.maximal_value "

number_of_playlists_user_query = "select auth_user.username, auth_user.first_name, auth_user.last_name, count(*) \
                                    from playlist, auth_user where \
                                    playlist.Username = auth_user.username and \
                                    auth_user.username != '{}' \
                                    group by auth_user.username"

user_follows_query = "select followers.FollowingID from followers where FollowerID = '{}'"


user_follower_query = "select followers.FollowerID from followers where FollowingID = '{}'"

songs_count_in_playlist_user_query = "select playlist.Title, count(*) \
                                        from playlist, auth_user, playlist_song, song \
                                        where auth_user.username='{}' and \
                                        playlist.Username=auth_user.username and \
                                        playlist.PlaylistId=playlist_song.PlaylistId and \
                                        song.SongId=playlist_song.SongId \
                                        group by auth_user.username, playlist.Title"