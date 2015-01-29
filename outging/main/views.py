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
from django.http import Http404
from django.core.context_processors import csrf
from models import *
from datetime import date
import logging
logger = logging.getLogger(__name__)

# Create your views here.


# class LoginView(TemplateView):
#     template_name = 'login.html'

FORMAL_AMOUNT = 75
INTERN_AMOUNT = 45

for ratio in AdjustRatio.objects.all():
    if ratio.name is 1:
        FORMAL_AMOUNT = ratio.amount
    elif ratio.name is 2:
        INTERN_AMOUNT = ratio.amount


"""
no need to judge "-123" and "0123"
for "-123", "-123".isdigit() will return False
for "0123", "0123".isdigit() return True, but int("0123") will return integer 123
"""
def IsInteger(str):
    if str and str.isdigit() and str[0] is not '0':
        return True
    else:
        return False

def IsIntegerOrFloat(str):
    if str and IsInteger(str):
        return True
    elif str and str.count(".") is 1 and IsInteger(str.replace(".","")):
        return True
    else:
        return False


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
        c = {}
        c.update(csrf(request))
        context = RequestContext(request)
        return render_to_response("login.html", c, context) 



def dologout(request):
    logout(request)
    return HttpResponseRedirect("/login") 


# class RegisterView(TemplateView):
#     template_name = 'register.html'


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        if not username:
            messages.add_message(request, messages.ERROR, '请输入注册用户名')
            context = RequestContext(request)
            return render_to_response("register.html", context) 
        email = request.POST['email']
        if not email:
            messages.add_message(request, messages.ERROR, '请输入注册邮箱')
            context = RequestContext(request)
            return render_to_response("register.html", context) 

        password = request.POST['pwd']
        if not password:
            messages.add_message(request, messages.ERROR, '请输入密码')
            context = RequestContext(request)
            return render_to_response("register.html", context) 

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
        context = RequestContext(request)
        return render_to_response('register.html', context)


def addteam(request):
    if request.user.is_authenticated():
        user = request.user
        print request.POST['selectTeam']
        team = Team.objects.filter(team_name=request.POST['selectTeam'])[0]

        if Hr.objects.filter(user=user):
            return HttpResponseRedirect("/index")
        else:
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


# class AdjustView(ListView):
#     template_name = 'adjust.html'
#     model = ActivityRatio

#     def get_context_data(self, **kwargs):
#         context = super(AdjustView, self).get_context_data(**kwargs)
#         teams = Team.objects.all()
#         context['teams'] = teams
#         return context


@login_required
def adjust(request):
    if request.method == 'POST':
        selectTeam = request.POST.get('selectTeam', '')
        if selectTeam:
            try:
                team = Team.objects.get(team_name = selectTeam)
            except Team.DoesNotExist:
                logger.error('selectTeam:%s not existed.' % selectTeam)
                messages.add_message(request, messages.ERROR, "selectTeam not existed")
                return HttpResponseRedirect("/adjust") 
        else:
            logger.error('selectTeam is null')
            messages.add_message(request, messages.ERROR, "请输入正确数据")
            return HttpResponseRedirect("/adjust") 

        selectActivity = request.POST.get('selectActivity', '')
        if selectActivity:
            try:
                activity = ActivityRatio.objects.get(activity_name=selectActivity)
            except ActivityRatio.DoesNotExist:
                logger.error('selectActivity:%s not existed.' % selectActivity)
                messages.add_message(request, messages.ERROR, "selectTeam not existed")
                return HttpResponseRedirect("/adjust") 
        else:
            logger.error('selectActivity is null')
            messages.add_message(request, messages.ERROR, "请输入正确数据")
            return HttpResponseRedirect("/adjust") 

        money = request.POST.get('money', '')
        if not money and not IsIntegerOrFloat:
            logger.error('money is null')
            messages.add_message(request, messages.ERROR, "请输入正确数据")
            return HttpResponseRedirect("/adjust") 

        comment = request.POST.get('comment', '')

        record = ChargeRecord(charge_money=money, team=team, activity=activity, comment=comment)
        record.save()
        return HttpResponseRedirect("/balance") 
    else:
        logger.debug('GET request for /adjust')
        c = {'object_list':ActivityRatio.objects.all(), 'teams':Team.objects.all()}
        context = RequestContext(request, c)
        return render_to_response("adjust.html", context) 


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
            try:
                hr = Hr.objects.get(user=self.request.user)
            except Hr.DoesNotExist:
                logger.error('for user:%s,related Hr not existed' % self.request.user.username)
                raise Http404 # not a proper way to return 404 page
            team = hr.team
            logger.info('team is %s' % team.team_name)
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
            context = super(ActivityView, self).get_context_data(**kwargs)
            return context
        else:
            hr = Hr.objects.get(user=self.request.user)
            team = hr.team
            context = super(ActivityView, self).get_context_data(**kwargs)
            context['teams'] = SubTeam.objects.filter(team=team)
            temp_context = calculateMoney(self.request.user)
            context.update(temp_context)
            return context

