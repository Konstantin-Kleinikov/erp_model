from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.models import Item, ItemBOM
from .serializers import ItemSerializer, ItemBOMSerializer


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user.username,
            modified_by=self.request.user.username
        )

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.username)


class ItemViewSet(BaseViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ItemBOMViewSet(BaseViewSet):
    queryset = ItemBOM.objects.all()
    serializer_class = ItemBOMSerializer
