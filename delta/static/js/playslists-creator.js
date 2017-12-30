$(document).ready(function () {
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
        var cardtracks = $("<h5>10 Tracks</h5>");
        var cardtext = $("<p class='card-text'>Total Duration: 0</p>");
        $(cardbody).append(cardtitle);
        $(cardbody).append(cardtracks);
        $(cardbody).append(cardtext);

        var cardfoot = $("<div class='card-footer'><small class='text-muted'>" + playlistObject.created_on + "</small></div>");

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
                    buildSongsTable(response, $($("#amazing-table")[0]));
                    $($("#amazing-table")[0]).fadeIn();
                },
                error: function () {
                    alert("something went wrong...")
                }
            });
        }
        else {
            $('.table').remove();
            $($("#amazing-table")[0]).css('display', 'none');
        }
    })
}

function buildSongsTable(raw_data, container){
    var table = $('<table class="table"></table>');
    var thead = $('<thead><tr></tr></thead>');
    var trhead = $('<tr></tr>')
    var col1 = $('<td scope="col">#</td>');
    var col2 = $('<td scope="col">Title</td>');
    var col3 = $('<td scope="col">Duration</td>');
    var col4 = $('<td scope="col">Artist</td>');
    var col5 = $('<td scope="col">Album</td>');
    $(trhead).append(col1);
    $(trhead).append(col2);
    $(trhead).append(col3);
    $(trhead).append(col4);
    $(trhead).append(col5);
    $(thead).append(trhead);
    $(table).append(thead);
    var tbody = $('<tbody></tbody>');
    for(var i in raw_data){
        var songobj = raw_data[i];
        var tr = $('<tr></tr>');
        var col1 = $('<th></th>');
        var delbtn = $('<button type="button" class="btn btn-danger" style="margin-top:3px">X</button>');
        $(delbtn).data('songid', songobj.id);
        $(delbtn).on("click", function(){
           alert($(this).data('songid'));
        });
        $(col1).append(delbtn);
        var col2 = $('<td>' + songobj.title + '</td>');
        var col3 = $('<td>' + songobj.duration + '</td>');
        var col4 = $('<td>' + songobj.artist + '</td>');
        var col5 = $('<td>' + songobj.album + '</td>');
        $(tr).append(col1);
        $(tr).append(col2);
        $(tr).append(col3);
        $(tr).append(col4);
        $(tr).append(col5);
        $(tbody).append(tr);
    }
    $(table).append(tbody);
    $(container).append(table);
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