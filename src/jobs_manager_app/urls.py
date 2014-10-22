from django.conf.urls import patterns, url

from jobs_manager_app import views

urlpatterns = patterns(
    '',
    url(r'^project/$',
        views.project.index, name='project_index'),
    url(r'^project/(?P<project_id>\d+)/$',
        views.project.detail, name='project_detail'),
    url(r'^project/(?P<project_id>\d+)/update/$',
        views.project.update, name='project_update'),
    url(r'^project/create/$',
        views.project.update, name='project_create'),
    url(r'^project/(?P<project_id>\d+)/delete/$',
        views.project.delete, name='project_delete'),

    url(r'^assignment/$',
        views.assignment.index, name='assignment_index'),
    url(r'^assignment/(?P<assignment_id>\d+)/$',
        views.assignment.detail, name='assignment_detail'),
    url(r'^assignments/(?P<assignment_id>\d+)/update/$',
        views.assignment.update, name='assignment_update'),
    url(r'^assignment/(?P<project_id>\d+)/create/$',
        views.assignment.update, name='assignment_create'),
    url(r'^assignment/(?P<assignment_id>\d+)/delete/$',
        views.assignment.delete, name='assignment_delete'),

    url(r'^task/$', views.task.index, name='task_index'),
    url(r'^task/(?P<task_id>\d+)/$',
        views.task.detail, name='task_detail'),
    url(r'^task/(?P<task_id>\d+)/update/$',
        views.task.update, name='task_update'),
    url(r'^task/(?P<assignment_id>\d+)/create/$',
        views.task.update, name='task_create'),
    url(r'^task/(?P<task_id>\d+)/delete/$',
        views.task.delete, name='task_delete'),
    )
