

from django.urls import path
from accounts import views

urlpatterns = [
      path('login/',views.HandleLogin.as_view(),name='login'),
      path('logout/',views.HandleLogout.as_view(),name='logout'),
      path('signup/',views.HandleSignup.as_view(),name='signup'),
      path('verify-otp/',views.CreateAccount.as_view(),name='otp'),
      path('google-login/', views.google_login, name='google-login'),
      path('google-callback/', views.google_callback, name='google-callback'),
]
        