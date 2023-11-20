from django.contrib import admin
from .models import *
# Register your models here.


class taks_admin(admin.ModelAdmin):
    list_display = ['user','task','completed','created_at']

admin.site.register(tasks_model, taks_admin)