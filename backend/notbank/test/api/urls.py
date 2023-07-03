from django.urls import path

from notbank.test.api import status as status_views

app_name = 'test'

urlpatterns = [
    path("status", status_views.StatusView.as_view(), name="status_view")
]
