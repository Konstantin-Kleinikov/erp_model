from rest_framework import serializers

from common.models import Item, ItemBOM


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by')


class ItemSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Item


class ItemBOMSerializer(BaseSerializer):
    main_item = serializers.SlugRelatedField(
        queryset=Item.objects.all(),
        slug_field='item_id',
    )
    sub_item = serializers.SlugRelatedField(
        queryset=Item.objects.all(),
        slug_field='item_id',
    )

    class Meta (BaseSerializer.Meta):
        model = ItemBOM


class CurrencyRateSerializer(serializers.Serializer):
    rate_date = serializers.CharField(max_length=10)
