#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Team(models.Model):
    team_name = models.CharField(u'项目组名称', max_length=30)
    team_leader = models.CharField(u'Team Leader', max_length=30)

    class Meta:
        verbose_name_plural = verbose_name = u'项目组'

    def __unicode__(self):
        return self.team_name


class Hr(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, verbose_name=u'所属项目组')

    class Meta:
        verbose_name_plural = verbose_name = u'用户名'


class SubTeam(models.Model):
    subteam_name = models.CharField(u'小组名称', max_length=30)
    subteam_leader = models.CharField(u'小组领导人', max_length=30)
    team = models.ForeignKey(Team, verbose_name=u'所属项目组', related_name='subTeams')

    class Meta:
        verbose_name_plural = verbose_name = u'小组'

    def __unicode__(self):
        return self.subteam_name

class ActivityRatio(models.Model):
    activity_name = models.CharField(u'活动类别', max_length=30)
    ratio = models.IntegerField(u'费用比例')

    class Meta:
        verbose_name_plural = verbose_name = u'活动费用比例'


    def __unicode__(self):
        return self.activity_name


class Activity(models.Model):
    maint_time = models.DateField(u'维护日期')
    activity_time = models.DateField(u'活动日期')
    member_number = models.IntegerField(u'活动人数')
    money = models.FloatField(u'活动金额')
    comment = models.CharField(u'活动备注', max_length = 50)
    team = models.ForeignKey(Team, verbose_name=u'组别')
    sub_team = models.ForeignKey(SubTeam, verbose_name=u'项目组')
    activity_type = models.ForeignKey(ActivityRatio, verbose_name=u'活动类别')

    class Meta:
        verbose_name_plural = verbose_name = u'活动维护'


class Charge(models.Model):
    charge_date = models.DateField(u'充值时间')
    charge_money = models.FloatField(u'金额')
    team = models.ForeignKey(Team, verbose_name=u'组别')
    formal_number = models.IntegerField(u'正式员工')
    intern_number = models.IntegerField(u'实习生')


# class ActivityType(models.Model):
#     type = models.CharField(u'活动名称', max_length=30)
#     comment = models.CharField(u'备注', max_length=50)

#     class Meta:
#         verbose_name_plural = verbose_name = u'活动类别'


