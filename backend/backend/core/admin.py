from django.contrib import admin
from .models import ScheduleRequest


admin.site.site_header = "Schedule Generator Admin"
admin.site.site_title = "Schedule Generator Admin Portal"
admin.site.index_title = "Welcome to the Schedule Generator Admin Portal"

admin.site.register(ScheduleRequest)
