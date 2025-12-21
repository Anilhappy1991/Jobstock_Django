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
        {{ navigation_groups }}
        {{ dashboard_widgets }}
        {{ quick_actions }}
        {{ navigation_stats }}
    """
    context = {
        'navigation_groups': [],
        'dashboard_widgets': [],
        'quick_actions': [],
        'navigation_stats': {},
    }
    
    # Only add navigation for authenticated users
    if request.user.is_authenticated:
        service = NavigationService()
        
        # Get navigation data from service layer (returns ApiResponse format)
        nav_response = service.get_navigation_for_user(request.user)
        if isinstance(nav_response, dict) and nav_response.get('success'):
            context['navigation_groups'] = nav_response.get('data', {}).get('navigation', [])
        
        widgets_response = service.get_dashboard_widgets(request.user)
        if isinstance(widgets_response, dict) and widgets_response.get('success'):
            context['dashboard_widgets'] = widgets_response.get('data', {}).get('widgets', [])
        
        actions_response = service.get_quick_actions(request.user)
        if isinstance(actions_response, dict) and actions_response.get('success'):
            context['quick_actions'] = actions_response.get('data', {}).get('actions', [])
        
        stats_response = service.get_navigation_stats(request.user)
        if isinstance(stats_response, dict) and stats_response.get('success'):
            context['navigation_stats'] = stats_response.get('data', {})
    
    return context
