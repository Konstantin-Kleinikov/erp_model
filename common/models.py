from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator

from common.choices import ITEM_TYPES, UNIT_OF_MEASURES
from common.constants import NUM_OF_WORDS_IN_DESC
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
        ordering = ['user__username', 'telegram_id']
        verbose_name = 'telegram user'
        verbose_name_plural = 'Telegram Users'

    def __str__(self):
        return f'{self.user.username} - {self.telegram_id}'


class Item(AuditTrailModel, NoteModel):
    item_id = models.CharField(
        'Item ID',
        max_length=50,
        unique=True,
    )
    description = models.CharField(
        'Description',
        max_length=150,
    )
    type = models.CharField(
        'Item Type',
        max_length=20,
        choices=ITEM_TYPES,
        default='Purchased',
    )
    unit_of_measure = models.CharField(
        'Unit of Measure',
        max_length=4,
        choices=UNIT_OF_MEASURES,
        default='pcs.',
    )
    cost_price = models.FloatField(
        'Cost Price',
        default=0,
    )
    weight = models.FloatField(
        'Weight',
        default=0,
    )
    image = models.ImageField(
        'Item image',
        blank=True,
        upload_to='item_images',
    )

    class Meta:
        ordering = ['item_id']
        verbose_name = 'item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return (f'{self.item_id} - '
                f'{Truncator(self.description).words(NUM_OF_WORDS_IN_DESC)}')


class ItemBOM(AuditTrailModel):
    main_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='main_items',
        verbose_name='Main Item',
    )
    sub_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='sub_items',
        verbose_name='Sub Item',
    )
    bom_quantity = models.PositiveSmallIntegerField(
        'Bom Quantity',
        default=1,
    )

    class Meta:
        ordering = ['main_item', 'sub_item']
        verbose_name = 'BOM Item'
        verbose_name_plural = 'BOM Items'
        constraints = [
            models.UniqueConstraint(
                fields=['main_item', 'sub_item'],
                name='unique_main_sub_items',
            ),
            models.CheckConstraint(
                check=~models.Q(main_item=models.F('sub_item')),
                name='prevent_self_item'
            ),
        ]

    def clean(self):
        if self.main_item.type != 'Produced':
            raise ValidationError(
                {'main_item': 'The main item must have a type of "Produced".'}
            )

    def __str__(self):
        return f'{self.main_item.item_id} - {self.sub_item.item_id}'
