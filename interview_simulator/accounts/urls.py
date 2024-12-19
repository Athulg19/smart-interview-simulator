from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_or_signup_view, name='login'),  # Default login/signup page
    path('logout/', views.logout_view, name='logout'),  # Logout
]
