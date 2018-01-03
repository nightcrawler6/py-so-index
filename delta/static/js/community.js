$(document).ready(function () {
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

function buildAllUsers(allUsersInfo){
    $('#members-container').css('display','none');
    for(var username in allUsersInfo){
        var userObj = allUsersInfo[username];
        var fname = userObj.fname;
        var lname = userObj.lname;
        var popular_category = renderArray(userObj.genre);
        var popular_artist = renderArray(userObj.artist);
        var playlists_num = userObj.playlists_num;
        var following = userObj.follow;

        var wrapperDiv = $('<div class="col-lg-3 col-sm-3 text-center mb-3"></div>');
        var h3 = $('<h3>' + fname + ' ' + lname + '<p><small>' + username + '</small><p></h3>');
        var innerp = $('<p><strong>' + playlists_num + '</strong> Playlists<br>' +
            'Dominant genre: <strong>' + popular_category + '</strong><br>' +
            'Mostly listens to <strong>' + popular_artist + '</strong></p>');
        if(following){
            var button = $('<button class="button follow"><span>View!</span></button>');
        }
        else{
            var button = $('<button class="button foreign"><span>Follow!</span></button>');
        }

        $(wrapperDiv).append(h3);
        $(wrapperDiv).append(innerp);
        $(wrapperDiv).append(button);

        $('#members-container').append(wrapperDiv);
    }
    $('#members-container').fadeIn();
}


/***
 * Renders an array into a comma separated string
 * @param Array
 *          Array of items
 * @returns {string}
 */
function renderArray(Array){
    var rendered = "";
    for (var i in Array){
        rendered += Array[i] + ", ";
    }

    rendered = rendered.substring(0, rendered.length-2);
    return rendered;
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