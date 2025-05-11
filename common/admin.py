from django.contrib import admin

from .models import Currency, CurrencyRate, TelegramUser


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


admin.site.register(CurrencyRate)
admin.site.register(TelegramUser)
