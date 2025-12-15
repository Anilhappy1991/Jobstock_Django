"""
Custom template filters for the App
"""
from django import template
import os

register = template.Library()


@register.filter(name='filename')
def get_filename(filepath):
    """
    Extract just the filename from a file path.
    Usage: {{ file.name|filename }}
    """
    if not filepath:
        return ''
    return os.path.basename(str(filepath))


@register.filter(name='filesize')
def format_filesize(size_bytes):
    """
    Format file size in bytes to human-readable format.
    Usage: {{ file.size|filesize }}
    """
    if not size_bytes:
        return '0 B'
    
    try:
        size_bytes = int(size_bytes)
    except (ValueError, TypeError):
        return '0 B'
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


@register.filter(name='file_extension')
def get_file_extension(filepath):
    """
    Get the file extension from a file path.
    Usage: {{ file.name|file_extension }}
    """
    if not filepath:
        return ''
    return os.path.splitext(str(filepath))[1].upper().replace('.', '')
