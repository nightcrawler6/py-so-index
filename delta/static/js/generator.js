$(document).ready(function () {
    $('#silence').on('click', function () {
        $('#player_body').empty();
    });
    $('.select-button').on('mouseup', function () {
        $('#generateModal').modal('show');
        $.ajax({
            type: "GET",
            url: "/magic",
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            contentType: 'application/json; charset=utf-8',
            success: function (response) {
                buildSongsTable(response.data, $('#search-table-modal')[0])
                bindSaveParams(response.save_data);
            },
            error: function () {
                alert("something went wrong...")
            }
        });
    });
});

function bindSaveParams(songIds) {
    $('#save-gen').on('click', function () {
        var data = {
            'id-set': songIds
        }
        $.ajax({
            type: "POST",
            url: "/magic",
            data: JSON.stringify(data),
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            contentType: 'application/json; charset=utf-8',
            success: function (response) {
                $('.table').fadeOut('slow', function () {
                    $('#generateModal').modal('hide');
                });
            },
            error: function () {
                alert("something went wrong...")
            }
        });
    })
}

function buildSongsTable(raw_data, container) {
    $('#impress').remove();
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

        var ms = songobj.duration;
        min = Math.floor((ms/1000/60) << 0);
        sec = Math.floor((ms/1000) % 60);
        if(sec<10) {sec = "0"+sec.toString()};

        var col3 = $('<td>' + min + ":" + sec + '</td>');
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