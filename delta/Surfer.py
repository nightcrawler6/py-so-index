import requests
import lxml.html as magic
import Utils
import sys

headers = {
    'User-Agent': 'Mozilla/5.0\
    (Macintosh; Intel Mac OS X 10_10_1)\
    AppleWebKit/537.36\
    (KHTML, like Gecko)\
    Chrome/39.0.2171.95\
    Safari/537.36'
}

class Surfer:
    def __init__(self, debug):
        self.url = None
        self.source = None
        self.sourceObject = None
        self.debug = debug

    def __str__(self):
        return "StackOverflow Surfer: " + self.url

    def get_source(self):
        if Utils.noneorempty(self.url):
            raise NameError('URL was not set properly!')
        if Utils.noneorempty(self.source):
            self.source = requests.get(self.url, headers=headers).content
        return self.source

    def get_source_object(self):
        if Utils.noneorempty(self.sourceObject):
            if Utils.noneorempty(self.sourceObject):
                self.source = self.get_source()
            self.sourceObject = magic.fromstring(self.source)
        return self.sourceObject

    def get_best_answer(self):
        best_answer_xpath = '//div[@id="answers" or @class="answer"]//td[@class="answercell"]/div'
        rated_best_answer_xpath = '//span[@class="vote-accepted-on load-accepted-answer-date"]'

        best_answer_element = self.sourceObject.xpath(best_answer_xpath)
        is_rated_best = len(self.sourceObject.xpath(rated_best_answer_xpath)) != 0
        best_answer = ""
        if len(best_answer_element) == 0:
            if self.debug:
                print "No best answer yet!"
            return None
        for elem in best_answer_element[0]:
            best_answer += magic.tostring(elem)
        return (best_answer, is_rated_best)

    def get_question_description(self):
        question_xpath = '//td[@class="postcell"]//div[@class="post-text"]'
        question_element = self.sourceObject.xpath(question_xpath)
        question = ""
        if len(question_element) == 0:
            if self.debug:
                print "Could not find question!"
            return None
        question += magic.tostring(question_element[0])

        return question

    def get_title(self):
        title_xpath = '//div[@id="question-header"]/h1/a'
        title_element = self.sourceObject.xpath(title_xpath)
        title = ""
        if len(title_element) == 0:
            if self.debug:
                print "No title? hmmmm weird..."
            return None
        title += magic.tostring(title_element[0])

        return Utils.cleanhtml(title)

    def get_lucky(self, query_question, service):
        query_question = query_question.replace(" ", "+")
        PREFIX = service()
        SUFFIX = Utils.get_feeling_lucky_suffix()
        url_to_get_lucky = PREFIX + query_question + '&oq' + query_question + SUFFIX
        if self.debug:
            print "BROWSING TO: " + url_to_get_lucky
        get = requests.get(url_to_get_lucky)
        html = magic.fromstring(get.content)
        bingo1 = None
        bingo2 = None
        try:
            bingo1 = html.xpath("//a[@dir='ltr']/@href")[0].split("=")[1]
            if len(bingo1) != 0:
                if self.debug:
                    print "MATCH AT: " + bingo1
                return bingo1
        except:
            if self.debug:
                print "Could not fetch search from source, checking redirects..."
        bingo2 = get.url
        if self.debug:
            print "MATCH AT: " + bingo2
        return bingo2

    def get_topic_tags(self):
        tags_xpath = '//div[@class="post-taglist"]//a'
        tag_elements = self.sourceObject.xpath(tags_xpath)
        tags = []
        if len(tag_elements) == 0:
            if self.debug:
                print "No tags for questions"
            return []
        for tag_obj in tag_elements:
            tags.append(tag_obj.text)
        return tags

    def think_it_through(self):
        return None

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url
        self.get_source()
        self.get_source_object()

'''
so = Surfer(False)

# user = raw_input("What do you need to know? --> ")
if len(sys.argv) != 3:
    print '[Error code #1]: Two few arguments; please specify question and service!'
    exit(1)
user_query_search = sys.argv[1]
user_query_service = sys.argv[2]

# clean
user_query_service = user_query_service.replace("\"","")
user_query_search = user_query_search.replace("\"","")

if user_query_service.lower() not in Utils.method_mapping:
    print '[Error code #2]: invalid or unsupported service!'
    exit(1)

user_query_service = user_query_service.lower()
lucky_charm = so.get_lucky(user_query_search, Utils.method_mapping[user_query_service])

so.set_url(lucky_charm)

mytitle = so.get_title()
myquestion = so.get_question_description()
myanswer_tuple = so.get_best_answer()
myanswer = myanswer_tuple[0]
is_best = myanswer_tuple[1]
mytags = so.get_topic_tags()
overall = {}
overall['user-query'] = user_query_search.encode("utf-8")
overall['url'] = lucky_charm.encode("utf-8")
overall['title'] = mytitle if mytitle is None else mytitle.encode("utf-8")
overall['question'] = myquestion if myquestion is None else myquestion.encode("utf-8")
overall['answer'] = myanswer if myanswer is None else myanswer.encode("utf-8")
overall['tags'] = mytags
overall['is_top_rated'] = is_best

print overall
'''
