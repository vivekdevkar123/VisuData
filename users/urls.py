from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('OtpVerification/', OtpVerification, name='OtpVerification'),
]
