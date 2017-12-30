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
    for(var i in raw_data){
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
            $($("#amazing-table")[0]).fadeIn();
        }
        else {
            $($("#amazing-table")[0]).css('display', 'none');
        }
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