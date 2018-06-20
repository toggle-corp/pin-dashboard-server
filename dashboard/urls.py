from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from geo.views import MapViewSet
from metadata.views import MetadataView


router = routers.DefaultRouter()
router.register(r'maps', MapViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/metadata/', MetadataView.as_view()),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
