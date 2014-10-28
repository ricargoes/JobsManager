from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Project(models.Model):
    customer = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        # When Django displays some object of this class,
        # it will show the returned value.
        return self.name


class Assignment(models.Model):
    dev = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    requirements = models.TextField()
    STATE = {
        0: {'state': _('Assignment created'), 'next': _('Price/ETA proposal'),
            'desc': ''},
        1: {'state': _('Offer proposed'), 'next': _('Confirmation'),
            'desc': ''},
        -1: {'state': _('Assignment rejected'),
             'next': _('Price/ETA reevaluation'), 'desc': ''},
        2: {'state': _('Assignment confirmed'), 'next': _('Working'),
            'desc': ''},
        -2: {'state': _('Assignment in hold'), 'next': _('Meeting conditions'),
             'desc': ''},
        3: {'state': _('Assignment completed'), 'next': _('Payment'),
            'desc': ''},
        -3: {'state': _('Payment in hold'), 'next': _('Payment'),
             'desc': ''},
        4: {'state': _('Assignment paid'), 'next': _('Closure'),
            'desc': ''},
        5: {'state': _('Assignment closed'), 'next': _('Closed'),
            'desc': ''},
    }

    int_state = models.IntegerField(default=0)
    deal_comment = models.TextField(blank=True)
    price = models.FloatField(blank=True, null=True)
    eta = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class Task(models.Model):
    assignment = models.ForeignKey(Assignment)
    colaborator = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=1)
    STATE = (
        (False, _('Pending')),
        (True, _('Completed'))
        )
    bool_completed = models.BooleanField(default=False, blank=True,
                                         choices=STATE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class Comment(models.Model):
    assignment = models.ForeignKey(Assignment, blank=True, null=True)
    task = models.ForeignKey(Task, blank=True, null=True)
    user = models.ForeignKey(User)
    comment = models.TextField()
    attachment = models.FileField(upload_to='documents/%Y/%m/%d', blank=True,
                                  null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.comment[0:20]


class Notification(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    description = models.TextField()
    NOTIF_TYPE = (
        (0, _('New task')),
        (1, _('New assignment')),
        (2, _('Negotiation process')),
        (3, _('Task closed')),
        (4, _('Comment in assignment')),
        (5, _('Comment in task')),
        (6, _('Comment in assignment')),
        )
    int_type = models.IntegerField(default=False, choices=NOTIF_TYPE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name