from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from jobs_manager_app.models import Project, Assignment
from jobs_manager_app.forms import (AssignmentForm, CommentForm,
                                    EstimationForm, DealForm)
from datetime import date


context = {}
context['tag'] = 'assignment'


@login_required
def index(request):
    assignment_list = Assignment.objects.filter(
        Q(dev=request.user) | Q(project__customer=request.user)
    )
    context['assignment_list'] = assignment_list
    context['state'] = Assignment.STATE
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
        if (p.customer != request.user):
            return HttpResponseForbidden()  # Raises a 403 error

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
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
    context['comment_form'] = CommentForm()
    context['estimation_form'] = EstimationForm()
    context['deal_form'] = DealForm()
    return render(request, 'jobs_manager_app/assignment_detail.html', context)


@login_required
def delete(request, assignment_id):
    if request.method != 'POST':
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:assignment_index')
        )

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if assignment.project.customer != request.user:
        return HttpResponseForbidden()  # Raises a 403 error

    assignment.delete()
    messages.success(request, 'Assignment deleted')
    return HttpResponseRedirect(
        reverse_lazy('jobs_manager_app:assignment_index')
    )


@login_required
def estimate(request, assignment_id):
    # Check models.Assignment for the description of the states
    if request.method != 'POST':
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:assignment_index')
        )

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if not (assignment.dev == request.user
            and assignment.int_state in [-1, 0]):
        return HttpResponseForbidden()  # Raises a 403 error

    form = EstimationForm(request.POST, instance=assignment)
    if form.is_valid():
        a = form.save(commit=False)
        a.int_state = 1
        a.save()
        messages.success(request, 'Estimation proposed.')
        return HttpResponseRedirect(
            reverse('jobs_manager_app:assignment_index')
        )


@login_required
def confirm_estimate(request, assignment_id):
    # decision == 0 means estimation rejected, else means confirmed
    # Check models.Assignment for the description of the states
    if request.method != 'POST':
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:assignment_index')
        )
    decision = request.POST['decision']

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if not (assignment.project.customer == request.user
            and assignment.int_state == 1):
        return HttpResponseForbidden()  # Raises a 403 error

    form = DealForm(request.POST, instance=assignment)
    if form.is_valid():
        a = form.save(commit=False)
        if decision == "rejected":  # reject offer
            a.int_state = -1
            messages.error(request, 'Offer rejected.')
        elif decision == "confirmed":  # confirm offer
            a.int_state = 2
            messages.success(request, 'Offer confirmed')

        a.save()
        return HttpResponseRedirect(
            reverse('jobs_manager_app:assignment_index')
        )


@login_required
def state_forward(request, assignment_id):
    # Check models.Assignment for the description of the states
    if request.method != 'POST':
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:assignment_index')
        )

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if not ((assignment.dev == request.user
            and assignment.int_state in [2, 4]) or
            (assignment.project.customer == request.user
            and assignment.int_state == 3)):
        return HttpResponseForbidden()  # Raises a 403 error

    if assignment.int_state == 2:
        assignment.delivery_date = date.today()
        text = 'Assignment submitted'
    elif assignment.int_state == 3:
        assignment.payment_date = date.today()
        text = 'Assignment paid'
    elif assignment.int_state == 4:
        assignment.close_date = date .today()
        text = 'Assignment closed'

    assignment.int_state = assignment.int_state + 1
    assignment.save()
    messages.success(request, text)
    return HttpResponseRedirect(
        reverse('jobs_manager_app:assignment_index')
    )


@login_required
def toggle_hold(request, assignment_id):
    # Check models.Assignment for the description of the states
    if request.method != 'POST':
        messages.error(request, 'POST method expected')
        return HttpResponseRedirect(
            reverse_lazy('jobs_manager_app:assignment_index')
        )

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if not (assignment.dev == request.user
            and assignment.int_state in [-2, 2]):
        return HttpResponseForbidden()  # Raises a 403 error

    assignment.int_state = -1*assignment.int_state
    assignment.save()
    if assignment.int_state == 2:
        text = 'Assignment in progress'
    elif assignment.int_state == -2:
        text = 'Assignment in hold'
    messages.success(request, text)
    return HttpResponseRedirect(
        reverse('jobs_manager_app:assignment_index')
    )
