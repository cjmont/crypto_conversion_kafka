import os

from time import time

from ipware import get_client_ip
from ratelimit.exceptions import Ratelimited

from django.views import defaults
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.translation import gettext_lazy as _

from notbank.base.decorators.throttling_views import ultrahigh_security


# ERROR VIEWS
# ======================================================================================================================
@ultrahigh_security
def error_400(request, exception):
    return defaults.bad_request(request=request, exception=exception, template_name='error/400.html')


@ultrahigh_security
def error_403(request, exception):
    return defaults.permission_denied(request=request, exception=exception, template_name='error/403.html')


@ultrahigh_security
def error_404(request, exception):
    return defaults.page_not_found(request=request, exception=exception, template_name='error/404.html')


@ultrahigh_security
def error_500(request):
    return defaults.server_error(request=request, template_name='error/500.html')


# RATELIMIT ERROR VIEWS
# ======================================================================================================================
def locked(request, exception):
    if isinstance(exception, Ratelimited):
        ip, routable = get_client_ip(request)
        if ip and ip not in settings.LOCAL_IPS:
            add_ip = True  # TODO : is a constant ?
            if add_ip:
                # print("add ip")
                with open(os.path.join(str(settings.ROOT_DIR), 'ban_ip.txt'), 'a+') as f:
                    f.write(str(int(time())) + '*' +
                            request.path + '*' + ip + '\n')
    request.session['VALID_IS_ROBOT'] = False

    return JsonResponse({
        'status': 'error',
        'code': 'rate_limited',
        'message': str(_('Demasiadas solicitudes'))
    }, status=429)


# CSRF ERROR VIEWS
# ======================================================================================================================
@ultrahigh_security
def csrf(request, reason=""):
    ip, routable = get_client_ip(request)
    if ip and ip not in settings.LOCAL_IPS:
        add_ip = True  # TODO : is a constant ?
        if add_ip:
            with open(os.path.join(str(settings.ROOT_DIR), 'ban_ip.txt'), 'a+') as f:
                f.write(str(int(time())) + '*' +
                        request.path + '*' + ip + '\n')

    return JsonResponse({
        'status': 'error',
        'code': 'rate_limited',
        'message': str(_('Sesión no iniciada'))
    }, status=429)
