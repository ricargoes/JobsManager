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
    STATE = (
        (0, 'Pending estimate'),
        (1, 'Estimate proposed'),
        (2, 'Estimate rejected'),
        (3, 'Assignment accepted'),
        (4, 'Assignment completed'),
        (5, 'Assignment paid'),
        (6, 'Assignment closed')
        )
    int_state = models.IntegerField(default=0, choices=STATE)
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
    bool_completed = models.BooleanField(default=False, blank=True)
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
