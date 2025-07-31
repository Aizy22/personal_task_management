from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'due_time', 'reminder_time', 'context_tag']
        widgets = {
            'status': forms.Select(attrs={'class':'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            
        }