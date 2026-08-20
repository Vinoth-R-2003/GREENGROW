from .models import Notification

def notifications_count(request):
    """Make unread notifications count available globally in templates."""
    try:
        if request.user.is_authenticated:
            count = request.user.notifications.filter(is_read=False).count()
            recent = request.user.notifications.all()[:5]
            return {
                'unread_notifications_count': count,
                'recent_notifications': recent
            }
    except Exception:
        pass
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }
