function verifySignupForm(){
    var fname = $('#signupform #first_name').val();
    var lname = $('#signupform #last_name').val();
    var username = $('#signupform #username').val();
    var email = $('#signupform #email').val();
    var password = $('#signupform #password').val();
    var vpassword = $('#signupform #password_confirmation').val();
    var valid = true;
    if(fname == ""){
        valid = false;
    }
    else if(lname == ""){
        valid = false;
    }
    else if(username == ""){
        valid = false;
    }
    else if(email == ""){
        valid = false;
    }
    else if(password == ""){
        valid = false;
    }
    else if(vpassword == ""){
        valid = false;
    }

    if(valid){
        if (password != vpassword){
            $('#match-pass-warn').slideDown().delay(2500).slideUp();
            return false;
        }
    }
    if(!valid){
        $('#fill-all-warn').slideDown().delay(2500).slideUp();
    }
    return valid;
}

function verifyLoginForm(){
    var username = $('#loginform #username-login').val();
    var password = $('#loginform #password-login').val();
    var valid = true;
    if(username == ""){
        valid = false;
    }
    if(password == ""){
        valid = false;
    }
    if(!valid){
        $('#fill-all-warn').slideDown().delay(2500).slideUp();
    }
    return valid;
}