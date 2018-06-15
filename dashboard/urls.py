from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from geo.views import MapViewSet


router = routers.DefaultRouter()
router.register(r'maps', MapViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
