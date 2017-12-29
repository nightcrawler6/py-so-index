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

@ensure_csrf_cookie
@never_cache
def so_index(request):
    if request.session.has_key('username'):
        return render(request, 'so-index.html')
    else:
        return render(request, 'test_login.html')

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