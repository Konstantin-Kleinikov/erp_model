"""Mixins for common application."""
from django.shortcuts import get_object_or_404
from django.urls import reverse

from common.forms import CurrencyForm, CurrencyRateForm
from common.models import Currency, CurrencyRate


class CurrencyMixin:
    model = Currency
    form_class = CurrencyForm
    pk_url_kwarg = 'currency_code'


class CurrencyRateMixin:
    model = CurrencyRate
    form_class = CurrencyRateForm


class CurrencyRateDetailMixin:
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        currency_rate = get_object_or_404(CurrencyRate, pk=pk)
        return currency_rate

    def get_success_url(self):
        rate_date = self.object.rate_date
        return reverse(
            'common:currency_rates_date',
            kwargs={'date_str': rate_date.strftime('%Y-%m-%d')}
        )
