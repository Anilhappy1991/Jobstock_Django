from django.contrib import admin
from .models import (
    Blog, Candidate, Employer, Job, Profile, DropdownGroup, DropdownMaster,
    CandidateSkill, CandidateEducation, CandidateExperience, CandidateCertification,
    ResumeProcessing, ErrorLog
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


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
	"""
	Admin interface for ErrorLog model.
	Provides comprehensive filtering, searching, and management of error logs.
	"""
	list_display = (
		'id',
		'error_type',
		'get_short_message',
		'function_name',
		'line_number',
		'severity',
		'occurrence_count',
		'is_resolved',
		'last_occurred',
		'user',
	)
	
	list_filter = (
		'severity',
		'is_resolved',
		'error_type',
		'environment',
		'created_at',
		'last_occurred',
	)
	
	search_fields = (
		'error_type',
		'error_message',
		'file_path',
		'function_name',
		'user__username',
		'request_path',
		'error_hash',
	)
	
	readonly_fields = (
		'error_hash',
		'created_at',
		'updated_at',
		'first_occurred',
		'last_occurred',
		'occurrence_count',
	)
	
	list_editable = ('is_resolved',)
	
	date_hierarchy = 'last_occurred'
	
	ordering = ('-last_occurred',)
	
	list_per_page = 50
	
	fieldsets = (
		('Error Information', {
			'fields': (
				'error_type',
				'error_message',
				'error_hash',
				'severity',
				'environment',
			)
		}),
		('Source Location', {
			'fields': (
				'file_path',
				'function_name',
				'line_number',
			)
		}),
		('Full Traceback', {
			'fields': ('error_traceback',),
			'classes': ('collapse',)
		}),
		('Request Context', {
			'fields': (
				'request_method',
				'request_path',
				'request_data',
				'status_code',
			),
			'classes': ('collapse',)
		}),
		('Client Information', {
			'fields': (
				'user',
				'ip_address',
				'user_agent',
			),
			'classes': ('collapse',)
		}),
		('Resolution Tracking', {
			'fields': (
				'is_resolved',
				'resolved_at',
				'resolved_by',
				'resolution_notes',
			)
		}),
		('Occurrence Tracking', {
			'fields': (
				'occurrence_count',
				'first_occurred',
				'last_occurred',
			)
		}),
		('Timestamps', {
			'fields': (
				'created_at',
				'updated_at',
			)
		}),
	)
	
	actions = [
		'mark_as_resolved',
		'mark_as_unresolved',
		'delete_resolved_errors',
		'export_error_report',
	]
	
	def get_short_message(self, obj):
		"""Display shortened error message"""
		if len(obj.error_message) > 80:
			return obj.error_message[:80] + '...'
		return obj.error_message
	get_short_message.short_description = 'Error Message'
	
	def mark_as_resolved(self, request, queryset):
		"""Mark selected errors as resolved"""
		updated = queryset.update(
			is_resolved=True,
			resolved_at=admin.models.timezone.now(),
			resolved_by=request.user
		)
		self.message_user(request, f'{updated} error(s) marked as resolved.')
	mark_as_resolved.short_description = 'Mark selected errors as resolved'
	
	def mark_as_unresolved(self, request, queryset):
		"""Mark selected errors as unresolved"""
		updated = queryset.update(
			is_resolved=False,
			resolved_at=None,
			resolved_by=None
		)
		self.message_user(request, f'{updated} error(s) marked as unresolved.')
	mark_as_unresolved.short_description = 'Mark selected errors as unresolved'
	
	def delete_resolved_errors(self, request, queryset):
		"""Delete errors that are marked as resolved"""
		resolved_errors = queryset.filter(is_resolved=True)
		count = resolved_errors.count()
		resolved_errors.delete()
		self.message_user(request, f'{count} resolved error(s) deleted.')
	delete_resolved_errors.short_description = 'Delete resolved errors'
	
	def export_error_report(self, request, queryset):
		"""Export selected errors as JSON"""
		import json
		from django.http import HttpResponse
		
		errors_data = []
		for error in queryset:
			errors_data.append({
				'id': error.id,
				'error_type': error.error_type,
				'error_message': error.error_message,
				'file_path': error.file_path,
				'function_name': error.function_name,
				'line_number': error.line_number,
				'severity': error.severity,
				'occurrence_count': error.occurrence_count,
				'first_occurred': error.first_occurred.isoformat(),
				'last_occurred': error.last_occurred.isoformat(),
				'is_resolved': error.is_resolved,
			})
		
		response = HttpResponse(
			json.dumps(errors_data, indent=2),
			content_type='application/json'
		)
		response['Content-Disposition'] = 'attachment; filename="error_report.json"'
		return response
	export_error_report.short_description = 'Export error report (JSON)'
