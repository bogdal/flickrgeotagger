from django.conf import settings


def social_media_buttons(request):
    return {
        'SHOW_ADDTHIS_BUTTONS': getattr(settings, 'SHOW_GITHUB_BUTTONS'),
        'SHOW_GITHUB_BUTTONS': getattr(settings, 'SHOW_GITHUB_BUTTONS')}
