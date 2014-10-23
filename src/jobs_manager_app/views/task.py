from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from jobs_manager_app.models import Assignment, Task
from jobs_manager_app.forms import TaskForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

context = {}
context['tag'] = 'task'


@login_required
def index(request):
    task_list = Task.objects.filter(
        Q(colaborator=request.user) | Q(assignment__dev=request.user)
    )
    context['task_list'] = task_list
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
            messages.success(request, 'The task has been updated')
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
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:task_index')
        )

    task = get_object_or_404(Task, pk=task_id)
    if (task.assignment.dev != request.user or task.bool_completed is True):
        return HttpResponseForbidden()  # Raises a 403 error

    task.delete()
    messages.success(request, 'Task deleted')
    return HttpResponseRedirect(reverse_lazy('jobs_manager_app:task_index'))
