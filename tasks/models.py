from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    CONTEXT_CHOICES = [
    ('morning', 'After Breakfast'),
    ('commute', 'During Commute'),
    ('evening', 'Before Bed'),
    ]

    context_tag = models.CharField(max_length=50, choices=CONTEXT_CHOICES, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    reminder_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_overdue(self):
        if self.due_date:
            task_datetime = datetime.combine(self.due_date, self.due_time or datetime.min.time())
            return task_datetime < datetime.now() and self.status != 'completed'
        return False
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"