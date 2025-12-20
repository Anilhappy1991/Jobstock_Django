"""
Custom template filters for job forms
"""
from django import template

register = template.Library()

@register.filter
def is_selected(dropdown_item, job_field):
    """
    Check if a dropdown item should be selected based on job field
    Usage: {% if item|is_selected:job.job_category %}selected{% endif %}
    """
    if not job_field:
        return False
    
    # Handle ForeignKey fields
    if hasattr(job_field, 'value'):
        return dropdown_item.value == job_field.value
    
    # Handle direct value comparison
    return dropdown_item.value == job_field
