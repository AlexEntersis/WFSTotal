__author__ = 'Alex'
from django.conf.urls import include, url


urlpatterns = [
    url(r'^upload/$', 'basic_parser.views.upload'),

    url(r'^parse/$', 'basic_parser.views.parser'),
    url(r'^statistics/$', 'basic_parser.views.statistics'),
    url(r'^download_all/$', 'basic_parser.db.download_all'),
    url(r'', 'basic_parser.views.basic'),




]