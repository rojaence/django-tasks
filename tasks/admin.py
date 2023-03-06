from django.contrib import admin
from .models import Tasks


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", )


# Register your models here.
admin.site.register(Tasks, TaskAdmin)
