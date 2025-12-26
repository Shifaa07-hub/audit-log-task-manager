from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.CharField (max_length = 100)
    completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.task
    
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('added', 'Added'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('completed', 'completed'),
        ('incompleted', 'Incompleted'),
    ]

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete = models.SET_NULL, null = True, blank = True)
    task_name = models.CharField(max_length = 100)
    action = models.CharField(max_length = 20, choices = ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user} {self.action} {self.task}"