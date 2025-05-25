from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ItemBOMSerializer, ItemSerializer, CurrencyRateSerializer
from common.currency_rates import download_currency_rates
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


class CurrencyRateViewSet(viewsets.GenericViewSet):
    """
    API endpoint to download currency rates for a specific date.
    Accepts a POST request with a JSON payload containing the rate_date.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencyRateSerializer  # Use the serializer

    @action(detail=False, methods=['post'])
    def download(self, request):
        """
        Handles POST requests to download currency rates for a specific date.

        This method extracts the `rate_date` from the request payload, validates it,
        and calls the `download_currency_rates` function to fetch the rates. It then
        returns a response indicating success or failure.

        Args:
            request (Request): The HTTP request object containing the `rate_date` in the payload.

        Returns:
            Response: A JSON response with a success or error message and the downloaded rates (if any).
        """
        date_str = request.data.get('rate_date')
        if not date_str:
            return Response(
                {"error": "Date is required in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date_req = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user.username
        rates = download_currency_rates(user, date_req)

        if rates:
            return Response(
                {"message": "Currency rates downloaded successfully.", "rates": rates},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "No rates were downloaded or an error occurred."},
                status=status.HTTP_200_OK
            )