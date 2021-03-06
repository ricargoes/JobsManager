from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import ugettext as _
from jobs_manager_app.models import Assignment, Task
from jobs_manager_app.forms import TaskForm, CommentForm
from jobs_manager_app import tools


context = {}
context['tag'] = 'task'


@login_required
def index(request):
    task_list = Task.objects.filter(
        Q(colaborator=request.user) | Q(assignment__dev=request.user)
    )

    task_paginator = Paginator(task_list, 2)

    page = request.GET.get('page')
    try:
        task_list_p = task_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        task_list_p = task_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        task_list_p = task_paginator.page(task_paginator.num_pages)

    context['task_list'] = task_list_p
    return render(request, 'jobs_manager_app/task_list.html', context)


@login_required
def update(request, assignment_id=None, task_id=None):
    # We load the instance we are going to change.
    if task_id:
        task = get_object_or_404(Task, pk=task_id)
        if (task.assignment.dev != request.user
                or task.bool_completed is True):
            return HttpResponseForbidden()  # Raises a 403 error
    elif assignment_id:
        a = get_object_or_404(Assignment, pk=assignment_id)
        if a.dev != request.user:
            return HttpResponseForbidden()  # Raises a 403 error
        task = Task(assignment=a)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            t = form.save(commit=False)
            t.save()

            if task.colaborator:
                notif = tools.notif_new_task(t)
                notif.save()

            messages.success(request, _('The task has been updated'))
            return HttpResponseRedirect(
                reverse('jobs_manager_app:task_index')
            )
    else:
        form = TaskForm(instance=task)

    context['form'] = form
    context['assignment_id'] = assignment_id
    context['task_id'] = task_id
    return render(request, 'jobs_manager_app/task_update.html', context)


@login_required
def detail(request, task_id=None):
    task = get_object_or_404(Task, pk=task_id)
    context['task'] = task
    context['comment_form'] = CommentForm()
    return render(request, 'jobs_manager_app/task_detail.html', context)


@login_required
def delete(request, task_id):
    if request.method != 'POST':
        messages.error(request, _('POST method expected'))
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:task_index')
        )

    task = get_object_or_404(Task, pk=task_id)
    if (task.assignment.dev != request.user or task.bool_completed is True):
        return HttpResponseForbidden()  # Raises a 403 error

    task.delete()
    messages.success(request, _('Task deleted'))
    return HttpResponseRedirect(reverse_lazy('jobs_manager_app:task_index'))


@login_required
def close_task(request, task_id):
    if request.method != 'POST':
        messages.error(request, _('POST method expected'))
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:task_detail',
                         kwargs={'task_id': task_id})
        )

    task = get_object_or_404(Task, pk=task_id)
    if (task.assignment.dev != request.user or task.bool_completed is True):
        return HttpResponseForbidden()  # Raises a 403 error

    task.bool_completed = True
    task.save()

    if task.colaborator:  # Notification
        if (task.colaborator == request.user):
            recipient = task.assignment.dev
        else:
            recipient = task.colaborator
        notif = tools.notif_closed_task(task, recipient)
        notif.save()

    messages.success(request, _('Task closed'))
    return HttpResponseRedirect(reverse_lazy('jobs_manager_app:task_detail',
                                             kwargs={'task_id': task_id}))
