from rest_framework import viewsets

from .models import Map
from .serializers import MapSerializer


class MapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    lookup_field = 'key'
    lookup_url_kwarg = 'pk'
