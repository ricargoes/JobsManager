from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from jobs_manager_app.models import Project, Assignment
from jobs_manager_app.forms import AssignmentForm
from django.contrib.auth.decorators import login_required

context = {}
context['tag'] = 'assignment'


@login_required
def index(request):
    assignment_list = Assignment.objects.filter(dev=request.user)
    context['assignment_list'] = assignment_list
    return render(request, 'jobs_manager_app/assignment_list.html', context)


@login_required
def update(request, project_id=None, assignment_id=None):
    # We load the instance we are going to change.
    if assignment_id:
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        if (assignment.project.customer != request.user
                or assignment.int_state > 0):
            return HttpResponseForbidden()  # Raises a 403 error
    elif project_id:
        p = get_object_or_404(Project, pk=project_id)
        assignment = Assignment(project=p)
        context['assignment_id'] = None

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        a = form.save(commit=False)
        a.save()
        messages.success(request, 'The assignment has been updated')
        return HttpResponseRedirect(
            reverse('jobs_manager_app:assignment_index')
            )
    else:
        form = AssignmentForm(instance=assignment)

    context['form'] = form
    context['project_id'] = project_id
    context['assignment_id'] = assignment_id
    return render(request, 'jobs_manager_app/assignment_update.html', context)


@login_required
def detail(request, assignment_id=None):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    context['assignment'] = assignment
    return render(request, 'jobs_manager_app/assignment_detail.html', context)


class DeleteView(generic.edit.DeleteView):
    model = Assignment
    success_url = reverse_lazy('jobs_manager_app:assignment_list')
