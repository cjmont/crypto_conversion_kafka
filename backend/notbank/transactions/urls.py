from django.urls import path

from notbank.transactions import views

app_name = 'transactions'

urlpatterns = [
    path('paytouser', views.PayToUserView.as_view(), name='paytouser'),
    path('transfer', views.TransferView.as_view(), name='transfer'),
    path('transfer-request', views.TransferRequestView.as_view(),
         name='transfer_request'),
    path('transfer-request/commit', views.CommitTransferRequest.as_view(),
         name='transfer_request_commit'),
    path('transfer_all', views.TransferAllView.as_view(), name='transfer_all'),
    path('conversions', views.QuoteView.as_view(), name='conversion'),
    path('quote', views.QuoteView.as_view(), name='quote'),
    path('requestid_all', views.RequestIdAllView.as_view(), name='requestid_all'),
    path('user', views.GetUserView.as_view(), name='user'),

]
