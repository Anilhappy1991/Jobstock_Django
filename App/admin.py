from django.contrib import admin
from .models import Blog, Candidate, Employer, Job, Profile, DropdownGroup, DropdownMaster

admin.site.register(Blog)
admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(Job)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'full_name', 'phone', 'work_status', 'role')
	search_fields = ('user__username', 'full_name', 'phone')


@admin.register(DropdownGroup)
class DropdownGroupAdmin(admin.ModelAdmin):
	list_display = ('id', 'text', 'value', 'is_active', 'created_at')
	list_filter = ('is_active',)
	search_fields = ('text', 'value')


@admin.register(DropdownMaster)
class DropdownMasterAdmin(admin.ModelAdmin):
	list_display = ('id', 'group', 'text', 'value', 'sort_order', 'is_active', 'created_at')
	list_filter = ('group', 'is_active')
	search_fields = ('text', 'value')
	list_editable = ('sort_order', 'is_active')

