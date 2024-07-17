from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from trip.views import RouteViewSet

router = DefaultRouter()
router.register(r"routes", RouteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
