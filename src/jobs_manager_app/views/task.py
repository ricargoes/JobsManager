from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from jobs_manager_app.models import Task
from jobs_manager_app.forms import TaskForm
from django.contrib.auth.decorators import login_required

context = {}
context['tag'] = 'task'


@login_required
def index(request):
    task_list = Task.objects.all()
    context['task_list'] = task_list
    return render(request, 'jobs_manager_app/task_list.html', context)


@login_required
def update(request, task_id=None):
    if task_id is None:
        form = TaskForm()
    else:
        pini = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=pini)

    if request.method == 'POST':
        f = TaskForm(request.POST)
        p = f.save(commit=False)
        if task_id is not None:
            p.id = task_id
            p.created = pini.created
        p.customer = request.user
        p.save()
        messages.success(request, 'The task has been updated')
        return HttpResponseRedirect(reverse('jobs_manager_app:task_detail',
                                            kwargs={'pk': p.id}))

    context['form'] = form
    return render(request, 'jobs_manager_app/task_update.html', context)

# class IndexView(generic.ListView):
    # model = Task
    # template_name = 'jobs_manager_app/list.html'. Default: app/model_detail
    # context_object_name = 'tasks_list'. It uses model_list by default


class DetailView(generic.DetailView):
    model = Task
    # template_name = 'jobs_manager_app/detail.html'. Default: app/model_detail


class DeleteView(generic.edit.DeleteView):
    model = Task
    success_url = reverse_lazy('jobs_manager_app:task_list')
