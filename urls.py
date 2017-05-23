from django.conf.urls import url

from questions.views import questions_list, questions_detail

urlpatterns = [
    url(r'^$', questions_list, name='questions_list'),
    url(r'^(?P<question_id>[0-9]+)/$', questions_detail, name='questions_detail'),
]
