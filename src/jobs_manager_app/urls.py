from django.conf.urls import patterns, url

from jobs_manager_app import views

urlpatterns = patterns(
    '',
    url(r'^project/$',
        'jobs_manager_app.views.project.index', name='project_index'),
    url(r'^project/(?P<pk>\d+)/$',
        views.project.DetailView.as_view(), name='project_detail'),
    url(r'^project/(?P<project_id>\d+)/update/$',
        'jobs_manager_app.views.project.update', name='project_update'),
    url(r'^project/update/$',
        'jobs_manager_app.views.project.update', name='project_update'),
    url(r'^project/(?P<pk>\d+)/delete/$',
        views.project.DeleteView.as_view(), name='project_delete'),

    url(r'^assignment/$',
        'jobs_manager_app.views.assignment.index', name='assignment_index'),
    url(r'^assignment/(?P<pk>\d+)/$',
        views.assignment.DetailView.as_view(), name='assignment_detail'),
    url(r'^assignments/(?P<project_id>\d+)/update/$',
        'jobs_manager_app.views.assignment.update', name='assignment_update'),
    url(r'^assignment/update/$',
        'jobs_manager_app.views.assignment.update', name='assignment_update'),
    url(r'^assignment/(?P<pk>\d+)/delete/$',
        views.assignment.DeleteView.as_view(), name='assignment_delete'),

    url(r'^task/$', 'jobs_manager_app.views.task.index', name='task_index'),
    url(r'^task/(?P<pk>\d+)/$',
        views.task.DetailView.as_view(), name='task_detail'),
    url(r'^task/(?P<project_id>\d+)/update/$',
        'jobs_manager_app.views.task.update', name='task_update'),
    url(r'^task/update/$',
        'jobs_manager_app.views.task.update', name='task_update'),
    url(r'^task/(?P<pk>\d+)/delete/$',
        views.task.DeleteView.as_view(), name='task_delete'),
    )