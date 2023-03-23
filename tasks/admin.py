from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", )


# Register your models here.
admin.site.site_header = "DjangoTasks administration"
admin.site.register(Task, TaskAdmin)
