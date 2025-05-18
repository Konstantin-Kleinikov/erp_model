from rest_framework import serializers
from common.models import Item, ItemBOM


class ItemSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField()
    modified_by = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = '__all__'


class ItemBOMSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField()
    modified_by = serializers.ReadOnlyField()

    class Meta:
        model = ItemBOM
        fields = '__all__'
