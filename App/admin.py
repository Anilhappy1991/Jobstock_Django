from django.contrib import admin
from .models import Blog, Candidate, Employer, Job, Profile

admin.site.register(Blog)
admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(Profile)
