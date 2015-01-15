from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class ActivityView(TemplateView):
    template_name = 'activity.html'


class RatioView(TemplateView):
    template_name = 'ratio.html'


class ChangeView(TemplateView):
    template_name = 'change.html'


class AddActivityView(TemplateView):
    template_name = 'add_activity.html'


class ChargeView(TemplateView):
    template_name = 'charge.html'
