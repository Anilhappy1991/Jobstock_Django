"""
Navigation Context Processor
Makes navigation data available in all templates
"""
from App.services.navigation_service import NavigationService


def navigation_context(request):
    """
    Add navigation data to template context for all requests
    
    Usage in settings.py:
        TEMPLATES = [{
            'OPTIONS': {
                'context_processors': [
                    ...
                    'App.context_processors_navigation.navigation_context',
                ],
            },
        }]
    
    Then in any template:
        {{ dashboard_data.navigation }}
        {{ dashboard_data.widgets }}
        {{ dashboard_data.quick_actions }}
    """
    context = {
        'dashboard_data': {
            'navigation': [],
            'widgets': [],
            'quick_actions': [],
            'user': None,
        }
    }
    
    # Only add navigation for authenticated users
    if request.user.is_authenticated:
        result = NavigationService.get_complete_dashboard_data(request.user)
        
        if result.get('success'):
            context['dashboard_data'] = result.get('data', {})
    
    return context