#添加活动消费
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

    if activity_date and activity_type and subteam and sub_team and IsInteger(member_number) and IsIntegerOrFloat(money):
        logger.debug("activity_date:%s,sub_team is:%s,member_number is:%s,money is:%s" % (activity_date,subteam,member_number,money))
        activity = Activity(activity_time=activity_date, member_number=member_number, maint_time=date.today(),  
            activity_type=activity_type, money=money, comment=comment, sub_team=sub_team, team=sub_team.team)
        activity.save()
        return HttpResponseRedirect("/index") 
    else:
        logger.error("input data error")
        messages.add_message(request, messages.ERROR, "请输入正确数据")
        return HttpResponseRedirect("/activity") 


class RatioView(ListView):
    template_name = 'ratio.html'
    model = ActivityRatio

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RatioView, self).dispatch(*args, **kwargs)


class ChangeView(TemplateView):
    template_name = 'change.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChagenView, self).dispatch(*args, **kwargs)


class AddActivityView(TemplateView):
    template_name = 'add_activity.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddActivityView, self).dispatch(*args, **kwargs)


# class ChargeView(ListView):
#     template_name = 'charge.html'
#     model = Team

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(ChargeView, self).dispatch(*args, **kwargs)


class ChargeHistoryView(ListView):
    template_name = 'history.html'
    model = Charge

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChargeHistoryView, self).dispatch(*args, **kwargs)


class BalanceHistoryView(TemplateView):
    template_name = 'balance_history.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BalanceHistoryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        consume = 0
        charge = 0
        balance = {}
        context = {}
        amount = []

        context = super(BalanceHistoryView, self).get_context_data(**kwargs)
        for team in Team.objects.all():
            temp = [team]
            for a in ActivityRatio.objects.all():
                balance[a] = 0

            activity = Activity.objects.filter(team=team)
            for a in activity:
                consume = consume + a.money 
                balance[a.activity_type] = balance[a.activity_type] - a.money

            record = ChargeRecord.objects.filter(team=team)
            for r in record:
                charge = charge + r.charge_money
                balance[r.activity] = balance[r.activity] + r.charge_money

            temp = temp + balance.values()
            amount.append(temp)

        context['amount']=amount
        return context


@login_required
def charge(request):
    print 'fadsfad'
    if request.method == 'POST':
        print 'fadsfad'
        if 'Month' in request.POST:
            month = request.POST['Month']
        if 'selectTeam' in request.POST:
            selectTeam = request.POST['selectTeam']
            team = Team.objects.filter(team_name=selectTeam)[0]
        if 'formal_number' in request.POST:
            formal_number = request.POST['formal_number']
        if 'intern_number' in request.POST:
            intern_number = request.POST['intern_number']

        if month and team and IsInteger(formal_number) and IsInteger(intern_number):
            logger.debug('formal_amount is %d , intern_amout is:%d' % (FORMAL_AMOUNT, INTERN_AMOUNT))
            charge_money = int(formal_number) * FORMAL_AMOUNT + int(intern_number) * INTERN_AMOUNT
            logger.debug('charge_money is:%d' % charge_money)
            try:
                charge = Charge(month=month, charge_money=charge_money, team=team, formal_number=formal_number,intern_number=intern_number)
                charge.save()
            except Exception, e:
                logger.error(e)
            return HttpResponseRedirect("/history") 
        else:
            messages.add_message(request, messages.ERROR, '请输入正确数据')
            return HttpResponseRedirect("/charge") 
    else:
        logger.debug('GET request for /charge')
        c = {'object_list':Team.objects.all()}
        context = RequestContext(request, c)
        return render_to_response("charge.html", context) 
