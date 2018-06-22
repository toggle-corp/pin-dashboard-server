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


class GaupalikaSerializer(BaseMetadataSerializer):
    gaupalika = serializers.CharField(source='gaupalika.code')


class DistrictDetailSerializer(BaseMetadataSerializer):
    district = serializers.CharField()
    gaupalikas = ListToDictField(
        child=GaupalikaSerializer(many=True),
        key='gaupalika',
    )


class DistrictSerializer(BaseMetadataSerializer):
    district = serializers.CharField(source='district.code')


class CountrySerializer(BaseMetadataSerializer):
    districts = ListToDictField(
        child=DistrictSerializer(many=True),
        key='district',
    )
