from django.contrib import admin
from .models import Profile, JobPosting, Application

admin.site.register(Profile)
admin.site.register(JobPosting)
admin.site.register(Application)