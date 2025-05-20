from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from api.views import ItemViewSet, ItemBOMViewSet

router_v1 = DefaultRouter()
router_v1.register(r'items', ItemViewSet, basename='item')

# Nested router for ItemBOM under Item
items_router_v1 = NestedDefaultRouter(router_v1, r'items', lookup='item')
items_router_v1.register(r'boms', ItemBOMViewSet, basename='item-boms')

urlpatterns_v1 = [
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
    path('', include(items_router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]
