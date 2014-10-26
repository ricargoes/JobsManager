from django.db import models
from django.contrib.auth.models import User


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
        0: {'state': 'Assignment created', 'next': 'Price/ETA proposal',
            'desc': ''},
        1: {'state': 'Offer proposed', 'next': 'Confirmation',
            'desc': ''},
        -1: {'state': 'Assignment rejected', 'next': 'Price/ETA reevaluation',
             'desc': ''},
        2: {'state': 'Assignment confirmed', 'next': 'Working',
            'desc': ''},
        -2: {'state': 'Assignment in hold', 'next': 'Meeting conditions',
             'desc': ''},
        3: {'state': 'Assignment completed', 'next': 'Payment',
            'desc': ''},
        -3: {'state': 'Payment in hold', 'next': 'Payment',
             'desc': ''},
        4: {'state': 'Assignment paid', 'next': 'Closure',
            'desc': ''},
        5: {'state': 'Assignment closed', 'next': 'Closed',
            'desc': ''},
    }
    STATE2 = (
        (0, {'state': 'Assignment created', 'next': 'Price/ETA proposal',
             'desc': ''}),
        (1, {'state': 'Offer proposed', 'next': 'Confirmation',
             'desc': ''}),
        (-1, {'state': 'Assignment rejected', 'next': 'Price/ETA reevaluation',
              'desc': ''}),
        (2, {'state': 'Assignment confirmed', 'next': 'Working',
             'desc': ''}),
        (-2, {'state': 'Assignment in hold', 'next': 'Meeting conditions',
              'desc': ''}),
        (3, {'state': 'Assignment completed', 'next': 'Payment',
             'desc': ''}),
        (-3, {'state': 'Payment in hold', 'next': 'Payment',
              'desc': ''}),
        (4, {'state': 'Assignment paid', 'next': 'Closure',
             'desc': ''}),
        (5, {'state': 'Assignment closed', 'next': 'Closed',
             'desc': ''}),
    )

    int_state = models.IntegerField(default=0, choices=STATE2)
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
        (False, 'Pending'),
        (True, 'Completed')
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
