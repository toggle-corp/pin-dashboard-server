from rest_framework import (
    views,
    response,
)
from .serializers import MetadataSerializer


class MetadataView(views.APIView):
    def get(self, request):
        data = {'test': 'abc'}
        serializer = MetadataSerializer(data=data)
        serializer.is_valid()
        return response.Response(serializer.data)
