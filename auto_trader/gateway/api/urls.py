from django.urls import path
from gateway.api.views import (
    register,
    Verification,
    check
)

from gateway.api.views import CustomAuthToken


app_name = 'gateway'


urlpatterns = [
    path('register', register,name='register'),
    path('login',CustomAuthToken.as_view(),name='Login'),
    path('verification/<uid>/<token>',Verification.as_view(),name='verification_account'),
    path('check',check,name="check") # This is just test server live!
]