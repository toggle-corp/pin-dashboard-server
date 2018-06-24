from rest_framework import serializers
from .models import Map

import json


class MapSerializer(serializers.ModelSerializer):
    json = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Map
        fields = ('key', 'json', 'default_object')

    def get_json(self, map):
        if not map.file:
            return

        return json.loads(map.file.read().decode('utf-8'))
