from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

context = {}
context['tag'] = 'user'


@login_required
def index(request):
    user_list = User.objects.all()
    context['user_list'] = user_list
    return render(request, 'jobs_manager_app/user_list.html', context)


@login_required
def detail(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)
    context['user'] = user
    return render(request, 'jobs_manager_app/user_detail.html', context)
