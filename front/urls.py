from django.contrib import admin
from django.urls import path

import front
from front import views

urlpatterns = [
    path('', views.Home.as_view()),
    path('webcam/', views.webcam_feed)
]
