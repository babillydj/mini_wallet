from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'wallet'
urlpatterns = [
    path('api/v1/wallet/', include(
        ([
            path('', views.Wallet.as_view(), name='generic_wallet'),
            path('deposits/', views.top_up, name='top_up_wallet'),
            path('withdrawals/', views.withdraw, name='withdraw_wallet'),
        ], 'wallet_api_v1')
    ))
]
