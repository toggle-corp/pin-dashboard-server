from rest_framework import serializers


class MetadataSerializer(serializers.Serializer):
    test = serializers.CharField()
