from django import forms
from jobs_manager_app.models import Project, Assignment, Task, Comment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'website']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'dev', 'requirements']


class EstimationForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['price', 'eta']


class DealForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['deal_comment']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['colaborator', 'name', 'description', 'priority']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'attachment']
