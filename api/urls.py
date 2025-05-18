from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ItemViewSet, ItemBOMViewSet

router_v1 = DefaultRouter()
router_v1.register(r'items', ItemViewSet, basename='item')
router_v1.register(r'itemboms', ItemBOMViewSet, basename='itembom')

urlpatterns_v1 = [
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]
