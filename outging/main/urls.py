from django.conf.urls import patterns, url, include
from views import *


urlpatterns = patterns('',
    url('^index$', IndexView.as_view()),
    url('^activity$', ActivityView.as_view()),
    url('^ratio$', RatioView.as_view()),
    url('^change$', ChangeView.as_view()),
    url('^add$', 'main.views.add'),
    url('^add_charge$', 'main.views.add_charge'),
    url('^charge$', ChargeView.as_view()),
)
