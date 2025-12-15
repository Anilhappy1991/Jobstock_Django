from django.contrib import admin
from .models import (
    Blog, Candidate, Employer, Job, Profile, DropdownGroup, DropdownMaster,
    CandidateSkill, CandidateEducation, CandidateExperience, CandidateCertification
)

admin.site.register(Blog)
admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(Job)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'full_name', 'phone', 'work_status', 'role', 'profile_completion', 'updated_at')
	list_filter = ('work_status', 'role', 'is_active')
	search_fields = ('user__username', 'full_name', 'phone', 'email')
	readonly_fields = ('profile_completion', 'created_at', 'updated_at')


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


@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
	list_display = ('profile', 'skill_name', 'proficiency', 'created_at')
	list_filter = ('proficiency',)
	search_fields = ('profile__user__username', 'skill_name')


@admin.register(CandidateEducation)
class CandidateEducationAdmin(admin.ModelAdmin):
	list_display = ('profile', 'degree', 'institution', 'start_date', 'end_date', 'is_current')
	list_filter = ('is_current',)
	search_fields = ('profile__user__username', 'degree', 'institution')


@admin.register(CandidateExperience)
class CandidateExperienceAdmin(admin.ModelAdmin):
	list_display = ('profile', 'job_title', 'company_name', 'start_date', 'end_date', 'is_current')
	list_filter = ('is_current',)
	search_fields = ('profile__user__username', 'job_title', 'company_name')


@admin.register(CandidateCertification)
class CandidateCertificationAdmin(admin.ModelAdmin):
	list_display = ('profile', 'certification_name', 'issuing_organization', 'issue_date', 'expiry_date')
	search_fields = ('profile__user__username', 'certification_name', 'issuing_organization')

