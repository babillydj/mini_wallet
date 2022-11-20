from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'auth_customer'
urlpatterns = [
    path('v1/', include(
        ([
            path('init/', views.init_wallet, name='init_wallet'),
        ], 'auth_v1')
    ))
]
