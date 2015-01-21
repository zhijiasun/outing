#coding:utf-8
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect 
from django.shortcuts import render_to_response 
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from models import *
from datetime import date

# Create your views here.


# class LoginView(TemplateView):
#     template_name = 'login.html'


def dologin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/index") 
        else:
            messages.add_message(request, messages.ERROR, 'Username or password invalid.')
            context = RequestContext(request)
            return render_to_response("login.html", context) 
    else:
        context = RequestContext(request)
        return render_to_response("login.html", context) 



def dologout(request):
    logout(request)
    return HttpResponseRedirect("/login") 


# class RegisterView(TemplateView):
#     template_name = 'register.html'


def register(request):
    print '###'
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pwd']
        re_password = request.POST['re_pwd']

        if re_password != password:
            messages.add_message(request, messages.ERROR, '输入密码不一致，请重新输入.')
            context = RequestContext(request)
            return render_to_response("register.html", context) 

        user = User.objects.create_user(username, email, password)
        user.save()
        user = authenticate(username=username,password=password)
        login(request, user)
        return HttpResponseRedirect("/selectteam") 
    else:
        print '>>>>'
        context = RequestContext(request)
        return render_to_response('register.html', context)


def addteam(request):
    if request.user.is_authenticated():
        user = request.user
        print request.POST['selectTeam']
        team = Team.objects.filter(team_name=request.POST['selectTeam'])[0]

        hr = Hr(user=user, team=team)
        hr.save()
        return HttpResponseRedirect("/index") 


def calculateMoney(user):
    consume = 0
    charge = 0
    sum = 0
    balance = {}
    context = {}
    for a in ActivityRatio.objects.all():
        balance[a] = 0
    try:
        hr = Hr.objects.get(user=user)
    except Exception, e:
        print 'object not existed!'
    team = hr.team
    activity = Activity.objects.filter(team=team)
    for a in activity:
        consume = consume + a.money 
        balance[a.activity_type] = balance[a.activity_type] - a.money

    
    record = ChargeRecord.objects.filter(team=team)
    for r in record:
        charge = charge + r.charge_money
        balance[r.activity]=balance[r.activity] + r.charge_money

    sum = charge - consume
    context['sum'] = sum
    context['balance']=balance
    return context


class IndexView(ListView):
    template_name = 'index.html'
    model = Activity

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Activity.objects.all()
            return queryset
        else:
            hr = Hr.objects.filter(user=self.request.user)[0]
            team = hr.team
            queryset = Activity.objects.filter(team=team)
            return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            return context
        else:
            temp_context = calculateMoney(self.request.user)
            context.update(temp_context)
            return context


class SelectTeamView(ListView):
    template_name = 'select_team.html'
    model = Team


class ActivityView(ListView):
    template_name = 'activity.html'
    model = ActivityRatio

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            return context
        else:
            hr = Hr.objects.get(user=self.request.user)
            team = hr.team
            context = super(ActivityView, self).get_context_data(**kwargs)
            context['teams'] = SubTeam.objects.filter(team=team)
            temp_context = calculateMoney(self.request.user)
            context.update(temp_context)
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

