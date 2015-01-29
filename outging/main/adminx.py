#coding:utf-8
from xadmin.sites import site
from main.models import *


class TeamAdmin(object):
    list_display = ('team_name', 'team_leader')


class SubTeamAdmin(object):
    list_display = ('subteam_name', 'subteam_leader', 'team')


class ActivityAdmin(object):
    list_display = ('maint_time', 'activity_time', 'member_number', 'money', 'comment', 'sub_team', 'activity_type')


# class ActivityTypeAdmin(object):
#     list_display = ('type', 'comment')


class ActivityRatioAdmin(object):
    list_display = ('activity_name', 'ratio', 'comment')


class HrAdmin(object):
    list_display = ('user', 'team')


class AdjustRatioAdmin(object):
    list_display = ('name', 'amount')


site.register(Hr, HrAdmin)
site.register(Team, TeamAdmin)
site.register(SubTeam, SubTeamAdmin)
site.register(Activity, ActivityAdmin)
# site.register(ActivityType, ActivityTypeAdmin)
site.register(ActivityRatio, ActivityRatioAdmin)
site.register(AdjustRatio, AdjustRatioAdmin)
