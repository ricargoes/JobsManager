from django.contrib import admin
from jobs_manager_app.models import (Project, Assignment, Task, Comment,
                                     Notification)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'website', 'customer']}),
    ]
    inlines = [AssignmentInline]


class AssignmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'requirements', 'price', 'eta', 'project',
                           'dev']}),
        ('State', {'fields': ['int_state', 'deal_comment', 'delivery_date',
                              'payment_date', 'close_date'],
                   'classes': ['collapse']}),
    ]
    inlines = [TaskInline, CommentInline]


class TaskAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)
admin.site.register(Notification)
