from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import AuditTrailModel, NoteModel

User = get_user_model()


class Currency(AuditTrailModel, NoteModel):
    code = models.CharField(
        primary_key=True,
        max_length=3,
        unique=True,
        null=False,
        verbose_name='Currency Code',
    )
    name = models.CharField(
        max_length=30,
        verbose_name='Short Description',
    )
    iso_code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name='ISO',
    )
    numeric_code = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return f'{self.code} - {self.name}'

    def get_absolute_url(self):
        return reverse(
            'common:currency_detail',
            kwargs={'currency_code': self.code},
        )


class CurrencyRate(AuditTrailModel):
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='rates',
        verbose_name='Currency',
    )
    rate_date = models.DateField(blank=False, null=False)
    nominal = models.PositiveSmallIntegerField(default=1)
    rate = models.FloatField(blank=False, null=False)

    class Meta:
        ordering = ['-rate_date', 'currency']
        verbose_name = 'Currency Rate'
        verbose_name_plural = 'Currency Rates'
        unique_together = ('currency', 'rate_date')

    def __str__(self):
        return f'{self.currency.code} - {self.rate_date}'

    def get_absolute_url(self):
        return reverse(
            'common:currency_rates_date',
            kwargs={'date': self.rate_date},
        )


class TelegramUser(models.Model):
    telegram_id = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name='Telegram ID',
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='telegram_user',
    )

    class Meta:
        ordering = ['user__username']
        verbose_name = 'telegram user'
        verbose_name_plural = 'Telegram Users'

    def __str__(self):
        return f'{self.user.username} - {self.telegram_id}'
