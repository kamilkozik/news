from django.conf import settings


def base(request):
    context = {'DEBUG': settings.DEBUG}
    return context
