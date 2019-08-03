from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('income/', views.income_view, name='income'),
    path('quarter/', views.quarter_view, name='quarter'),
    path('cashflow/', views.cash_flow_view, name='cashflow'),
    path('balancesheet/', views.balance_sheet_view, name='balancesheet'),
    path('dividend/', views.dividend_view, name='dividend'),
    path('ratios/', views.ratios_view, name='ratios'),
]