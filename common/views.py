"""Module for views of application common."""
from datetime import datetime
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from common.constants import PAGINATOR_VALUE
from common.currency_rates import download_currency_rates
from common.forms import CalculateAmountForm, DownloadRatesForm
from common.mixins import (CurrencyMixin, CurrencyRateDetailMixin,
                           CurrencyRateMixin)
from common.models import Currency, CurrencyRate


class IndexView(TemplateView):
    """Home page of erp application."""

    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency_count'] = Currency.objects.count()
        context['currency_rates_count'] = CurrencyRate.objects.count()
        return context


class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    paginate_by = PAGINATOR_VALUE

    def get_queryset(self):
        queryset = super().get_queryset()
        text_of_filter = self.request.GET.get('filter_by_name')
        if text_of_filter:
            queryset = queryset.filter(name__icontains=text_of_filter)
        return queryset


class CurrencyDetailView(LoginRequiredMixin, CurrencyMixin, DetailView):
    model = Currency


class CurrencyCreateView(LoginRequiredMixin, CurrencyMixin, CreateView):
    model = Currency

    def form_valid(self, form):
        form.instance.created_by = self.request.user.username
        return super().form_valid(form)


class CurrencyUpdateView(LoginRequiredMixin, CurrencyMixin, UpdateView):
    model = Currency

    def form_valid(self, form):
        form.instance.modified_by = self.request.user.username
        return super().form_valid(form)


class CurrencyDeleteView(LoginRequiredMixin, CurrencyMixin, DeleteView):
    model = Currency
    success_url = reverse_lazy('common:currency_list')


class CurrencyRateListView(LoginRequiredMixin, ListView):
    model = CurrencyRate
    paginate_by = PAGINATOR_VALUE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Currency Rates'
        context['header'] = 'Currency Rates'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('currency')
        return queryset


class CurrencyRateDateListView(LoginRequiredMixin, ListView):
    model = CurrencyRate
    paginate_by = PAGINATOR_VALUE
    template_name = 'common/currencyrate_list.html'

    def get_queryset(self):
        rate_date = datetime.strptime(
            self.kwargs.get('date_str'), '%Y-%m-%d'
        ).date()
        if rate_date:
            return (super().get_queryset()
                    .filter(rate_date=rate_date)
                    .select_related('currency')
                    )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rate_date = self.kwargs.get('date_str')
        context.update({
            'title': f'Currency Rates by Date {rate_date}',
            'header': f'Currency Rates by Date {rate_date}',
        })
        return context


class CurrencyRateCurrencyListView(LoginRequiredMixin, ListView):
    model = CurrencyRate
    paginate_by = PAGINATOR_VALUE
    template_name = 'common/currencyrate_list.html'

    def get_queryset(self):
        currency = self.kwargs.get('currency_code')
        if currency:
            return (super().get_queryset()
                    .filter(currency=currency)
                    .select_related('currency')
                    )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = self.kwargs.get('currency_code')
        context.update({
            'title': f'Currency Rates by {currency}',
            'header': f'Currency Rates by {currency}'
        })
        return context


class CurrencyRateCreateView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    CreateView
):
    pk_url_kwarg = 'rate_date'

    def get_initial(self):
        initial = super().get_initial()
        initial['rate_date'] = timezone.now().date()
        return initial


class CurrencyRateDetailView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    CurrencyRateDetailMixin,
    DetailView
):
    pass


class CurrencyRateEditView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    CurrencyRateDetailMixin,
    UpdateView
):
    def form_valid(self, form):
        form.instance.modified_by = self.request.user.username
        return super().form_valid(form)


class CurrencyRateDeleteView(
    LoginRequiredMixin,
    CurrencyRateMixin,
    CurrencyRateDetailMixin,
    DeleteView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency_rate'] = self.object
        return context


def get_currency_rates(request):
    date_str = request.GET.get(
        'rate_date',
        timezone.now().date().strftime('%Y-%m-%d')
    )
    # Convert date string to dd/mm/yyyy format
    date_req = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    rates = download_currency_rates(request.user.username, date_req)
    if rates:
        return render(
            request,
            'common/download_rates.html',
            {
                'form': DownloadRatesForm(initial={'rate_date': date_str}),
                'rates': rates
            }
        )
    else:
        return HttpResponse(
            'Error fetching data from the Bank of Russia',
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


def download_rates(request):
    initial_data = {'rate_date': timezone.now().date()}
    form = DownloadRatesForm(initial=initial_data)
    return render(
        request,
        'common/download_rates.html',
        {'form': form}
    )


class CalculateAmountView(View):
    template_name = 'common/calculate_amount.html'

    def get(self, request):
        form = CalculateAmountForm(initial=self.get_initial())
        return render(request, self.template_name, {'form': form})

    def get_initial(self):
        return {
            'date': timezone.now().date(),
            'amount': 100,
        }

    def post(self, request):
        form = CalculateAmountForm(request.POST)
        result = None
        error_message = None
        rate = None

        if form.is_valid():
            currency = form.cleaned_data['currency']
            date = form.cleaned_data['date']
            amount = form.cleaned_data['amount']

            # Find the first available currency rate
            rate = CurrencyRate.objects.filter(
                currency=currency, rate_date__lte=date
            ).order_by('-rate_date').first()

            if rate:
                result = round((amount * rate.rate) / rate.nominal, 2)
            else:
                error_message = (f'Currency rate was not found for {currency} '
                                 f'and {date}!')

        return render(request, self.template_name, {
            'form': form,
            'result': result,
            'rate': rate,
            'error_message': error_message,
        })
