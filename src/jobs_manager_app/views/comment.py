from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from jobs_manager_app.models import Assignment, Task
from jobs_manager_app.forms import CommentForm
from django.contrib.auth.decorators import login_required


@login_required
def create_from_assignment(request, assignment_id):

    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.assignment = assignment
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(
                reverse('jobs_manager_app:assignment_detail',
                        kwargs={'assignment_id': assignment.id})
                )

    else:
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse('jobs_manager_app:assignment_detail',
                    kwargs={'assignment_id': assignment.id})
            )


@login_required
def create_from_task(request, task_id):

    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(
                reverse('jobs_manager_app:task_detail',
                        kwargs={'task_id': task.id})
                )
        else:
            messages.error('form not valid')

    else:
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse('jobs_manager_app:task_detail',
                    kwargs={'task_id': task.id})
            )
