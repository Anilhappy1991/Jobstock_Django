from django.contrib import admin
from .models import Blog, Candidate, Employer, Job, Profile

admin.site.register(Blog)
admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(Job)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'full_name', 'phone', 'work_status', 'role')
	search_fields = ('user__username', 'full_name', 'phone')
