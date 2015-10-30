__author__ = 'Alex'


from django.conf.urls import include, url


urlpatterns = [
    url(r'^new_search/$', 'search.views.new_search'),
    url(r'', 'search.views.basic')]
