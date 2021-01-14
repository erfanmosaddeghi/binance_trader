from django.urls import path
from .views import (
    CustomAuthToken, 
    register_view,
    Verification_view,
    checkServerTime_view,
    get_system_status_view,
    get_exchange_info_view,
    get_order_book_view
)

app_name = 'gateway'


urlpatterns = [
    path('register', register_view,name='register'), # For register NewUser
    path('login',CustomAuthToken.as_view(),name='Login'), # for login Users
    path('verification/<uid>/<token>',Verification_view.as_view(),name='verification_account'), # This Url For Email verification
    path('checkserver',checkServerTime_view,name="checkServerTime"), # This is just test server live!
    path('sysstatus',get_system_status_view,name="systemstatus"),
    path('exchangeinfo',get_exchange_info_view,name="exchangeinfo"),
    path('getorderbook',get_order_book_view,name="getorderbook"),
]