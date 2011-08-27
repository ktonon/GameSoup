from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.expressions.views',
    url(r'^$', 'index', name='index'),
    url(r'^render-(?P<type>grammar|syntax)/$', 'render', name='render'),
)
