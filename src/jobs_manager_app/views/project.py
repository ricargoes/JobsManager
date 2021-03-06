from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jobs_manager_app.models import Project
from jobs_manager_app.forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

context = {}
context['tag'] = 'project'


@login_required
def index(request):
    project_list = Project.objects.filter(customer=request.user)
    project_paginator = Paginator(project_list, 2)

    page = request.GET.get('page')
    try:
        project_list_p = project_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        project_list_p = project_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        project_list_p = project_paginator.page(project_paginator.num_pages)

    context['project_list'] = project_list_p
    return render(request, 'jobs_manager_app/project_list.html', context)


@login_required
def update(request, project_id=None):
    # We load the instance we are going to change.
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        if project.customer != request.user:
            return HttpResponseForbidden()  # Raises a 403 error
    else:
        project = Project()

    # We save the data coming from the POST petition.
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            p = form.save(commit=False)
            p.customer = request.user
            p.save()
            messages.success(request, _('The project has been updated'))
            return HttpResponseRedirect(
                reverse('jobs_manager_app:project_index')
            )
    else:
        form = ProjectForm(instance=project)

    # We prepare the form we are going to draw in the template and we render.
    context['form'] = form
    context['project_id'] = project_id
    return render(request, 'jobs_manager_app/project_update.html', context)


@login_required
def detail(request, project_id=None):
    project = get_object_or_404(Project, pk=project_id)
    context['project'] = project
    return render(request, 'jobs_manager_app/project_detail.html', context)


@login_required
def delete(request, project_id):
    if request.method != 'POST':
        messages.error(request, _('POST method expected'))
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:project_index')
        )

    project = get_object_or_404(Project, pk=project_id)
    if project.customer != request.user:
        return HttpResponseForbidden()  # Raises a 403 error

    project.delete()
    messages.success(request, _('Project deleted'))
    return HttpResponseRedirect(
        reverse_lazy('jobs_manager_app:project_index')
    )
