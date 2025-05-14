from django.urls import path

from common.views import (CalculateAmountView, CurrencyRateCreateView,
                          CurrencyRateDeleteView, CurrencyRateDetailView,
                          CurrencyRateEditView, download_rates,
                          get_currency_rates)

from . import views

app_name = 'common'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'calculate_amount_in_RUB/',
        CalculateAmountView.as_view(),
        name='calculate_amount',
    ),
    path(
        'currency/',
        views.CurrencyListView.as_view(),
        name='currency_list',
    ),
    path(
        'currency/detail/<str:currency_code>/',
        views.CurrencyDetailView.as_view(),
        name='currency_detail',
    ),
    path(
        'currency/create/',
        views.CurrencyCreateView.as_view(),
        name='currency_create',
    ),
    path(
        'currency/edit/<str:currency_code>/',
        views.CurrencyUpdateView.as_view(),
        name='currency_edit',
    ),
    path(
        'currency/delete/<str:currency_code>/',
        views.CurrencyDeleteView.as_view(),
        name='currency_delete',
    ),
    path(
        'currency_rates/',
        views.CurrencyRateListView.as_view(),
        name='currency_rates',
    ),
    path(
        'currency_rates/<int:pk>/',
        CurrencyRateDetailView.as_view(),
        name='currency_rates_detail',
    ),
    path(
        'currency_rates/date/<str:date_str>/',
        views.CurrencyRateDateListView.as_view(),
        name='currency_rates_date',
    ),
    path(
        'currency_rates/currency/<str:currency_code>/',
        views.CurrencyRateCurrencyListView.as_view(),
        name='currency_rates_currency',
    ),
    path(
        'currency_rates/create/',
        CurrencyRateCreateView.as_view(),
        name='currency_rates_create',
    ),
    path(
        'currency_rates/edit/<int:pk>/',
        CurrencyRateEditView.as_view(),
        name='currency_rates_edit',
    ),
    path(
        'currency_rates/delete/<int:pk>/',
        CurrencyRateDeleteView.as_view(),
        name='currency_rates_delete',
    ),
    path(
        'get_currency_rates/',
        get_currency_rates,
        name='get_currency_rates',
    ),
    path(
        'download_rates/',
        download_rates,
        name='download_rates',
    ),
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('item/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('item/edit/<int:pk>/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('item/delete/<int:pk>/', views.ItemDeleteView.as_view(), name='item_delete'),
]
