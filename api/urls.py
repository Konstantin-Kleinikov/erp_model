from django.urls import include, path
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()


urlpatterns_v1 = [
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]