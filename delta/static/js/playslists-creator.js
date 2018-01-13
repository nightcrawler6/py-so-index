$(document).ready(function () {
    $('#silence').on('click', function () {
        $('#player_body').empty();
    });
    $.ajax({
        type: "GET",
        url: "/get_my_playlists",
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            console.log(response);
            buildPlaylistView(response);
            registerTransitions();
        },
        error: function () {
            alert("something went wrong...")
        }
    });

    $('.cf').keypress(function (e) {
        var key = e.which;
        if (key == 13)  // the enter key code
        {
            e.preventDefault();
            if ($('.cf').data('active-playlist') != undefined) {
                var query_string = $('#search-bar').val();
                $('#search-bar').val('');
                $('#searchModal h4').text("Results for: " + query_string);
                var data = {
                    'search_string': query_string
                }
                $.ajax({
                    type: "POST",
                    url: "/search_songs",
                    data: JSON.stringify(data),
                    headers: {"X-CSRFToken": getCookie("csrftoken")},
                    contentType: 'application/json; charset=utf-8',
                    success: function (response) {
                        buildSongsTable(response, $('#search-table-modal')[0], false);
                        $("#searchModal").modal('show');
                    },
                    error: function () {
                        alert("something went wrong...")
                    }
                });
            }
        }
    });
});

/***
 * Builds a set of playlist cards given raw data received from the server and attaches them directly
 * to html page
 * @param raw_data
 *      raw data containing basic playlist info
 */
function buildPlaylistView(raw_data) {
    var container = $('.row')[1];
    for (var i in raw_data) {
        var playlistObject = raw_data[i];

        var col = $("<div id='" + playlistObject.id + "' class='col-lg-3 col-md-6 mb-3 play'></div>");
        col.data('playlist-id', playlistObject.id);

        var card = $("<div class='card'></div>");

        var link = $("<a href='#'></a>");
        var img = $("<img class='card-img-top' src='" + playlistObject.cover_uri + "' alt=''>");
        $(link).append(img);

        var cardbody = $("<div class='card-body'></div>");
        var cardtitle = $("<h4 class='class-title'>" + playlistObject.title + "</h4>");
        var cardtracks = $("<h5>" + playlistObject.total + " Tracks</h5>");
        var du = msToTime(parseInt(playlistObject.duration));
        var cardtext = $("<p class='card-text'>Total Duration: " + du + "</p>");
        $(cardbody).append(cardtitle);
        $(cardbody).append(cardtracks);
        $(cardbody).append(cardtext);

        var cardfoot = $("<div class='card-footer'></div>");

        var del = $('<i style="float: right; cursor: pointer;" class="icon-remove play-del"></i>');
        del.data('playlist-id', playlistObject.id);
        registerDeletePlaylist(del);
        var creation = $("<small class='text-muted'>Created on: " + playlistObject.created_on + "</small>");

        $(cardfoot).append(creation);
        $(cardfoot).append(del);

        $(card).append(link);
        $(card).append(cardbody);
        $(card).append(cardfoot);

        $(col).append(card);

        $(container).append(col);
    }
}

function msToTime(s) {
    var ms = s % 1000;
    s = (s - ms) / 1000;
    var secs = s % 60;
    s = (s - secs) / 60;
    var mins = s % 60;
    var hrs = (s - mins) / 60;
    if(mins<10){ mins = '0'+mins;}

    return '<strong>' + hrs + ':' + mins + '</strong> (hr/min)';
}

function registerDeletePlaylist(btn) {
    var id = btn.data('playlist-id');
    var data = {
        'id': id
    }
    $(btn).on('click', function () {
        $.ajax({
            type: "POST",
            url: "/delete_playlist",
            data: JSON.stringify(data),
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            contentType: 'application/json; charset=utf-8',
            success: function (response) {
                $($(btn).parent().parent().parent()).fadeOut(function () {
                    $(this).remove();
                });
            },
            error: function () {
                alert("something went wrong...")
            }
        });
    });
}

/***
 * Iterates over all the card elements and registers the on click handler
 * The handler defines the following behavior:
 *      hide every other element that is different than clicked
 *      display table with songs in playlist (card element)
 */
function registerTransitions() {
    $('.play a').on("click", function (event) {
        var obj = $(event.target).parent().parent().parent()[0];


        if ($("#amazing-table").css('display') == 'none') {
            var playlistid = $(obj).data('playlist-id');
            data = {
                'playlistId': playlistid
            }
            $.ajax({
                type: "POST",
                url: "/get_playlist_songs",
                data: JSON.stringify(data),
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                contentType: 'application/json; charset=utf-8',
                success: function (response) {
                    toggleAll(obj, function () {
                    });
                    buildSongsTable(response, $($("#amazing-table")[0]), true);
                    $($("#amazing-table")[0]).fadeIn();
                    $('.cf').slideDown();
                    $('.cf').data('active-playlist', playlistid);
                    $('.play-del').css('display','none');
                },
                error: function () {
                    alert("something went wrong...")
                }
            });
        }
        else {
            $('.table').remove();
            $($("#amazing-table")[0]).css('display', 'none');
            $('.play-del').css('display','block');
            toggleAll(obj);
            $('.cf').slideUp();
            $('.cf').removeData('active-playlist');
        }
    })
}

