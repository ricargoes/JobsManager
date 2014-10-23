from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from jobs_manager_project import settings
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'jobs_manager_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^jobs_manager_app/',
        include('jobs_manager_app.urls', namespace="jobs_manager_app")),
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'jobs_manager_app/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,
        {'next_page': '/'}, name='logout'),
    url(r'^logout/(?P<next_page>.*)/$',
        'django.contrib.auth.views.logout', name='logout_next'),) + (static(
            settings.STATIC_URL,
            document_root=settings.STATIC_ROOT
            ))
