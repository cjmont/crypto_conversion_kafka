from django.conf import settings
from django.urls import path, include

from rest_framework.routers import DefaultRouter, SimpleRouter

from notbank.test.api import urls as test_urls
from notbank.transactions import urls as transactions_urls


# SimpleJWT imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
    path("test/", include(test_urls, namespace="test")),
    path("transactions/", include(transactions_urls, namespace="transactions")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

app_name = "api"
urlpatterns += router.urls
