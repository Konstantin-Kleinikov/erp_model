from common.models import Currency, CurrencyRate, Item, ItemBOM, TelegramUser
from django.contrib import admin


@admin.register(Currency)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'iso_code',
        'numeric_code',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
        'note',
    )
    list_editable = (
        'name',
        'iso_code',
        'numeric_code',
    )
    list_display_links = ('code',)
    list_filter = (
        'code',
        'iso_code',
        'numeric_code',
    )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_id',
        'type',
        'unit_of_measure',
        'cost_price',
        'weight',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )

admin.site.register(CurrencyRate)
admin.site.register(TelegramUser)
admin.site.register(ItemBOM)
