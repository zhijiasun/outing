#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

MONTH_CHOICE = (
        (1,u'一月'),(2,u'二月'),(3,u'三月'),(4,u'四月'),    
        (5,u'五月'),(6,u'六月'),(7,u'七月'),(8,u'八月'),   
        (9,u'九月'),(9,u'九月'),(10,u'十月'),(11,u'十一月'),(12,u'十二月')    
    )

EMPLOYEE_TYPE = (
    (1, u'正式员工'),
    (2, u'实习生')
    )

class Team(models.Model):
    team_name = models.CharField(u'组别名称', max_length=30)
    team_leader = models.CharField(u'Team Leader', max_length=30)

    class Meta:
        verbose_name_plural = verbose_name = u'组别'

    def __unicode__(self):
        return self.team_name


class Hr(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, verbose_name=u'所属组别')

    class Meta:
        verbose_name_plural = verbose_name = u'财务'


class SubTeam(models.Model):
    subteam_name = models.CharField(u'项目组名称', max_length=30)
    subteam_leader = models.CharField(u'项目组领导人', max_length=30)
    team = models.ForeignKey(Team, verbose_name=u'所属组别', related_name='subTeams')

    class Meta:
        verbose_name_plural = verbose_name = u'项目组'

    def __unicode__(self):
        return self.subteam_name

class ActivityRatio(models.Model):
    activity_name = models.CharField(u'活动类别', max_length=30)
    ratio = models.IntegerField(u'费用比例')
    comment = models.CharField(u'活动说明', max_length=80)

    class Meta:
        verbose_name_plural = verbose_name = u'活动费用比例'


    def __unicode__(self):
        return self.activity_name


class Activity(models.Model):
    maint_time = models.DateField(u'维护日期')
    activity_time = models.DateField(u'活动日期')
    member_number = models.IntegerField(u'活动人数')
    money = models.FloatField(u'活动金额')
    comment = models.CharField(u'活动备注', max_length=50, blank=True, null=True)
    team = models.ForeignKey(Team, verbose_name=u'组别')
    sub_team = models.ForeignKey(SubTeam, verbose_name=u'项目组')
    activity_type = models.ForeignKey(ActivityRatio, verbose_name=u'活动类别')

    class Meta:
        verbose_name_plural = verbose_name = u'活动维护'


class ChargeRecord(models.Model):
    charge_date = models.DateField(u'充值时间', auto_now=True)
    charge_money = models.FloatField(u'金额')
    team = models.ForeignKey(Team, verbose_name=u'组别')
    activity = models.ForeignKey(ActivityRatio, verbose_name=u'活动')
    comment = models.CharField(u'备注', max_length=80)


class Charge(models.Model):
    charge_date = models.DateField(u'充值时间', auto_now=True)
    month = models.IntegerField(choices=MONTH_CHOICE)
    charge_money = models.FloatField(u'金额')
    team = models.ForeignKey(Team, verbose_name=u'组别')
    formal_number = models.IntegerField(u'正式员工')
    intern_number = models.IntegerField(u'实习生')

    def save(self, *args, **kwargs):
        for activity in ActivityRatio.objects.all():
            record = ChargeRecord(charge_money=activity.ratio*0.01*self.charge_money, team=self.team, activity=activity)
            record.save()
        super(Charge, self).save(*args, **kwargs)


class AdjustRatio(models.Model):
    name = models.IntegerField(u'员工类型', choices=EMPLOYEE_TYPE)
    amount = models.IntegerField(u'费用金额')

    class Meta:
        verbose_name = verbose_name_plural = u'调整经费比例'

    def __unicode__(self):
        return self.name


# class ActivityType(models.Model):
#     type = models.CharField(u'活动名称', max_length=30)
#     comment = models.CharField(u'备注', max_length=50)

#     class Meta:
#         verbose_name_plural = verbose_name = u'活动类别'


