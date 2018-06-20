from rest_framework import serializers
from dashboard.serializers import ListToDictField


class BaseMetadataSerializer(serializers.Serializer):
    landslides_surveyed = serializers.DictField(serializers.IntegerField)
    landslides_risk_rating = serializers.DictField(serializers.IntegerField)

    land_purchased = serializers.FloatField()
    geohazard_affected = serializers.DictField(serializers.IntegerField)
    landless = serializers.DictField(serializers.IntegerField)

    people_relocated = serializers.DictField(serializers.IntegerField)
    total_households = serializers.IntegerField()


class DistrictSerializer(BaseMetadataSerializer):
    district = serializers.CharField()


class CountrySerializer(BaseMetadataSerializer):
    districts = ListToDictField(
        child=DistrictSerializer(many=True),
        key='district',
    )
