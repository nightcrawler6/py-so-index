from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache


import json

# navigate to the home page
@ensure_csrf_cookie
@never_cache
def musico(request):
    isAuth = request.user.is_authenticated()
    context = {"authenticated": isAuth, "user": request.user}
    return render(request, "index.html", context)

# navigate to the one click playlists generator page
@ensure_csrf_cookie
@never_cache
def generator(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "generator.html", context)
    return redirect("/musico_register")

# navigate to the music community tab
@ensure_csrf_cookie
@never_cache
def community(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "community.html", context)
    return redirect("/musico_register")

# navigate to the "who is following" tab
@ensure_csrf_cookie
@never_cache
def who_is_following(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "who_is_following.html", context)
    return redirect("/musico_register")

# navigate to the playlists studio page
def playlists(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        context = {"authenticated": isAuth, "user": request.user}
        return render(request, "playlists-creator.html", context)
    return redirect("/musico_register")

# navigate to the sign up page
@ensure_csrf_cookie
@never_cache
def musico_register(request):
    isAuth = request.user.is_authenticated()
    if isAuth:
        return redirect("/musico")
    return render(request, 'signup.html')

# perform a user login
@ensure_csrf_cookie
@never_cache
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    # init a user object container
    user = None

    # check if user exists in the db
    if User.objects.filter(username=username).exists():
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect("/musico")
        else:
            return redirect("/musico_register")
    return redirect("/musico_register")


# perform a user sign up procedure
@ensure_csrf_cookie
@never_cache
def register_user(request):
    # user is already logged in
    if request.session.has_key('username'):
        user = authenticate(request.session['username'])
        print request.session['username']
        return redirect("/musico",{'user':user})

    # user is not logged in - check if creation is valid
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # init a user object container
        user = None

        # truncate operations if user is already taken
        if User.objects.filter(username=username).exists():
            user = None
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

        # authenticate the user and redirect to home page if signup is successful
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect("/musico")
        else:
            return redirect("/musico_register")


# perform a clean log out of the user
def logout_user(request):
    if request.session.has_key('username'):
        logout(request)
        # del request.session['username']
    return redirect("/musico")
