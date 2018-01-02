$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/mitigation",
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            // assume that I am receiving back a json array such that each element is of the form:
            /*
            {
                'username':<username>,
                'first_name':<first_name>,
                'last_name':<last_name>,
                'top_category':<top>,
                'top_artist':<top2>,
                'playlists_num':<num>
            }
            */
            buildAllUsers(response);
        },
        error: function () {
            alert("something went wrong...")
        }
    });
});

function buildAllUsers(allUsersInfo){

    for(var i in allUsersInfo){
        var userObj = allUsersInfo[i];
        var username = userObj.username;
        var fname = userObj.first_name;
        var lname = userObj.last_name;
        var popular_category = userObj.popular_category;
        var popular_artist = userObj.popular_artist;
        var playlists_num = userObj.playlists_num;

        var wrapperDiv = $('<div class="col-lg-3 col-sm-3 text-center mb-3"></div>');
        var h3 = $('<h3>' + fname + ' ' + lname + '<p><small>' + username + '</small><p></h3>');
        var innerp = $('<p><strong>' + playlists_num + '</strong> Playlists<br>' +
            'Dominant genre: <strong>' + popular_category + '</strong><br>' +
            'Mostly listens to <strong>' + popular_artist + '</strong></p>');
        var button = $('<button class="button"><span>Follow!</span></button>');

        $(wrapperDiv).append(h3);
        $(wrapperDiv).append(innerp);
        $(wrapperDiv).append(button);

        $('#members-container').append(wrapperDiv);
    }
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