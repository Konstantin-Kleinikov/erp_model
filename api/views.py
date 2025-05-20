from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ItemBOMSerializer, ItemSerializer
from common.models import Item, ItemBOM


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.username)

    def create(self, request, *args, **kwargs):
        is_bulk = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ItemViewSet(BaseViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemBOMViewSet(BaseViewSet):
    serializer_class = ItemBOMSerializer

    def get_queryset(self):
        item_id = self.kwargs['item_pk']  # 'item_pk' is derived from `lookup='item'`
        return ItemBOM.objects.filter(main_item__id=item_id)
