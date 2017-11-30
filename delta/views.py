from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from DBProjectDelta.settings import BASE_DIR
from Surfer import Surfer
import Utils
import json


@ensure_csrf_cookie
def so_index(request):
    return render(request, 'so-index.html')


def iframe_page(request):
    content = open(BASE_DIR + r'/templates/' + 'so-express-view.html').read()
    return HttpResponse(content)


def ask(request):
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

        so.set_url(lucky_charm)

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

        return HttpResponse(json.dumps(overall), content_type="application/json", status=200)