function toggleAll(obj) {
    var objId = obj.id;
    var allCards = $('.play');
    var toHide = [];
    for (var i = 0; i < allCards.length; i++) {
        var cur = allCards[i];
        if ($(cur).data('playlist-id') == $(obj).data('playlist-id')) {
            continue;
        }
        else {
            if ($(cur).css('display') == 'none') {
                $(cur).css('display', 'block');
            }
            else {
                $(cur).css('display', 'none');
            }
        }
    }
}

function buildSongsTable(raw_data, container, isDelete) {
    $(container).empty();
    var buttonType = 'btn btn-success add';
    if (isDelete) {
        buttonType = 'btn btn-danger del';
    }
    var table = $('<table class="table"></table>');
    var thead = $('<thead></thead>');
    var trhead = $('<tr></tr>')
    var col1 = $('<th scope="col">#</th>');
    var col2 = $('<th scope="col">Title</th>');
    var col3 = $('<th scope="col">Duration</th>');
    var col4 = $('<th scope="col">Artist</th>');
    var col5 = $('<th scope="col">Album</th>');
    var col6 = $('<th scope="col">Genre</th>');
    $(trhead).append(col1);
    $(trhead).append(col2);
    $(trhead).append(col3);
    $(trhead).append(col4);
    $(trhead).append(col5);
    $(trhead).append(col6);
    $(thead).append(trhead);
    $(table).append(thead);
    var tbody = $('<tbody></tbody>');
    for (var i in raw_data) {
        var songobj = raw_data[i];
        var tr = $('<tr></tr>');
        var col1 = $('<th></th>');
        var icon = '<i class="icon-ok"></i>';
        if (isDelete) {
            icon = '<i class="icon-remove"></i>'
        }
        var delbtn = $('<button type="button" class="' + buttonType + '" style="cursor:pointer">' + icon + '</button>');
        $(delbtn).data('songid', songobj.id);
        if (isDelete) {
            $(delbtn).on("click", function () {
                //alert($(this).data('songid'));
                editPlaylist(isDelete, $('.cf').data('active-playlist'), $(this).data('songid'), null);
            });
        }
        else {
            $(delbtn).on("click", function () {
                //alert($(this).data('songid'));
                editPlaylist(isDelete, $('.cf').data('active-playlist'), $(this).data('songid'), this);
            });
        }

        $(col1).append(delbtn);
        var col2 = $('<td><a href="#">' + songobj.title + '</a></td>');
        $(col2).data('title', songobj.title);
        $(col2).data('artist', songobj.artist);
        registerPlayMethod(col2);
        var ms = songobj.duration;
        min = Math.floor((ms / 1000 / 60) << 0);
        sec = Math.floor((ms / 1000) % 60);
        if (sec < 10) {
            sec = "0" + sec.toString()
        }
        ;

        var col3 = $('<td>' + min + ":" + sec + '</td>');
        var col4 = $('<td>' + songobj.artist + '</td>');
        var col5 = $('<td>' + songobj.album + '</td>');
        var col6 = $('<td>' + songobj.category + '</td>');
        $(tr).append(col1);
        $(tr).append(col2);
        $(tr).append(col3);
        $(tr).append(col4);
        $(tr).append(col5);
        $(tr).append(col6);
        $(tbody).append(tr);
    }
    $(table).append(tbody);
    $(container).append(table);
}

function editPlaylist(isDelete, playlistId, songId, srcBtn) {
    var servlet = "";
    var containerId = "";
    if (!isDelete) {
        servlet = "/add_song_to_playlist";
    }
    else {
        servlet = "/remove_song_from_playlist";
    }
    data = {
        'playlistId': playlistId,
        'songId': songId
    }
    $.ajax({
        type: "POST",
        url: servlet,
        data: JSON.stringify(data),
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            //$('#searchModal').modal('hide');
            $.ajax({
                type: "POST",
                url: "/get_playlist_songs",
                data: JSON.stringify(data),
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                contentType: 'application/json; charset=utf-8',
                success: function (response) {
                    $($("#amazing-table")[0]).fadeOut('slow', function () {
                        buildSongsTable(response, $($("#amazing-table")[0]), true);
                        $($("#amazing-table")[0]).fadeIn();
                    });
                    if (srcBtn != null) {
                        var tag = $('<span id="added_tag" style="display: none; font-size:10px; cursor: pointer;"class="badge badge-success">added!</span>\n');
                        $($(srcBtn).parent().parent().find('td')[0]).append(tag);
                        $('#added_tag').fadeIn().delay(1000).fadeOut(function () {
                            $('#added_tag').remove();
                        });
                    }
                },
                error: function () {
                    alert("something went wrong...")
                }
            });
        },
        error: function () {
            alert("something went wrong...")
        }
    });
}

function registerPlayMethod(col) {
    $(col).on('click', function () {
        if ($('#loader').length) {
            return;
        }
        $(col).append("<img id='loader' src='static/media/ajax-loader.gif'></img>");
        title = $(col).data('title');
        artist = $(col).data('artist');
        data = {
            'title': title,
            'artist': artist
        }
        $.ajax({
            type: "POST",
            url: "/play_song",
            data: JSON.stringify(data),
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            contentType: 'application/json; charset=utf-8',
            success: function (response) {
                redirect_url = response.embed;
                $('#player_body').empty();
                $('#player_body').append('<iframe src= "' + redirect_url + '"></iframe>');
                $('#loader').remove();
                //$('#player').modal('show');
            },
            error: function () {
                alert("something went wrong...")
            }
        });
    })
}

/***
 * Retrieves the cookie name set on current page
 * @param c_name
 *      name of cookie entry
 * @returns {*}
 */
function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}