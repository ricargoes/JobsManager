from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from jobs_manager_app.models import Assignment, Task
from jobs_manager_app.forms import CommentForm
from jobs_manager_app import tools


@login_required
def create_from_assignment(request, assignment_id):

    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.assignment = assignment
            comment.user = request.user
            comment.save()

            if (assignment.dev == comment.user):
                recipient = assignment.project.dev
            elif (assignment.projet.dev == comment.user):
                recipient = assignment.dev
            notif = tools.notif_comment_assign(comment, recipient)
            notif.save()

            return HttpResponseRedirect(
                reverse('jobs_manager_app:assignment_detail',
                        kwargs={'assignment_id': assignment.id})
            )
        else:
            messages.error(_('Form not valid'))

    else:
        messages.error(request, _('POST method expected'))
        return HttpResponseRedirect(
            reverse('jobs_manager_app:assignment_detail',
                    kwargs={'assignment_id': assignment.id})
        )


@login_required
def create_from_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id)

    if request.method != 'POST':
        messages.error(request, _('POST method expected'))
        return HttpResponseRedirect(
            reverse('jobs_manager_app:task_detail',
                    kwargs={'task_id': task.id})
        )

    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.user = request.user
        comment.save()

        if task.colaborator:
            if (task.colaborator == comment.user):
                recipient = task.assignment.dev
            else:
                recipient = task.colaborator
            notif = tools.notif_comment_task(comment, recipient)
            notif.save()

        return HttpResponseRedirect(
            reverse('jobs_manager_app:task_detail',
                    kwargs={'task_id': task.id})
        )
    else:
        messages.error(_('Form not valid'))
