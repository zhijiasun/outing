from django.conf.urls import patterns, url, include
from views import *


urlpatterns = patterns('',
    # url('^dologin$', 'main.views.dologin'),
    url('login$', 'main.views.dologin'),
    url('logout$', 'main.views.dologout'),
    url('register$', 'main.views.register'),
    url('selectteam$', SelectTeamView.as_view()),
    url('index$', IndexView.as_view()),
    url('activity$', ActivityView.as_view()),
    url('ratio$', RatioView.as_view()),
    url('change$', ChangeView.as_view()),
    url('add$', 'main.views.add'),
    url('addteam$', 'main.views.addteam'),
    url('add_charge$', 'main.views.add_charge'),
    url('charge$', ChargeView.as_view()),
)
