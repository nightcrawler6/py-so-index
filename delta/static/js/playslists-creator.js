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

/*<div id="01" class="col-lg-3 col-md-6 mb-3 play">
                    <div class="card">
                        <a href="#"><img class="card-img-top"
                                         src="https://upload.wikimedia.org/wikipedia/en/thumb/d/dc/Damn._Kendrick_Lamar.jpg/220px-Damn._Kendrick_Lamar.jpg"
                                         alt=""></a>
                        <div class="card-body">
                            <h4 class="card-title">
                                Kendrick Beast Mode!
                            </h4>
                            <h5>12 Tracks</h5>
                            <p class="card-text">Total Duration: 1.9 Hours</p>
                        </div>
                        <div class="card-footer">
                            <small class="text-muted">Public | (30 Likes)</small>
                        </div>
                    </div>
                </div>*/


function buildPlaylistView(raw_data) {
    var container = $('.row')[1];
    for(var i in raw_data){
        var playlistObject = raw_data[i];

        var col = $("<div id='" + playlistObject.id + "' class='col-lg-3 col-md-6 mb-3 play'></div>");
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

function registerTransitions() {
    $('.play a').on("click", function (event) {
        var obj = $(event.target).parent().parent().parent()[0];

        var objId = obj.id;
        var allCards = $('.play');
        var toHide = [];
        for (var i = 0; i < allCards.length; i++) {
            var cur = allCards[i];
            if (cur.id == objId) {
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