from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect 
from django.shortcuts import render_to_response 
from django.template import RequestContext
from models import *
from datetime import date

# Create your views here.


class IndexView(ListView):
    template_name = 'index.html'
    model = Activity

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     context['teams'] = SubTeam.objects.all()
    #     return context


class ActivityView(ListView):
    template_name = 'activity.html'
    model = ActivityRatio

    def get_context_data(self, **kwargs):
        context = super(ActivityView, self).get_context_data(**kwargs)
        context['teams'] = SubTeam.objects.all()
        return context


def add(request):
    print request.POST
    if 'activity_date' in request.POST:
        activity_date = request.POST['activity_date']
    if 'selectActivity' in request.POST:
        selectactivity = request.POST['selectActivity']
        activity_type = ActivityRatio.objects.filter(activity_name=selectactivity)[0]
    if 'selectSubTeam' in request.POST:
        subteam = request.POST['selectSubTeam']
        sub_team = SubTeam.objects.filter(subteam_name=subteam)[0]
    if 'MemberNumber' in request.POST:
        member_number = request.POST['MemberNumber']
    if 'activity_comments' in request.POST:
        comment = request.POST['activity_comments']
    if 'money' in request.POST:
        money = request.POST['money']

    activity = Activity(activity_time=activity_date, member_number=member_number, maint_time=date.today(),  
            activity_type=activity_type, money=money, comment=comment, sub_team=sub_team, team=sub_team.team)
    activity.save()
    return HttpResponseRedirect("/index") 
    # return render_to_response('/index', context_instance=RequestContext(request))


class RatioView(ListView):
    template_name = 'ratio.html'
    model = ActivityRatio


class ChangeView(TemplateView):
    template_name = 'change.html'


class AddActivityView(TemplateView):
    template_name = 'add_activity.html'


class ChargeView(ListView):
    template_name = 'charge.html'
    model = Team



def add_charge(request):
    print request.POST
    if 'charge_date' in request.POST:
        date = request.POST['charge_date']
    if 'selectTeam' in request.POST:
        selectTeam = request.POST['selectTeam']
        team = Team.objects.filter(team_name=selectTeam)[0]
    if 'formal_number' in request.POST:
        formal_number = request.POST['formal_number']
    if 'intern_number' in request.POST:
        intern_number = request.POST['intern_number']

    charge_money = int(formal_number) * 75 + int(intern_number) * 45
    print 'charge_money is:', charge_money
    charge = Charge(charge_date=date, charge_money=charge_money, team=team, formal_number=formal_number,intern_number=intern_number)
    charge.save()
    print 'done'
    return HttpResponseRedirect("/index") 

