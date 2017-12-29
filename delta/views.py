from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from DBProjectDelta.settings import BASE_DIR, CACHE_SIZE
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache

import json
from cache import Cache

# init cache singletone
cache = Cache(CACHE_SIZE)

#for reference ONLY!
#@ensure_csrf_cookie
#@never_cache
#def so_index(request):
#    if request.session.has_key('username'):
#        return render(request, 'so-index.html')
#    else:
#        return render(request, 'test_login.html')

@ensure_csrf_cookie
@never_cache
def musico(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
@never_cache
def musico_register(request):
    return render(request, 'signup.html')

@ensure_csrf_cookie
def register_user(request):
    # user is already logged in
    if request.session.has_key('username'):
        print request.session['username']
        return redirect("/musico")

    # user is not logged in - trying to create new account
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = None

        if User.objects.filter(username=username).exists():
            user = None
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            return redirect("/musico")
        else:
            return redirect("/musico_register")

def signup(request):
    if request.session.has_key('username'):
        print request.session['username']
        return redirect("home-view")
    if request.method == "GET":
        return render(request, 'test_login.html')
    else:
        response = {'response':None}
        credentials_unicode = request.body.decode('utf-8')
        credentials = json.loads(credentials_unicode)
        user = credentials['user']
        password = credentials['password']
        userobj = User.objects.get(username=user)
        # user, created = User.objects.get_or_create(username=user)
        '''if user:
            user.set_password(password)
            user.save()
            request.session['username'] = credentials['user']
            response['response'] = 'added successfully!'
        else:'''
        if userobj:
            user = authenticate(username=user, password=password)
            if user is not None:
                request.session['username'] = credentials['user']
                response['url'] = '/home'
                return HttpResponse(json.dumps(response), content_type="application/json", status=200)
            else:
                response['url'] = '/signup'
                return HttpResponse(json.dumps(response), content_type="application/json", status=200)
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
    return redirect("signup-view")