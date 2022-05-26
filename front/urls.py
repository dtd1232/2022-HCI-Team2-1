from django.contrib.auth.views import LoginView
from django.urls import path

from front import views
from front.views import *

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', Register.as_view(), name='register'),
    path('play/<int:pk>/', views.Play.as_view(), name='play'),
    path('result/<int:pk>/', views.ResultView.as_view(), name='result'),
    path('', views.Selection.as_view()),
]
