from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.core import serializers
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from jobs_manager_app.models import Notification


@login_required
def user_notif_list(request):
    notif_list = (Notification.objects.filter(user=request.user)
                  .order_by('-id'))[:8]
    data = serializers.serialize("json", notif_list)
    return HttpResponse(data, content_type="application/json")


@login_required
def toggle_mark_as_read(request):
    notif = get_object_or_404(Notification, pk=request.POST['notif_id'])
    if (notif.user != request.user):
        return HttpResponseForbidden()  # Raises a 403 error

    notif.bool_seen = not notif.bool_seen
    notif.save()
    data = {}
    data['message'] = _('Marked as %sread') % ("" if notif.bool_seen else "un")
    return JsonResponse(data)
