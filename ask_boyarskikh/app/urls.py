# pylint: disable=invalid-name

from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from app import views

JS_INFO_DICT = {
    'packages': ('app',),
}

urlpatterns = [
    url(r'^hello/?$', views.hello, name='HelloWorld'),
    url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='search'),  # TODO
    url(r'^user/?$', views.user, name='user'),
    url(r'^user/(?P<uid>\w+)/?$', views.user, name='user'),
    url(r'^tag/(?P<tid>\w+)/?$', views.tag, name='tag'),
    url(r'^signup/?$', views.registration, name='registration'),
    url(r'^profile/edit/?$', views.settings, name='settings'),
    url(r'^question/(?P<qid>\d+)/?$', views.question, name='question'),
    url(r'^hot/?$', views.hot, name='hot'),
    url(r'^ask/?$', views.ask, name='ask'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^intapi/?$', views.intapi, name='intapi'),
    url(r'^jsi18n/?$', JavaScriptCatalog.as_view(**JS_INFO_DICT), name='jsi18n'),
]
