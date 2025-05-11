"""Module with forms for common application."""
from django import forms

from common.models import Currency, CurrencyRate


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = [
            'code',
            'name',
            'iso_code',
            'numeric_code',
            'note',
            # 'created_at',
            # 'created_by',
            # 'modified_at',
            # 'modified_by',
        ]


class CurrencyRateForm(forms.ModelForm):
    rate_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CurrencyRate
        fields = [
            'currency',
            'rate_date',
            'nominal',
            'rate',
        ]


class DownloadRatesForm(forms.Form):
    rate_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class CalculateAmountForm(forms.Form):
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        label='Currency',
        required=True
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date',
        required=True
    )
    amount = forms.FloatField(
        label='Currency Amount',
        required=True,
        min_value=0
    )
