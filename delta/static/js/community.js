$(document).ready(function () {
    $('#silence').on('click', function () {
        $('#player_body').empty();
    });
    data = {
        'view': $('html').data('who_is_following')
    }
    $.ajax({
        type: "POST",
        url: "/populate_user_data",
        data: JSON.stringify(data),
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            buildAllUsers(response);
        },
        error: function () {
            alert("something went wrong...")
        }
    });
});

function buildAllUsers(allUsersInfo) {
    $('#members-container').css('display', 'none');
    for (var username in allUsersInfo) {
        var userObj = allUsersInfo[username];
        var fname = userObj.fname;
        var lname = userObj.lname;
        var popular_category = renderArray(userObj.genre);
        var popular_artist = renderArray(userObj.artist);
        var playlists_num = userObj.playlists_num;
        var following = userObj.follow;

        var tag = buildTag(following, username);

        var wrapperDiv = $('<div class="col-lg-3 col-xs-3 text-center mb-3"></div>');
        var h3 = $('<h3>' + fname + ' ' + lname + '</h3>');
        var pUser = $('<p></p>');
        var noBiggy = $('<small>' + username + '</small>');
        $(pUser).append(noBiggy);
        $(pUser).append(tag);
        $(h3).append(pUser);
        var innerp = $('<p><strong>' + playlists_num + '</strong> Playlists<br>' +
            'Dominant genre: <strong>' + popular_category + '</strong><br>' +
            'Mostly listens to <strong>' + popular_artist + '</strong></p>');
        if (following) {
            var button = $('<button class="button follow"><span>View!</span></button>');
            handleClick(button, 'follow');
        }
        else {
            var button = $('<button class="button foreign"><span>Follow!</span></button>');
            handleClick(button, 'foreign');
        }
        $(button).data('username', username);

        $(wrapperDiv).append(h3);
        $(wrapperDiv).append(innerp);
        $(wrapperDiv).append(button);

        $('#members-container').append(wrapperDiv);
    }
    $('#members-container').fadeIn();
}

function buildTag(following, username) {
    var tag = $("");
    if (following) {
        tag = $('<span style="font-size:10px; cursor: pointer;"class="badge badge-success">following</span>\n');
        $(tag).data('username', username);
        handleTagTransition(tag);
    }
    $(tag).hover(
        function () {
            $(this).text('unfollow');
            $(this).removeClass('badge-success');
            $(this).addClass('badge-danger');
        },
        function () {
            $(this).text('following');
            $(this).removeClass('badge-danger');
            $(this).addClass('badge-success');
        }
    )

    return tag;
}

function handleTagTransition(tag) {
    $(tag).on('click', function () {
        data = {
            'toUnfollow': $(this).data('username')
        }
        $.ajax({
            type: "POST",
            url: "/unfollow_user",
            data: JSON.stringify(data),
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            contentType: 'application/json; charset=utf-8',
            success: function (response) {
                var button = $(tag).parent().parent().parent().find('button');
                $(tag).remove();
                $(button).removeClass('follow');
                $(button).addClass('foreign');
                $(button).empty();
                var span = $('<span>Follow!</span>');
                $(button).append(span);
                $(button).unbind();
                handleClick(button, 'foreign');
            },
            error: function () {
                alert("something went wrong...")
            }
        });
    });
}

function handleClick(button, action) {
    if (action == 'foreign') {
        $(button).on('click', function () {
            data = {
                'toFollow': $(this).data('username')
            }
            $.ajax({
                type: "POST",
                url: "/follow_user",
                data: JSON.stringify(data),
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                contentType: 'application/json; charset=utf-8',
                success: function (response) {
                    var tag = buildTag(true, $(button).data('username'));
                    $($(button).parent().find('p')[0]).append(tag);
                    $(button).removeClass('foreign');
                    $(button).addClass('follow');
                    $(button).empty();
                    var span = $('<span>View!</span>');
                    $(button).append(span);
                    $(button).unbind();
                    handleClick(button, 'follow');
                },
                error: function () {
                    alert("something went wrong...")
                }
            });
        });
    }
    if (action == 'follow') {
        $(button).on('click', function () {
            data = {
                'username': $(this).data('username')
            }
            $.ajax({
                type: "POST",
                url: "/get_my_playlists",
                data: JSON.stringify(data),
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                contentType: 'application/json; charset=utf-8',
                success: function (response) {
                    $('.play').remove();
                    $("#amazing-table").css('display', 'none');
                    buildPlaylistView(response);
                    registerTransitions();
                    $('.modal-title').text(data['username'] + "'s Playlists");
                    $('#user_playlists_modal').modal('show');
                },
                error: function () {
                    alert("something went wrong...")
                }
            })
        });
    }
}


/***
 * Renders an array into a comma separated string
 * @param Array
 *          Array of items
 * @returns {string}
 */
function renderArray(Array) {
    var rendered = "";
    for (var i in Array) {
        rendered += Array[i] + ", ";
    }

    rendered = rendered.substring(0, rendered.length - 2);
    return rendered;
}

/***
 * Builds a set of playlist cards given raw data received from the server and attaches them directly
 * to html page
 * @param raw_data
 *      raw data containing basic playlist info
 */
function buildPlaylistView(raw_data) {
    var container = $('.row')[2];
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
        var cardtext = $("<p class='card-text'>Total Duration: 0</p>");
        $(cardbody).append(cardtitle);
        $(cardbody).append(cardtracks);
        $(cardbody).append(cardtext);

        var cardfoot = $("<div class='card-footer'><small class='text-muted'>Created on: " + playlistObject.created_on + "</small></div>");

        $(card).append(link);
        $(card).append(cardbody);
        $(card).append(cardfoot);

        $(col).append(card);

        $(container).append(col);
    }
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
                },
                error: function () {
                    alert("something went wrong...")
                }
            });
        }
        else {
            $('.table').remove();
            $($("#amazing-table")[0]).css('display', 'none');
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

function buildSongsTable(raw_data, container) {
    $(container).empty();
    var table = $('<table class="table"></table>');
    var thead = $('<thead></thead>');
    var trhead = $('<tr></tr>')
    var col2 = $('<th scope="col">Title</th>');
    var col3 = $('<th scope="col">Duration</th>');
    var col4 = $('<th scope="col">Artist</th>');
    var col5 = $('<th scope="col">Album</th>');
    var col6 = $('<th scope="col">Genre</th>');
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
        var col2 = $('<td><a href="#">' + songobj.title + '</a></td>');
        $(col2).data('title', songobj.title);
        $(col2).data('artist', songobj.artist);
        registerPlayMethod(col2);
        var col3 = $('<td>' + songobj.duration + '</td>');
        var col4 = $('<td>' + songobj.artist + '</td>');
        var col5 = $('<td>' + songobj.album + '</td>');
        var col6 = $('<td>' + songobj.category + '</td>');
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