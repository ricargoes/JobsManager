from django.forms import ModelForm
from jobs_manager_app.models import Project, Assignment, Task, Comment


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'website']


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'dev', 'requirements']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['colaborator', 'name', 'description', 'priority',
                  'bool_completed']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'attachment']
