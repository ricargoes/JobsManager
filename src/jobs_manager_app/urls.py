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

    url(r'^assignment/(?P<assignment_id>\d+)/estimate/$',
        views.assignment.estimate, name='assignment_estimate'),
    url(r'^assignment/(?P<assignment_id>\d+)/confirm/$',
        views.assignment.confirm_estimate, name='assignment_confirm_estimate'),
    url(r'^assignment/(?P<assignment_id>\d+)/state_forward/$',
        views.assignment.state_forward, name='assignment_state_forward'),
    url(r'^assignment/(?P<assignment_id>\d+)/toggle_hold/$',
        views.assignment.toggle_hold, name='assignment_toggle_hold'),
    url(r'^assignment/(?P<assignment_id>\d+)/hold_payment/$',
        views.assignment.hold_payment, name='assignment_hold_payment'),

    url(r'^task/$', views.task.index, name='task_index'),
    url(r'^task/(?P<task_id>\d+)/$',
        views.task.detail, name='task_detail'),
    url(r'^task/(?P<task_id>\d+)/update/$',
        views.task.update, name='task_update'),
    url(r'^task/(?P<assignment_id>\d+)/create/$',
        views.task.update, name='task_create'),
    url(r'^task/(?P<task_id>\d+)/delete/$',
        views.task.delete, name='task_delete'),

    url(r'^user/$', views.user.index, name='user_index'),
    url(r'^user/(?P<user_id>\d+)/$',
        views.user.detail, name='user_detail'),

    url(r'^comment/(?P<assignment_id>\d+)/create_from_assignment/$',
        views.comment.create_from_assignment, name='comment_from_assignment'),
    url(r'^comment/(?P<task_id>\d+)/create_from_task/$',
        views.comment.create_from_task, name='comment_from_task'),

    url(r'^notification/user_list/$',
        views.notification.user_notif_list, name='notif_user_list'),
    url(r'^notification/(?P<notif_id>\d+)/toggle_seen/$',
        views.notification.toggle_mark_as_read, name='notif_toggle_seen'),

    )
