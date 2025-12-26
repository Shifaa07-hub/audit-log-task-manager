from django.contrib import admin
from .models import Task, AuditLog

# Register your models here.
admin.site.register(Task)
admin.site.register(AuditLog)