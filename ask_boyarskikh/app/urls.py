"""questandansw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.i18n import javascript_catalog

from app import views

js_info_dict = {
    'packages': ('app',),
}

urlpatterns = [
    url(r'^hello/?$', views.hello, name='HelloWorld'),
    url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='search'), #TODO
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
    url(r'^jsi18n/?$', javascript_catalog, js_info_dict, name='jsi18n'),
    url(r'^events/?$', views.events, name='events'),
]
