from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from DBProjectDelta.settings import BASE_DIR, CACHE_SIZE
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache

from Surfer import Surfer
import Utils
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


def iframe_page(request):
    content = open(BASE_DIR + r'/templates/' + 'so-express-view.html').read()
    return HttpResponse(content)


def ask(request):
    if not request.session.has_key('username'):
        return HttpResponse(json.dumps({'redirectUrl':'/signup'}), content_type="application/json", status=200)

    if request.method == "POST":
        so = Surfer(True)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        question = body["Question"]
        service = body["Service"]

        # clean
        user_query_service = service.replace("\"", "")
        user_query_search = question.replace("\"", "")

        if user_query_service.lower() not in Utils.method_mapping:
            print '[Error code #2]: invalid or unsupported service!'
            exit(1)

        user_query_service = user_query_service.lower()
        lucky_charm = so.get_lucky(user_query_search, Utils.method_mapping[user_query_service])

        hit = cache.checkCache(so, lucky_charm)
        if hit:
            return HttpResponse(json.dumps(hit['sourceobj']), content_type="application/json", status=200)

        try:
            mytitle = so.get_title()
            myquestion = so.get_question_description()
            myanswer_tuple = so.get_best_answer()
            myanswer = myanswer_tuple[0]
            is_best = myanswer_tuple[1]
            mytags = so.get_topic_tags()
        except:
            return HttpResponse(status=404)

        # prepare response body
        overall = dict()
        overall['user-query'] = user_query_search.encode("utf-8")
        overall['url'] = lucky_charm.encode("utf-8")
        overall['title'] = mytitle if mytitle is None else mytitle.encode("utf-8")
        overall['question'] = myquestion if myquestion is None else myquestion.encode("utf-8")
        overall['answer'] = myanswer if myanswer is None else myanswer.encode("utf-8")
        overall['tags'] = mytags
        overall['is_top_rated'] = is_best

        cache.populate_cache(overall, lucky_charm)

        return HttpResponse(json.dumps(overall), content_type="application/json", status=200)

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