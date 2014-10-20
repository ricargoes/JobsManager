from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from jobs_manager_app.models import Project
from jobs_manager_app.forms import ProjectForm
from django.contrib.auth.decorators import login_required

context = {}
context['tag'] = 'project'


@login_required
def index(request):
    project_list = Project.objects.filter(customer=request.user)
    context['project_list'] = project_list
    return render(request, 'jobs_manager_app/project_list.html', context)


@login_required
def update(request, project_id=None):
    if project_id is None:
        form = ProjectForm()
    else:
        pini = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(instance=pini)

    if request.method == 'POST':
        f = ProjectForm(request.POST)
        p = f.save(commit=False)
        if project_id is not None:
            p.id = project_id
            p.created = pini.created
        p.customer = request.user
        p.save()
        messages.success(request, 'The project has been updated')
        return HttpResponseRedirect(reverse('jobs_manager_app:project_detail',
                                            kwargs={'pk': p.id}))

    context['form'] = form
    return render(request, 'jobs_manager_app/project_update.html', context)

# class IndexView(generic.ListView):
    # model = Project
    # template_name = 'jobs_manager_app/list.html'. Default: app/model_detail
    # context_object_name = 'projects_list'. It uses model_list by default


class DetailView(generic.DetailView):
    model = Project
    # template_name = 'jobs_manager_app/detail.html'. Default: app/model_detail


class DeleteView(generic.edit.DeleteView):
    model = Project
    success_url = reverse_lazy('jobs_manager_app:project_list')
