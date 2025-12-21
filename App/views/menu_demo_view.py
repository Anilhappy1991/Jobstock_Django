"""
Menu Demo View
Demonstrates hierarchical multilevel menu
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def menu_demo(request):
    """
    Display hierarchical menu demo page
    Navigation context is automatically added by context processor
    """
    return render(request, 'Pages/menu_demo.html')
