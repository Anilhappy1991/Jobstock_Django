from django.contrib import admin
from .models import (
    Blog, Candidate, Employer, Job, Profile, DropdownGroup, DropdownMaster,
    CandidateSkill, CandidateEducation, CandidateExperience, CandidateCertification,
    ResumeProcessing
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


@admin.register(ResumeProcessing)
class ResumeProcessingAdmin(admin.ModelAdmin):
	list_display = ('user', 'original_filename', 'status', 'file_size', 'word_count', 'created_at', 'processing_completed_at')
	list_filter = ('status', 'created_at')
	search_fields = ('user__username', 'original_filename', 'extracted_email', 'extracted_phone')
	readonly_fields = ('created_at', 'updated_at', 'processing_started_at', 'processing_completed_at')
	fieldsets = (
		('User Information', {
			'fields': ('user', 'profile')
		}),
		('File Information', {
			'fields': ('resume_path', 'original_filename', 'file_size', 'file_extension')
		}),
		('Processing Status', {
			'fields': ('status', 'processing_started_at', 'processing_completed_at', 'error_message')
		}),
		('Extracted Data', {
			'fields': ('resume_text', 'resume_json'),
			'classes': ('collapse',)
		}),
		('Quick Access Fields', {
			'fields': ('extracted_skills', 'extracted_email', 'extracted_phone', 'years_of_experience', 'sentiment_score', 'word_count')
		}),
		('Timestamps', {
			'fields': ('created_at', 'updated_at')
		}),
	)

