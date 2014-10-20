from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from jobs_manager_app.models import Assignment
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
def update(request, assignment_id=None):
    if assignment_id is None:
        form = AssignmentForm()
    else:
        pini = get_object_or_404(Assignment, pk=assignment_id)
        form = AssignmentForm(instance=pini)

    if request.method == 'POST':
        f = AssignmentForm(request.POST)
        p = f.save(commit=False)
        if assignment_id is not None:
            p.id = assignment_id
            p.created = pini.created
        p.save()
        messages.success(request, 'The assignment has been updated')
        return HttpResponseRedirect(reverse('jobs_manager_app:assignment_detail',
                                            kwargs={'pk': p.id}))

    context['form'] = form
    return render(request, 'jobs_manager_app/assignment_update.html', context)

# class IndexView(generic.ListView):
    # model = Assignment
    # template_name = 'jobs_manager_app/list.html'. Default: app/model_detail
    # context_object_name = 'assignments_list'. It uses model_list by default


class DetailView(generic.DetailView):
    model = Assignment
    # template_name = 'jobs_manager_app/detail.html'. Default: app/model_detail


class DeleteView(generic.edit.DeleteView):
    model = Assignment
    success_url = reverse_lazy('jobs_manager_app:assignment_list')
