from rest_framework.throttling import BaseThrottle
from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled

from ratelimit.exceptions import Ratelimited
from ratelimit.core import is_ratelimited


class LocalSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return True


class LowSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="300/m",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        return True


class StandardSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="500/h",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="40/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="150/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="10/2s",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        return True


class HighSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="120/d",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="60/h",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="20/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="150/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="10/2s",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        return True


class UltrahighSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="60/d",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="30/h",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="10/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="150/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="10/2s",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        return True


class StaffStandardSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="user_or_ip", rate="300/m",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="user_or_ip", rate="500/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        return True


class PublicApiSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="ip", rate="60/m",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="ip", rate="150/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='global', key="ip", rate="10/2s",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        return True


class AuthenticatedApiSecurityThrottle(BaseThrottle):
    def allow_request(self, request, view):
        old_limited = getattr(request, 'limited', False)
        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            key="header:X-MKT-APIKEY", rate="60/m",
            increment=True
        )

        request.limited = ratelimited or old_limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='api', key="ip", rate="200/m",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        ratelimited = is_ratelimited(
            request=request,
            fn=view.as_view(),
            group='api', key="ip", rate="20/2s",
            increment=True
        )

        request.limited = ratelimited or request.limited

        if ratelimited:
            return False

        return True


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):
        raise Ratelimited()

    return response
