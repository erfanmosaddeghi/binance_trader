from django.urls import path
from gateway.api.views import (
    register_view,
    Verification_view,
    checkServer_view
)

from gateway.api.views import CustomAuthToken

app_name = 'gateway'


urlpatterns = [
    path('register', register_view,name='register'), # For register NewUser
    path('login',CustomAuthToken.as_view(),name='Login'), # for login Users
    path('verification/<uid>/<token>',Verification_view.as_view(),name='verification_account'), # This Url For Email verification
    path('checkserver',checkServer_view,name="checkServer"), # This is just test server live!
    path('getmarketdepth',getMarketDepth_view,name="checkServer"),
    path('getrecenttrades',getrecentTrades_view,name="checkServer"),
    path('getaggregatetrades',getAggTrades_view,name="checkServer"),
]