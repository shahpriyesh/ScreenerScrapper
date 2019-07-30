from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('income/', views.income_view, name='income'),
    path('quarter/', views.quarter_view, name='quarter'),
]